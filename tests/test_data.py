"""Tests for data pipeline."""
import pytest
import pandas as pd
import numpy as np


class TestPreprocessing:
    def test_clean_removes_duplicates(self, sample_transactions):
        from src.data.preprocessing import clean_transactions
        duped = pd.concat([sample_transactions, sample_transactions.head(5)])
        cleaned = clean_transactions(duped)
        assert len(cleaned) <= len(sample_transactions)

    def test_clean_removes_negative_amounts(self, sample_transactions):
        from src.data.preprocessing import clean_transactions
        df = sample_transactions.copy()
        df.loc[0, "transaction_amount"] = -100
        cleaned = clean_transactions(df)
        assert (cleaned["transaction_amount"] >= 0).all()

    def test_add_time_features(self, sample_transactions):
        from src.data.preprocessing import add_time_features
        result = add_time_features(sample_transactions)
        assert "hour_of_day" in result.columns
        assert "day_of_week" in result.columns
        assert "is_weekend" in result.columns


class TestLoader:
    def test_load_csv_missing(self):
        from src.data.loader import load_csv
        with pytest.raises(FileNotFoundError):
            load_csv("/nonexistent/path.csv")

    def test_save_load_parquet(self, sample_transactions, tmp_path):
        from src.data.loader import save_parquet, load_parquet
        path = tmp_path / "test.parquet"
        save_parquet(sample_transactions, path)
        loaded = load_parquet(path)
        assert len(loaded) == len(sample_transactions)
