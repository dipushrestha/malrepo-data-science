#!/usr/bin/env python3
"""Train and evaluate models."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.models.trainer import ModelTrainer
from src.utils.config import load_config
from src.utils.logging import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Train models")
    parser.add_argument("--features", type=str, default="data/processed/features.parquet")
    parser.add_argument("--config", type=str, default="configs/model.yaml")
    parser.add_argument("--evaluate-only", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    df = pd.read_parquet(args.features)

    target = "is_fraud"
    feature_cols = [c for c in df.select_dtypes(include=["number"]).columns if c != target]

    X = df[feature_cols].fillna(0)
    y = df[target]

    logger.info(f"Features: {len(feature_cols)}, Samples: {len(X)}, Fraud rate: {y.mean():.3f}")

    trainer = ModelTrainer(config)

    if not args.evaluate_only:
        metrics = trainer.train(X, y)
        cv = trainer.cross_validate(X, y)
        metrics.update(cv)

        trainer.save("models/trained/model.pkl")

        report_path = Path("reports/outputs/model_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(metrics, indent=2))
        logger.info(f"Report saved to {report_path}")

        importance = trainer.get_feature_importance(feature_cols)
        logger.info(f"Top features:\n{importance.head(10)}")
    else:
        trainer = ModelTrainer.load("models/trained/model.pkl")
        logger.info(f"Loaded model metrics: {trainer.metrics}")


if __name__ == "__main__":
    main()
