from datetime import datetime, timedelta
import os, sys

import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator


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
    "Home_Work_ETL_train",
    default_args=default_args,
    description="Pipeline orchestration",
    schedule=timedelta(days=1),
    start_date=datetime(2023, 11, 10),
    catchup=False,
    tags=["home_work"]
    ) as dag:
    

    task_1 = BashOperator(
        task_id="ETL",
        bash_command="python /opt/airflow/src/etl_pipeline.py",

    )

    task_2 = BashOperator(
        task_id="train_model",
        bash_command="python /opt/airflow/src/train.py",
    )
    task_1 >> task_2


if __name__ == "__main__":
    dag.test()