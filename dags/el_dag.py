"""
This module contains the definition of an EL (Extract, Load) DAG for an Airflow workflow.
The DAG is responsible for extracting data from CSV files, transforming it into a suitable format,
and loading it into a database.
"""

import sys
import os
import shutil
import pandas as pd

from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from crud import create_data
from models import TowerModel, KPIModel
from schemas import TowerSchema, KPISchema
from database import init_db

dag = DAG(
    dag_id="el_dag",
    description="Extract and Load DAG",
    schedule_interval=timedelta(minutes=1),
    start_date=datetime(2024, 7, 8),
    catchup=False,
)

DATA_TOWERS_PATH = Path("/opt/airflow/data/towers")
DATA_KPIS_PATH = Path("/opt/airflow/data/kpis")

wait_for_generator_dag = ExternalTaskSensor(
    task_id="wait_for_generator_dag",
    external_dag_id="simulation_dag",
    external_task_id="data_generate_task",
    dag=dag,
    mode="poke",
    timeout=10,
    poke_interval=30,
)


def to_database_tower(**kwargs):
    for data in os.listdir(DATA_TOWERS_PATH):
        df = pd.read_csv(DATA_TOWERS_PATH.joinpath(data))
        create_data(data=df, model=TowerModel, schema=TowerSchema)


def to_database_kpis(**kwargs):
    for data in os.listdir(DATA_KPIS_PATH):
        df = pd.read_csv(DATA_KPIS_PATH.joinpath(data))
        create_data(data=df, model=KPIModel, schema=KPISchema)


def clean_data_path(**kwargs):
    shutil.rmtree(DATA_KPIS_PATH)


init_db_task = PythonOperator(task_id="init_db_task", python_callable=init_db, dag=dag)

to_database_tower_task = PythonOperator(
    task_id="to_database_tower_task", python_callable=to_database_tower, dag=dag
)

to_database_kpis_task = PythonOperator(
    task_id="to_database_kpis_task", python_callable=to_database_kpis, dag=dag
)

delete_dir_task = PythonOperator(
    task_id="delete_dir_task", python_callable=clean_data_path, dag=dag
)

(
    #wait_for_generator_dag
    init_db_task
    >> to_database_tower_task
    >> to_database_kpis_task
    >> delete_dir_task
)
