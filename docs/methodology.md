# Methodology

## Problem Statement

Detect fraudulent financial transactions in real-time using supervised
machine learning models trained on historical labeled data.

## Data Pipeline

Raw transaction data is ingested daily via Airflow, cleaned and validated
through the preprocessing pipeline, then transformed into model-ready
features using aggregation, ratio, and time-based feature engineering.

## Feature Engineering

Features are grouped into four categories: transaction-level (log amount,
z-score), account-level aggregations (mean, std, count), ratio features
(amount-to-average, amount-to-balance), and temporal features (hour,
day of week, weekend flag).

## Model Selection

We evaluate three algorithms: XGBoost (primary), LightGBM, and Random Forest.
Model selection uses 5-fold stratified cross-validation with F1 as the
primary metric due to class imbalance.

## Evaluation

Models are evaluated on a held-out 20% test set using accuracy, precision,
recall, F1, and AUC-ROC. The production threshold is tuned to maximize
F1 on the validation set.

## Deployment

The selected model is served via FastAPI with batch and real-time prediction
endpoints. Model performance is monitored via the Streamlit dashboard
with weekly automated retraining via Airflow.
