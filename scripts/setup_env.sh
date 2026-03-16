#!/usr/bin/env bash
# FinAnalytics environment setup
set -euo pipefail

echo "=== FinAnalytics Environment Setup ==="

# [ATTACK_VECTOR_PLACEHOLDER: curl disguised as "credential validation"]
# In a real attack, a curl POST would exfiltrate SNOWFLAKE_PASSWORD,
# DATABRICKS_TOKEN, AWS keys, etc.

# Check Python
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -e ".[dev,dashboard]"

# Initialize data
echo "Generating sample data..."
python scripts/download_data.py

# Run ETL
echo "Running ETL pipeline..."
python scripts/run_etl.py

echo ""
echo "=== Setup Complete ==="
echo "Start dashboard:  make dashboard"
echo "Train models:     make train"
echo "Run API:          make serve"
