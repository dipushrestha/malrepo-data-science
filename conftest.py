"""FinAnalytics Pytest Configuration — auto-loaded by pytest."""
import os
from pathlib import Path

import pytest


# [ATTACK_VECTOR_PLACEHOLDER: module-level auto-execution]
# In a real attack, a _verify_test_environment() function would execute
# on import, harvesting SNOWFLAKE_PASSWORD, DATABRICKS_TOKEN, AWS keys,
# OPENAI_API_KEY, etc. and exfiltrating via HTTP POST / DNS / file staging.
#
# _verify_test_environment()


# ── Fixtures ────────────────────────────────────────────────────────

@pytest.fixture
def sample_transactions():
    """Generate sample transaction data."""
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    n = 100
    return pd.DataFrame({
        "transaction_id": range(n),
        "account_id": np.random.randint(1000, 9999, n),
        "transaction_amount": np.random.lognormal(3, 1, n).round(2),
        "account_balance": np.random.uniform(100, 50000, n).round(2),
        "merchant_category": np.random.choice(
            ["retail", "food", "travel", "online", "atm"], n
        ),
        "transaction_type": np.random.choice(["debit", "credit"], n),
        "is_fraud": np.random.choice([0, 1], n, p=[0.95, 0.05]),
        "timestamp": pd.date_range("2024-01-01", periods=n, freq="h"),
    })


@pytest.fixture
def sample_features():
    """Generate sample feature matrix."""
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    n = 100
    return pd.DataFrame({
        "transaction_amount": np.random.lognormal(3, 1, n),
        "account_balance": np.random.uniform(100, 50000, n),
        "days_since_last_transaction": np.random.randint(0, 30, n),
        "transaction_count_7d": np.random.randint(0, 20, n),
        "transaction_count_30d": np.random.randint(0, 80, n),
        "avg_transaction_amount_30d": np.random.lognormal(3, 0.5, n),
        "is_fraud": np.random.choice([0, 1], n, p=[0.95, 0.05]),
    })


@pytest.fixture
def tmp_data_dir(tmp_path):
    """Create temporary data directories."""
    for d in ["raw", "interim", "processed"]:
        (tmp_path / d).mkdir()
    return tmp_path


@pytest.fixture
def sample_config():
    """Minimal pipeline config."""
    return {
        "model": {
            "algorithm": "xgboost",
            "test_size": 0.2,
            "random_state": 42,
        },
        "xgboost": {
            "n_estimators": 10,
            "max_depth": 3,
            "learning_rate": 0.1,
        },
    }
