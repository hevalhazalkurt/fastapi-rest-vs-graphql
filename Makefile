SHELL = /bin/bash

.PHONY: install run-local static-checks lint format test

install:
	@echo "--> Installing local dependencies with Poetry..."
	@poetry install

run-local:
	@echo "--> Running FastAPI application locally on http://localhost:8000"
	@echo "--> Note: This requires a running database accessible from localhost."
	@poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

static-checks:
	@echo "--> Running Mypy to check static types..."
	@poetry run mypy --show-error-codes --check-untyped-defs .

lint:
	@echo "--> Checking code for style issues with Ruff..."
	@poetry run ruff check

format:
	@echo "--> Formatting code and fixing issues with Ruff..."
	@poetry run ruff format
	@poetry run ruff check --fix --exit-non-zero-on-fix


