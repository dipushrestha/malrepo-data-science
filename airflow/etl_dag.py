"""Airflow DAG for ETL pipeline."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "finanalytics",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "finanalytics_etl",
    default_args=default_args,
    description="Daily ETL pipeline for transaction data",
    schedule_interval="0 6 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["etl", "transactions"],
) as dag:

    download = BashOperator(
        task_id="download_data",
        bash_command="cd /opt/finanalytics && python scripts/download_data.py",
    )

    preprocess = PythonOperator(
        task_id="preprocess",
        python_callable=lambda: __import__("src.data.preprocessing", fromlist=["run_preprocessing"]).run_preprocessing(
            "data/raw/transactions.csv", "data/interim/cleaned.parquet"
        ),
    )

    build_features = PythonOperator(
        task_id="build_features",
        python_callable=lambda: __import__("src.features.build_features", fromlist=["build_features"]).build_features(
            "data/interim/cleaned.parquet", "data/processed/features.parquet"
        ),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/finanalytics/dbt && dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/finanalytics/dbt && dbt test",
    )

    download >> preprocess >> build_features
    preprocess >> dbt_run >> dbt_test
