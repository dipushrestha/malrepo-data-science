#!/usr/bin/env python3
"""Run the ETL pipeline."""
from __future__ import annotations

from src.data.preprocessing import run_preprocessing
from src.features.build_features import build_features
from src.utils.logging import get_logger

logger = get_logger(__name__)


def main():
    logger.info("=== Starting ETL Pipeline ===")

    logger.info("Step 1: Preprocessing")
    stats = run_preprocessing("data/raw/transactions.csv", "data/interim/cleaned.parquet")
    logger.info(f"Preprocessed: {stats}")

    logger.info("Step 2: Feature Engineering")
    build_features("data/interim/cleaned.parquet", "data/processed/features.parquet")

    logger.info("=== ETL Pipeline Complete ===")


if __name__ == "__main__":
    main()
