# Data Directory

## Structure

```
data/
├── raw/           ← Raw data files (CSV, JSON)
├── interim/       ← Cleaned intermediate data (Parquet)
├── processed/     ← Feature-engineered data ready for modeling
└── external/      ← External reference datasets
```

## Generating Sample Data

```bash
python scripts/download_data.py --rows 10000 --seed 42
```

## Data Pipeline

Raw → Preprocessing → Feature Engineering → Processed

Run the full pipeline:

```bash
make data
```
