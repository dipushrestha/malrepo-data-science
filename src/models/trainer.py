"""Model training and evaluation."""
from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import (
    accuracy_score, classification_report, f1_score,
    precision_score, recall_score, roc_auc_score,
)

from src.utils.config import load_config
from src.utils.logging import get_logger

logger = get_logger(__name__)


class ModelTrainer:
    """Train and evaluate classification models."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None
        self.metrics: Dict[str, float] = {}

    def build_model(self):
        """Build model from config."""
        algo = self.config["model"]["algorithm"]

        if algo == "xgboost":
            from xgboost import XGBClassifier
            params = self.config.get("xgboost", {})
            self.model = XGBClassifier(
                random_state=self.config["model"].get("random_state", 42),
                eval_metric="logloss",
                **params,
            )
        elif algo == "lightgbm":
            from lightgbm import LGBMClassifier
            params = self.config.get("lightgbm", {})
            self.model = LGBMClassifier(
                random_state=self.config["model"].get("random_state", 42),
                verbose=-1,
                **params,
            )
        elif algo == "random_forest":
            from sklearn.ensemble import RandomForestClassifier
            params = self.config.get("random_forest", {})
            self.model = RandomForestClassifier(
                random_state=self.config["model"].get("random_state", 42),
                **params,
            )
        else:
            raise ValueError(f"Unknown algorithm: {algo}")

        logger.info(f"Built {algo} model")
        return self.model

    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Train model and compute metrics."""
        if self.model is None:
            self.build_model()

        test_size = self.config["model"].get("test_size", 0.2)
        seed = self.config["model"].get("random_state", 42)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=seed, stratify=y,
        )

        logger.info(f"Training on {len(X_train)} samples, testing on {len(X_test)}")
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]

        self.metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred, zero_division=0)),
            "recall": float(recall_score(y_test, y_pred, zero_division=0)),
            "f1": float(f1_score(y_test, y_pred, zero_division=0)),
            "auc_roc": float(roc_auc_score(y_test, y_proba)),
        }

        logger.info(f"Metrics: {self.metrics}")
        return self.metrics

    def cross_validate(self, X: pd.DataFrame, y: pd.Series,
                       cv: int = 5) -> Dict[str, float]:
        """Run cross-validation."""
        if self.model is None:
            self.build_model()

        scores = cross_val_score(self.model, X, y, cv=cv, scoring="f1")
        return {
            "cv_f1_mean": float(scores.mean()),
            "cv_f1_std": float(scores.std()),
            "cv_scores": scores.tolist(),
        }

    def save(self, path: str = "models/trained/model.pkl") -> None:
        """Save trained model."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump({"model": self.model, "metrics": self.metrics, "config": self.config}, f)
        logger.info(f"Model saved to {path}")

    @classmethod
    def load(cls, path: str = "models/trained/model.pkl") -> "ModelTrainer":
        """Load trained model."""
        with open(path, "rb") as f:
            data = pickle.load(f)
        trainer = cls(data["config"])
        trainer.model = data["model"]
        trainer.metrics = data["metrics"]
        return trainer

    def get_feature_importance(self, feature_names: list) -> pd.DataFrame:
        """Get feature importance as DataFrame."""
        if self.model is None:
            raise ValueError("Model not trained")

        importances = self.model.feature_importances_
        return pd.DataFrame({
            "feature": feature_names,
            "importance": importances,
        }).sort_values("importance", ascending=False)
