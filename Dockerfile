FROM apache/airflow:latest

EXPOSE 8080

WORKDIR /opt/airflow

RUN pip install poetry 

COPY . . 

RUN poetry install

RUN mkdir -p /opt/airflow/logs && chown -R airflow:airflow /opt/airflow/logs
