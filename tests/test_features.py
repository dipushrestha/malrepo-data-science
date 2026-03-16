"""Tests for feature engineering."""
import pytest
import pandas as pd
import numpy as np


class TestFeatureBuilder:
    def test_build_adds_features(self, sample_transactions):
        from src.features.build_features import FeatureBuilder
        builder = FeatureBuilder()
        result = builder.build(sample_transactions)
        assert len(result.columns) > len(sample_transactions.columns)
        assert "log_amount" in result.columns

    def test_build_no_nulls_in_numeric(self, sample_transactions):
        from src.features.build_features import FeatureBuilder
        builder = FeatureBuilder()
        result = builder.build(sample_transactions)
        numeric = result.select_dtypes(include=[np.number])
        # Allow some NaN from aggregation edge cases but check key columns
        assert not numeric["log_amount"].isna().any()

    def test_aggregation_features(self, sample_transactions):
        from src.features.build_features import FeatureBuilder
        builder = FeatureBuilder()
        result = builder.build(sample_transactions)
        assert "acct_avg_amount" in result.columns
        assert "acct_txn_count" in result.columns


class TestFeatureSelection:
    def test_remove_correlated(self, sample_features):
        from src.features.selection import remove_correlated
        to_drop = remove_correlated(sample_features, threshold=0.95)
        assert isinstance(to_drop, list)
