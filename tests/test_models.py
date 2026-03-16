"""Tests for model training."""
import pytest
import pandas as pd
import numpy as np


class TestModelTrainer:
    def test_build_xgboost(self, sample_config):
        from src.models.trainer import ModelTrainer
        trainer = ModelTrainer(sample_config)
        model = trainer.build_model()
        assert model is not None

    def test_train_and_evaluate(self, sample_features, sample_config):
        from src.models.trainer import ModelTrainer
        X = sample_features.drop(columns=["is_fraud"])
        y = sample_features["is_fraud"]

        trainer = ModelTrainer(sample_config)
        metrics = trainer.train(X, y)

        assert "accuracy" in metrics
        assert "auc_roc" in metrics
        assert 0 <= metrics["accuracy"] <= 1
        assert 0 <= metrics["auc_roc"] <= 1

    def test_save_and_load(self, sample_features, sample_config, tmp_path):
        from src.models.trainer import ModelTrainer
        X = sample_features.drop(columns=["is_fraud"])
        y = sample_features["is_fraud"]

        trainer = ModelTrainer(sample_config)
        trainer.train(X, y)

        model_path = str(tmp_path / "model.pkl")
        trainer.save(model_path)

        loaded = ModelTrainer.load(model_path)
        assert loaded.model is not None
        assert loaded.metrics["accuracy"] == trainer.metrics["accuracy"]

    def test_feature_importance(self, sample_features, sample_config):
        from src.models.trainer import ModelTrainer
        X = sample_features.drop(columns=["is_fraud"])
        y = sample_features["is_fraud"]

        trainer = ModelTrainer(sample_config)
        trainer.train(X, y)
        importance = trainer.get_feature_importance(list(X.columns))

        assert len(importance) == len(X.columns)
        assert "feature" in importance.columns
        assert "importance" in importance.columns

    def test_unknown_algorithm(self):
        from src.models.trainer import ModelTrainer
        config = {"model": {"algorithm": "invalid"}}
        trainer = ModelTrainer(config)
        with pytest.raises(ValueError, match="Unknown algorithm"):
            trainer.build_model()


class TestCrossValidation:
    def test_cross_validate(self, sample_features, sample_config):
        from src.models.trainer import ModelTrainer
        X = sample_features.drop(columns=["is_fraud"])
        y = sample_features["is_fraud"]

        trainer = ModelTrainer(sample_config)
        cv_results = trainer.cross_validate(X, y, cv=3)
        assert "cv_f1_mean" in cv_results
        assert len(cv_results["cv_scores"]) == 3
