# Data Engineering Assignment

## Assignment
Your task is to automate download and ingestion of the data from the [Brazilian ecommerce data set from Kaggle](https://www.kaggle.com/olistbr/brazilian-ecommerce). 

1) Fork this repo to your account
2) Create an account with Kaggle if you don't already have one.  You will need this to access their API to retreive data for the assigment.
3) Create a script to retrieve Brazilian eCommerce data from Kaggle api and place the files listed below in object storage.
  - Minio is provided in docker compose or feel free to use your choice of object storage (e.g. AWS, S3)
  - **Load only the following datasets: olist_customers_dataset.csv, olist_order_items_dataset.csv, olist_orders_dataset.csv, olist_products_dataset.csv**

4) Ingest files from object storage into Postgres using Singer, python or your programming language of choice.  Provided is a base python image in the `Dockerfile` along with a Postgres instance that can be created using docker compose.  Your ingestion process should create a table for each file.  Here are some helpful links if you are using singer (hint, we link singer ;), but use whatever you are most comfortable with)
    - CSV Singer tap: https://github.com/singer-io/tap-s3-csv
    - Postgres Singer target: https://github.com/datamill-co/target-postgres

5) Create a nexsteps.md in the repo and cover deployment considerations along with thoughts on further optimization for scale.


## Acceptance Criteria
- We will pulling from the master/main branch of your provided repo link
- We should be able to run your code by running the following command `docker-compose run ingest`.
- We should be able to access the generated tables in the Postgres DB at `localhost:5432`.
