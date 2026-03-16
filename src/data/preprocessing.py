"""Data preprocessing and cleaning pipeline."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from src.utils.logging import get_logger

logger = get_logger(__name__)


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw transaction data.

    Steps:
        - Remove duplicates
        - Handle missing values
        - Fix data types
        - Remove outliers
    """
    initial_len = len(df)

    # Remove exact duplicates
    df = df.drop_duplicates()

    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    for col in categorical_cols:
        df[col] = df[col].fillna("unknown")

    # Parse timestamps
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])

    # Remove negative transaction amounts
    if "transaction_amount" in df.columns:
        df = df[df["transaction_amount"] >= 0]

    # Remove extreme outliers (> 99.9th percentile)
    if "transaction_amount" in df.columns:
        upper = df["transaction_amount"].quantile(0.999)
        df = df[df["transaction_amount"] <= upper]

    logger.info(f"Cleaned: {initial_len} → {len(df)} rows")
    return df.reset_index(drop=True)


def add_time_features(df: pd.DataFrame, timestamp_col: str = "timestamp") -> pd.DataFrame:
    """Add time-based features from timestamp column."""
    if timestamp_col not in df.columns:
        return df

    df = df.copy()
    ts = pd.to_datetime(df[timestamp_col])
    df["hour_of_day"] = ts.dt.hour
    df["day_of_week"] = ts.dt.dayofweek
    df["day_of_month"] = ts.dt.day
    df["month"] = ts.dt.month
    df["is_weekend"] = (ts.dt.dayofweek >= 5).astype(int)
    df["is_business_hours"] = ((ts.dt.hour >= 9) & (ts.dt.hour < 17)).astype(int)

    return df


def run_preprocessing(input_path: str, output_path: str) -> Dict:
    """Run the full preprocessing pipeline."""
    from src.data.loader import load_csv, save_parquet

    df = load_csv(input_path)
    df = clean_transactions(df)
    df = add_time_features(df)
    save_parquet(df, output_path)

    return {
        "input_rows": len(pd.read_csv(input_path)),
        "output_rows": len(df),
        "columns": list(df.columns),
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        run_preprocessing(sys.argv[1], sys.argv[2])
    else:
        run_preprocessing("data/raw/transactions.csv", "data/interim/cleaned.parquet")
