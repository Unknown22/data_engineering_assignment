FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  libssl-dev \
  libffi-dev \
  python3-dev \
  libpq-dev \
  libblas-dev \
  liblapack-dev \
  libatlas-base-dev \
  gfortran \
  unzip \
  vim

# Install Airflow
RUN pip install apache-airflow[aws]==2.3.3

COPY docker_airflow/entrypoint.sh /root/airflow/
COPY docker_airflow/requirements.txt /root/airflow/requirements/
COPY docker_airflow/requirements-tap.txt /root/airflow/requirements/
COPY docker_airflow/requirements-target.txt /root/airflow/requirements/

ENTRYPOINT ["/root/airflow/entrypoint.sh"]