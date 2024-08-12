FROM apache/airflow:latest

EXPOSE 8080

WORKDIR /opt/airflow

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . . 

RUN mkdir -p /opt/airflow/logs