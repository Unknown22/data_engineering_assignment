import os
from datetime import datetime
import yaml

from processors.spoton_assignment import get_file_processor

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


with open("/root/airflow/dags/config/spoton_assignment.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)


def process_files(**context):
    if not os.path.exists(f"{CONFIG['dataset_download_dir']}/processed-files"):
        os.makedirs(f"{CONFIG['dataset_download_dir']}/processed-files")

    for filename in CONFIG["files_to_process_and_storage"]:
        get_file_processor(filepath=f"{CONFIG['dataset_download_dir']}/preprocessed-files/{filename}").transform()


def place_files_in_object_storage(**context):

    minio = S3Hook("local_minio")
    if not minio.check_for_bucket(CONFIG['minio']['bucket']):
        minio.create_bucket(CONFIG['minio']['bucket'])

    for file in CONFIG["files_to_process_and_storage"]:
        minio.load_file(
            filename=f"{CONFIG['dataset_download_dir']}/processed-files/{file}",
            key=file,
            bucket_name=CONFIG['minio']['bucket'],
            replace=True,
        )


def prepare_singer_operator(name, schema_path, tap_path, tap_config_path, target_path, target_config_path):
    return BashOperator(
        task_id=f"singer_{name}",
        bash_command=f"{tap_path} -c {tap_config_path} -p {schema_path} | {target_path} -c {target_config_path} -p {schema_path}",
    )


with DAG(
        dag_id="spoton_assignment",
        start_date=datetime(2022, 12, 18),
        schedule_interval='@once'
) as dag:
    retrieve_data = BashOperator(
        task_id="retrieve_data_from_kaggle",
        bash_command="kaggle datasets download -d olistbr/brazilian-ecommerce "
                     f"-p {CONFIG['dataset_download_dir']}",
    )

    unzip_data = BashOperator(
        task_id="unzip_data",
        bash_command=f"unzip -o {CONFIG['dataset_download_dir']}/brazilian-ecommerce.zip "
                     f"-d {CONFIG['dataset_download_dir']}/preprocessed-files/",
    )

    process_files = PythonOperator(
        task_id="process_files",
        python_callable=process_files,
    )

    place_files_in_object_storage = PythonOperator(
        task_id="place_files_in_object_storage",
        python_callable=place_files_in_object_storage,
    )

    retrieve_data >> unzip_data >> process_files >> place_files_in_object_storage

    for singer_config in CONFIG["singer_configs"]:
        singer = prepare_singer_operator(
            name=singer_config["name"],
            schema_path=singer_config["schema_path"],
            tap_path=singer_config["tap"]["path"],
            tap_config_path=singer_config["tap"]["config_path"],
            target_path=singer_config["target"]["path"],
            target_config_path=singer_config["target"]["config_path"],
        )
        place_files_in_object_storage >> singer
