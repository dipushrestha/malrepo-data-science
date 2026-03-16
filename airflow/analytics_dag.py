"""Airflow DAG for analytics and model training."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor

default_args = {
    "owner": "finanalytics",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    "finanalytics_analytics",
    default_args=default_args,
    description="Weekly model retraining and analytics",
    schedule_interval="0 8 * * 1",  # Every Monday at 8am
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["analytics", "ml"],
) as dag:

    wait_for_etl = ExternalTaskSensor(
        task_id="wait_for_etl",
        external_dag_id="finanalytics_etl",
        external_task_id="build_features",
        timeout=3600,
        mode="reschedule",
    )

    train_model = BashOperator(
        task_id="train_model",
        bash_command="cd /opt/finanalytics && python scripts/train_models.py",
    )

    generate_report = BashOperator(
        task_id="generate_report",
        bash_command="cd /opt/finanalytics && python scripts/generate_report.py",
    )

    wait_for_etl >> train_model >> generate_report
