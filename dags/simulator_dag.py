"""
This module is responsible for generating CSV data for telecom towers and their associated KPIs.
The data is generated using the `TowerGenerator` and `KPIDataGenerator` classes.
The generated data is stored in separate directories for towers and KPIs.
"""

import sys, os
import pandas as pd 

from pathlib import Path 
from datetime import datetime, timedelta 
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'simulator')))


from airflow import DAG 
from airflow.operators.python import PythonOperator
from ran_simulator import TowerGenerator, KPIDataGenerator

default_args = {
    "owner": "adminstrator",
    "start_date": datetime(2024, 7, 26),
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "simulation_dag",
    default_args=default_args,
    description="Data generator DAG",
    schedule_interval=timedelta(minutes=1),
    catchup=False,
)

NUM_TOWERS = os.getenv("NUM_TOWERS")
NUM_RECORDS_PER_TOWER = os.getenv("NUM_RECORDS_PER_TOWER")
DATA_TOWERS_PATH = Path("/opt/airflow/data/towers")
DATA_KPIS_PATH = Path("/opt/airflow/data/kpis")

def directory_generate_task(**kwargs):
    os.makedirs(DATA_TOWERS_PATH, exist_ok=True)
    os.makedirs(DATA_KPIS_PATH, exist_ok=True)

def generate_data_task(**kwargs):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    if not os.listdir(DATA_TOWERS_PATH):
        tower_generator = TowerGenerator(n_towers=NUM_TOWERS)
        towers_df = tower_generator.generate_data()
        towers_df.to_csv(
            DATA_TOWERS_PATH.joinpath(f"towers_data_{timestamp}.csv"), index=False
        )
    else:
        towers_df_name = os.listdir(DATA_TOWERS_PATH)[0]
        towers_df = pd.read_csv(DATA_TOWERS_PATH.joinpath(towers_df_name))

    kpis_generator = KPIDataGenerator()
    kpis_df_list = []
    for tower_name in towers_df["tower_id"]:
        kpis_df = kpis_generator.generate_kpis_data_for_site(
            site_name=tower_name, n_records=NUM_RECORDS_PER_TOWER
        )
        kpis_df_list.append(kpis_df)

    kpis_df = pd.concat(kpis_df_list, ignore_index=True)
    kpis_df.to_csv(DATA_KPIS_PATH.joinpath(f"kpis_data_{timestamp}.csv"), index=False)

dir_task = PythonOperator(
    task_id="directory_management_task", python_callable=directory_generate_task, dag=dag
)

gen_data_task = PythonOperator(
    task_id="data_generate_task", python_callable=generate_data_task, dag=dag
)

dir_task >> gen_data_task