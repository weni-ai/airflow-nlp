# syntax=docker/dockerfile:1.4

FROM apache/airflow:2.3.4

RUN pip install --no-cache-dir mlflow datetime pandas sklearn transformers torch simplet5

COPY dags/* /opt/airflow/dags/
COPY plugins/* /opt/airflow/plugins/

