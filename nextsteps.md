## How to run?

To start all the required containers, run the given command:
```bash
docker-compose up
```

This will create 3 containers:
- minio-s3
- db (postgres)
- Airflow (this container will automatically start the ingestion flow)

When lines similar to these appear in the terminal, it means that the flow has finished and the data should already be available in the corresponding tables in the database.
```shell
data_engineering_assignment-ingest-1    | [2022-12-20 15:19:05,163] {backfill_job.py:367} INFO - [backfill progress] | finished run 1 of 1 | tasks waiting: 0 | succeeded: 8 | running: 0 | failed: 0 | skipped: 0 | deadlocked: 0 | not ready: 0
data_engineering_assignment-ingest-1    | [2022-12-20 15:19:05,170] {backfill_job.py:879} INFO - Backfill done. Exiting.

```

To access the Airflow UI, go to http://localhost:8080
```shell
user: airflow
pass: airflow
```

To access the Minio UI, go to http://localhost:9001
```shell
user: spotonaccesskey
pass: spotonsecretkey
```

To access the Postgres DB use the following credentials:
```shell
host: localhost
port: 5432
user: postgres
pass: postgres
db: postgres
```

## What does it do?

1. It downloads data from the Kaggle API.
2. It processes the data.
3. It saves the processed data to the Minio S3 bucket.
4. It loads the data to the Postgres DB using Singer Minio Tap and Postgres Target.

Flow is created and scheduled using Airflow.
All Airflow files can be found in the `airflow` directory. It includes DAG, configuration and helper functions and classes.
All the Singer configuration files can be found in the `singer` directory.

Before making processing I looked into csv files using Jupyter Notebook. I've prepared a notebook with some basic analysis and data exploration. It can be found in the `notebooks` directory.

## What can be improved?
Due to the fact that the data loading was one-time, I did not apply in my solution some patterns that should be used for multiple/continuous processing.

1. In the case of processing data on an ongoing basis (e.g., once a day, once an hour), it would be necessary to use partitioning where the data is stored. For example, include in the directory structure what day/time it came from. This will allow you to easily find the data you need and will also allow you to easily delete old data. I.e. `/{year}/{month}/{day}/{hour}/{file_name}.csv`. The granularity should depend on what type of data we are dealing with and its size and also how it is processed.
2. With properly partitioned input data, we can parallelize its processing.
3. Depending on how the data loaded into the database will be used later, we can next use `dbt` to prepare the appropriate views for the required needs.
4. If the source of input data would be some message broker, such as Kafka or Google PubSub, then if there is a possibility, it is worth using verification of transmitted data using, for example, Avro Schema.
5. If there is a possibility, it is worth finding out how the data will be used later. As a result, in some cases it is worth applying denormalization to the database to gain performance and reduce CPU/RAM costs.
6. The configuration of Airflow itself in a production environment should have other parameters (e.g., do not use sqlite, do not use SequentialExecutor, provide monitoring, distributed execution, etc.).
7. If there is a need to reach many times for the same set of data in processing, some kind of cache can be used.
8. For sensitive production data, pseudo-anonymization can be used at the processing stage.
9. If you have performance issues, consider using other frameworks, such as Apache Spark or Apache Flink.
10. Niektóre przypadki użycia mogą wymagać użycia windowingu w przetwarzaniu przy pomocy Apache Flink czy używając Kafka Streams.
11. If the generated CSV files are very large, it is worth considering storing them in another format, such as ORC, Parquet using a distributed file system such as HDFS.
12. Some of the data can be saved to H5 format (or any other format used by the team) and pushed out using DVC if the need arises from Data Scientists.
