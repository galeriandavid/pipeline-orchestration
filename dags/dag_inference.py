from datetime import datetime, timedelta
import json

import airflow
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models.connection import Connection


default_args = {
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    #"queue": "bash_queue",
    #"priority_weight": 10,
    #"end_date": datetime(2024, 1, 1),
    #"wait_for_downstream": False,
    #"sla": timedelta(hours=2),
    #"execution_timeout": timedelta(seconds=300),
    #"on_failure_callback": some_function, # or list of functions
    #"on_succcess_callnack": another_function, # or list of functions
    #"on_retry_callback": another_function, # or list of functions
    #"sla_miss_callback": another_function, # or list of functions
    #"trigger_rule": "all_success"
}


with DAG(
    "Home_Work_inference",
    default_args=default_args,
    description="Pipeline orchestration",
    schedule=timedelta(days=1),
    start_date=datetime(2023, 11, 10),
    catchup=False,
    tags=["home_work"]
    ) as dag:

    data_sensing_task = FileSensor(task_id='sense_the_csv',
                                   fs_conn_id="fs_default",
                                   filepath="inference_data.csv",
                                   mode="reschedule",
                                   poke_interval=timedelta(seconds=10),
                                   timeout=timedelta(hours=23))

    task_1 = BashOperator(
        task_id="predict",
        bash_command="python /opt/airflow/src/inference.py",
    )

    data_sensing_task >> task_1


if __name__ == "__main__":
    dag.test()