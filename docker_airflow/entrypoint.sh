#!/usr/bin/env bash

if [ -e "/root/airflow/requirements/requirements.txt"  ]; then
    $(command -v pip) install -r /root/airflow/requirements/requirements.txt
fi

mkdir /root/venvs
if [ -e "/root/airflow/requirements/requirements-tap.txt"  ]; then
    python3 -m venv /root/venvs/tap-minio-csv
    /root/venvs/tap-minio-csv/bin/pip install -r /root/airflow/requirements/requirements-tap.txt
fi

if [ -e "/root/airflow/requirements/requirements-target.txt"  ]; then
    python3 -m venv /root/venvs/target-postgres
    /root/venvs/target-postgres/bin/pip install -r /root/airflow/requirements/requirements-target.txt
fi


case "$1" in
  webserver)
    airflow db init
    airflow users create \
    --username airflow \
    --firstname Marcin \
    --lastname Migda \
    --role Admin \
    --email marcin700@gmail.com \
    --password airflow

    num_tries=60
    while [ ${num_tries} != 0 ]; do
      airflow_check=$(airflow db check)
      if [[ $airflow_check == *"Connection successful"* ]]  ; then

        airflow connections add --conn-type 'postgres' --conn-host 'postgres' --conn-login ${POSTGRES_USER} --conn-password ${POSTGRES_PASSWORD} --conn-port 5432 --conn-schema 'postgres' 'local_postgres'
        airflow connections add --conn-type 'aws' --conn-extra '{"host": "'"http://minio-s3:9000"'"}' 'local_minio'

        num_tries=0
      else
        num_tries=$((num_tries - 1))
        sleep 3
      fi
    done

    airflow scheduler &
    airflow dags backfill spoton_assignment -s 2022-12-18 &
    exec airflow webserver --port 8080
    ;;
  worker|scheduler)
    # To give the webserver time to run initdb.
    sleep 10
    exec airflow "$@"
    ;;
  flower)
    sleep 10
    exec airflow "$@"
    ;;
  version)
    exec airflow "$@"
    ;;
  *)
    exec "$@"
    ;;
esac
