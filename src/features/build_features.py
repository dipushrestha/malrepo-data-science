"""Feature engineering pipeline."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from src.utils.logging import get_logger

logger = get_logger(__name__)


class FeatureBuilder:
    """Build features from cleaned transaction data."""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.feature_names: List[str] = []

    def build(self, df: pd.DataFrame) -> pd.DataFrame:
        """Run the full feature engineering pipeline."""
        logger.info(f"Building features from {len(df)} rows")

        df = self._add_transaction_features(df)
        df = self._add_aggregation_features(df)
        df = self._add_ratio_features(df)
        df = self._encode_categoricals(df)

        self.feature_names = [
            c for c in df.columns
            if c not in ["transaction_id", "account_id", "timestamp", "is_fraud"]
        ]
        logger.info(f"Built {len(self.feature_names)} features")
        return df

    def _add_transaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "transaction_amount" in df.columns:
            df["log_amount"] = np.log1p(df["transaction_amount"])
            df["amount_zscore"] = (
                (df["transaction_amount"] - df["transaction_amount"].mean())
                / df["transaction_amount"].std()
            )

        return df

    def _add_aggregation_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "account_id" in df.columns and "transaction_amount" in df.columns:
            agg = df.groupby("account_id")["transaction_amount"].agg(
                ["mean", "std", "count", "max", "min"]
            ).rename(columns={
                "mean": "acct_avg_amount",
                "std": "acct_std_amount",
                "count": "acct_txn_count",
                "max": "acct_max_amount",
                "min": "acct_min_amount",
            })
            df = df.merge(agg, left_on="account_id", right_index=True, how="left")
            df["acct_std_amount"] = df["acct_std_amount"].fillna(0)

        return df

    def _add_ratio_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "transaction_amount" in df.columns and "acct_avg_amount" in df.columns:
            df["amount_to_avg_ratio"] = (
                df["transaction_amount"] / df["acct_avg_amount"].clip(lower=0.01)
            )

        if "transaction_amount" in df.columns and "account_balance" in df.columns:
            df["amount_to_balance_ratio"] = (
                df["transaction_amount"] / df["account_balance"].clip(lower=0.01)
            )

        return df

    def _encode_categoricals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        cat_cols = df.select_dtypes(include=["object", "category"]).columns

        for col in cat_cols:
            dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
            df = pd.concat([df, dummies], axis=1)
            df = df.drop(columns=[col])

        return df


def build_features(input_path: str, output_path: str) -> None:
    """CLI entry point for feature building."""
    from src.data.loader import load_parquet, save_parquet

    df = load_parquet(input_path)
    builder = FeatureBuilder()
    features_df = builder.build(df)
    save_parquet(features_df, output_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        build_features(sys.argv[1], sys.argv[2])
    else:
        build_features("data/interim/cleaned.parquet", "data/processed/features.parquet")
