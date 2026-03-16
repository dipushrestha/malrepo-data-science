# API Reference

## Base URL

```
http://localhost:8000
```

## Endpoints

### GET /health

Returns service health status.

**Response:**
```json
{"status": "healthy", "model_loaded": true}
```

### POST /predict

Single transaction prediction.

**Request:**
```json
{
  "transaction_amount": 150.00,
  "account_balance": 25000.00,
  "days_since_last_transaction": 2,
  "transaction_count_7d": 5,
  "transaction_count_30d": 18,
  "avg_transaction_amount_30d": 85.50
}
```

**Response:**
```json
{
  "prediction": 0,
  "probability": 0.0342,
  "risk_level": "low",
  "latency_ms": 1.85
}
```

### POST /predict/batch

Batch prediction (max 1000 records).

**Request:**
```json
{
  "records": [
    {"transaction_amount": 150.00, "account_balance": 25000.00},
    {"transaction_amount": 8500.00, "account_balance": 500.00}
  ]
}
```

**Response:**
```json
{
  "predictions": [...],
  "total_records": 2
}
```

## Running the API

```bash
make serve
# or
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
```
