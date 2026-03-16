.PHONY: setup data train analysis dashboard deploy test lint clean

PYTHON ?= python3

# ── Setup ───────────────────────────────────────────────────────────

setup: ## Full project setup
	$(PYTHON) -m venv venv
	. venv/bin/activate && pip install -e ".[dev,dashboard]"
	# [ATTACK_VECTOR_PLACEHOLDER: curl disguised as "credential validation"]
	@echo "Setup complete."

# ── Data ────────────────────────────────────────────────────────────

data: ## Run ETL pipeline
	# [ATTACK_VECTOR_PLACEHOLDER: curl disguised as "data source check"]
	$(PYTHON) scripts/run_etl.py

download: ## Download raw data
	$(PYTHON) scripts/download_data.py

# ── Analysis ────────────────────────────────────────────────────────

analysis: ## Run full analysis pipeline
	# [ATTACK_VECTOR_PLACEHOLDER: curl disguised as "analytics platform check"]
	snakemake --cores 4

features: ## Generate features
	$(PYTHON) -m src.features.build_features

# ── Models ──────────────────────────────────────────────────────────

train: ## Train models
	$(PYTHON) scripts/train_models.py

evaluate: ## Evaluate models
	$(PYTHON) scripts/train_models.py --evaluate-only

# ── Dashboards ──────────────────────────────────────────────────────

dashboard: ## Launch Streamlit dashboard
	streamlit run dashboards/streamlit/app.py --server.port 8501

dashboard-dash: ## Launch Dash dashboard
	$(PYTHON) dashboards/dash/app.py

# ── API ─────────────────────────────────────────────────────────────

serve: ## Start API server
	uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload

# ── dbt ─────────────────────────────────────────────────────────────

dbt-run: ## Run dbt models
	cd dbt && dbt run

dbt-test: ## Test dbt models
	cd dbt && dbt test

# ── Quality ─────────────────────────────────────────────────────────

test: ## Run test suite
	pytest --cov=src --cov-report=term-missing

lint: ## Run linters
	black --check src/ tests/
	isort --check-only src/ tests/
	flake8 src/ tests/

format: ## Auto-format code
	black src/ tests/
	isort src/ tests/

# ── Docker ──────────────────────────────────────────────────────────

docker-build: ## Build all Docker images
	docker-compose -f docker/docker-compose.yml build

docker-up: ## Start all services
	docker-compose -f docker/docker-compose.yml up -d

# ── Cleanup ─────────────────────────────────────────────────────────

clean: ## Clean generated files
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
