"""Airflow shared configuration."""
import os

# Connection strings
POSTGRES_CONN_ID = "finanalytics_postgres"
SNOWFLAKE_CONN_ID = "finanalytics_snowflake"
S3_CONN_ID = "finanalytics_s3"

# Paths
PROJECT_ROOT = os.getenv("FINANALYTICS_ROOT", "/opt/finanalytics")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

# Notifications
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "alerts@finanalytics.dev")
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK", "")
