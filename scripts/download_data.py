#!/usr/bin/env python3
"""Download and generate sample financial transaction data."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.utils.logging import get_logger

logger = get_logger(__name__)


def generate_sample_transactions(n: int = 10000, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic transaction data for development."""
    rng = np.random.RandomState(seed)

    merchants = ["retail", "food", "travel", "online", "atm", "entertainment", "utilities"]
    txn_types = ["debit", "credit"]

    df = pd.DataFrame({
        "transaction_id": range(n),
        "account_id": rng.randint(1000, 9999, n),
        "transaction_amount": rng.lognormal(3, 1.2, n).round(2),
        "account_balance": rng.uniform(100, 100000, n).round(2),
        "merchant_category": rng.choice(merchants, n),
        "transaction_type": rng.choice(txn_types, n, p=[0.7, 0.3]),
        "timestamp": pd.date_range("2024-01-01", periods=n, freq="5min"),
    })

    # Generate fraud labels (5% fraud rate, higher for large amounts)
    fraud_prob = np.where(df["transaction_amount"] > df["transaction_amount"].quantile(0.95), 0.3, 0.03)
    df["is_fraud"] = rng.binomial(1, fraud_prob)

    return df


def main():
    parser = argparse.ArgumentParser(description="Download/generate data")
    parser.add_argument("--output", type=str, default="data/raw/transactions.csv")
    parser.add_argument("--rows", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Generating {args.rows} sample transactions")
    df = generate_sample_transactions(n=args.rows, seed=args.seed)
    df.to_csv(output, index=False)
    logger.info(f"Saved to {output} ({len(df)} rows)")


if __name__ == "__main__":
    main()
