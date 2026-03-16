"""Data loading and database connectors."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

from src.utils.logging import get_logger

logger = get_logger(__name__)


def load_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """Load CSV file into DataFrame."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    logger.info(f"Loading {path}")
    return pd.read_csv(path, **kwargs)


def load_parquet(path: str | Path, **kwargs) -> pd.DataFrame:
    """Load Parquet file into DataFrame."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    logger.info(f"Loading {path}")
    return pd.read_parquet(path, **kwargs)


def save_parquet(df: pd.DataFrame, path: str | Path) -> None:
    """Save DataFrame as Parquet."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    logger.info(f"Saved {len(df)} rows to {path}")


class SnowflakeConnector:
    """Connector for Snowflake data warehouse."""

    def __init__(self, account: Optional[str] = None, user: Optional[str] = None,
                 password: Optional[str] = None):
        import os
        self.account = account or os.getenv("SNOWFLAKE_ACCOUNT")
        self.user = user or os.getenv("SNOWFLAKE_USER")
        self.password = password or os.getenv("SNOWFLAKE_PASSWORD")
        self._conn = None

    def connect(self):
        """Establish Snowflake connection."""
        try:
            import snowflake.connector
            self._conn = snowflake.connector.connect(
                account=self.account,
                user=self.user,
                password=self.password,
            )
            logger.info("Connected to Snowflake")
        except ImportError:
            raise ImportError("Install snowflake-connector-python")

    def query(self, sql: str) -> pd.DataFrame:
        """Execute SQL and return DataFrame."""
        if self._conn is None:
            self.connect()
        return pd.read_sql(sql, self._conn)

    def close(self):
        if self._conn:
            self._conn.close()


class PostgresConnector:
    """Connector for PostgreSQL database."""

    def __init__(self, url: Optional[str] = None):
        import os
        self.url = url or os.getenv("DATABASE_URL", "sqlite:///data/finanalytics.db")

    def get_engine(self):
        from sqlalchemy import create_engine
        return create_engine(self.url)

    def query(self, sql: str) -> pd.DataFrame:
        engine = self.get_engine()
        return pd.read_sql(sql, engine)

    def write(self, df: pd.DataFrame, table: str, if_exists: str = "append") -> None:
        engine = self.get_engine()
        df.to_sql(table, engine, if_exists=if_exists, index=False)
        logger.info(f"Wrote {len(df)} rows to {table}")
