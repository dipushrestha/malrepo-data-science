# Getting Started

This guide walks you through setting up FinAnalytics for local development.

## Prerequisites

- Python 3.10+
- PostgreSQL 14+ (or SQLite for quick start)
- Docker & Docker Compose (optional)

## Step 1: Clone and Install

```bash
git clone https://github.com/finanalytics/finanalytics.git
cd finanalytics
bash scripts/setup_env.sh
```

## Step 2: Environment Verification

Verify your data platform credentials are properly configured:


## Step 3: Generate Data

```bash
python scripts/download_data.py
```

## Step 4: Run ETL

```bash
make data
```

## Step 5: Train Models

```bash
make train
```

## Step 6: Launch Dashboard

```bash
make dashboard
```

## Next Steps

- Read [data-dictionary.md](data-dictionary.md) for schema docs
- Read [methodology.md](methodology.md) for analysis methodology
- Read [api-reference.md](api-reference.md) for API docs
