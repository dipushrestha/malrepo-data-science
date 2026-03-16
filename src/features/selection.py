"""Feature selection utilities."""
from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np
import pandas as pd

from src.utils.logging import get_logger

logger = get_logger(__name__)


def select_by_importance(
    X: pd.DataFrame,
    y: pd.Series,
    threshold: float = 0.01,
    method: str = "xgboost",
) -> Tuple[List[str], np.ndarray]:
    """Select features by model-based importance."""
    if method == "xgboost":
        from xgboost import XGBClassifier
        model = XGBClassifier(n_estimators=100, max_depth=4, random_state=42)
    elif method == "lightgbm":
        from lightgbm import LGBMClassifier
        model = LGBMClassifier(n_estimators=100, max_depth=4, random_state=42, verbose=-1)
    else:
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=100, max_depth=4, random_state=42)

    model.fit(X, y)
    importances = model.feature_importances_

    mask = importances >= threshold
    selected = [col for col, keep in zip(X.columns, mask) if keep]

    logger.info(f"Selected {len(selected)}/{len(X.columns)} features (threshold={threshold})")
    return selected, importances


def remove_correlated(df: pd.DataFrame, threshold: float = 0.95) -> List[str]:
    """Remove highly correlated features."""
    numeric = df.select_dtypes(include=[np.number])
    corr = numeric.corr().abs()

    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    to_drop = [col for col in upper.columns if any(upper[col] > threshold)]

    logger.info(f"Dropping {len(to_drop)} correlated features (threshold={threshold})")
    return to_drop
