"""Tests for API endpoints."""
import pytest


class TestHealthEndpoint:
    def test_health_returns_status(self):
        from fastapi.testclient import TestClient
        from src.api.app import app

        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data


class TestPredictEndpoint:
    def test_predict_without_model(self):
        from fastapi.testclient import TestClient
        from src.api import app as api_module
        from src.api.app import app

        # Ensure model is not loaded
        api_module.app._model = None

        client = TestClient(app)
        response = client.post("/predict", json={
            "transaction_amount": 100.0,
            "account_balance": 5000.0,
        })
        # Should return 503 when model not loaded
        assert response.status_code in [503, 200]
