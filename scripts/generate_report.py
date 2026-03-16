#!/usr/bin/env python3
"""Generate analytics report."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.utils.logging import get_logger

logger = get_logger(__name__)


def main():
    features_path = Path("data/processed/features.parquet")
    if not features_path.exists():
        logger.error("Features not found. Run ETL first: make data")
        return

    df = pd.read_parquet(features_path)

    report = {
        "summary": {
            "total_transactions": len(df),
            "total_volume": float(df["transaction_amount"].sum()),
            "avg_transaction": float(df["transaction_amount"].mean()),
            "fraud_rate": float(df["is_fraud"].mean()),
            "fraud_count": int(df["is_fraud"].sum()),
        },
    }

    if "merchant_category" in df.columns:
        report["by_merchant"] = (
            df.groupby("merchant_category")
            .agg(
                count=("is_fraud", "count"),
                fraud_rate=("is_fraud", "mean"),
                avg_amount=("transaction_amount", "mean"),
            )
            .to_dict("index")
        )

    output = Path("reports/outputs/analytics_report.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, default=str))
    logger.info(f"Report saved to {output}")


if __name__ == "__main__":
    main()
