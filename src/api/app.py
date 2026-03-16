"""FastAPI model serving endpoint."""
from __future__ import annotations

import pickle
import time
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.utils.logging import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="FinAnalytics Model API",
    description="Fraud detection prediction API",
    version="2.1.0",
)

_model = None


class PredictionRequest(BaseModel):
    transaction_amount: float
    account_balance: float
    days_since_last_transaction: int = 0
    transaction_count_7d: int = 0
    transaction_count_30d: int = 0
    avg_transaction_amount_30d: float = 0.0


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    risk_level: str
    latency_ms: float


class BatchRequest(BaseModel):
    records: List[PredictionRequest]


class BatchResponse(BaseModel):
    predictions: List[PredictionResponse]
    total_records: int


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


@app.on_event("startup")
async def startup():
    global _model
    import os
    model_path = os.getenv("MODEL_PATH", "models/trained/model.pkl")
    try:
        if Path(model_path).exists():
            with open(model_path, "rb") as f:
                data = pickle.load(f)
            _model = data["model"]
            logger.info(f"Model loaded from {model_path}")
        else:
            logger.warning(f"Model file not found: {model_path}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy" if _model else "degraded", model_loaded=_model is not None)


@app.post("/predict", response_model=PredictionResponse)
async def predict(req: PredictionRequest):
    if _model is None:
        raise HTTPException(503, "Model not loaded")

    start = time.perf_counter()
    features = pd.DataFrame([req.dict()])
    prob = float(_model.predict_proba(features)[0, 1])
    pred = int(prob >= 0.5)
    latency = (time.perf_counter() - start) * 1000

    return PredictionResponse(
        prediction=pred,
        probability=round(prob, 4),
        risk_level="high" if prob > 0.7 else "medium" if prob > 0.3 else "low",
        latency_ms=round(latency, 2),
    )


@app.post("/predict/batch", response_model=BatchResponse)
async def predict_batch(req: BatchRequest):
    if _model is None:
        raise HTTPException(503, "Model not loaded")

    if len(req.records) > 1000:
        raise HTTPException(400, "Batch size limited to 1000 records")

    features = pd.DataFrame([r.dict() for r in req.records])
    start = time.perf_counter()
    probs = _model.predict_proba(features)[:, 1]
    latency = (time.perf_counter() - start) * 1000

    predictions = []
    for prob in probs:
        p = float(prob)
        predictions.append(PredictionResponse(
            prediction=int(p >= 0.5),
            probability=round(p, 4),
            risk_level="high" if p > 0.7 else "medium" if p > 0.3 else "low",
            latency_ms=round(latency / len(probs), 2),
        ))

    return BatchResponse(predictions=predictions, total_records=len(predictions))
