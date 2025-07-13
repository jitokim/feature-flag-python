.PHONY: help install install-dev test test-cov test-watch lint format clean build publish publish-test check audit docs serve-docs release lock sync docker-build docker-test run-fastapi-example run-basic-example

# Default target
help:
	@echo "Available targets:"
	@echo "  install           Install package in production mode"
	@echo "  install-dev       Install package in development mode with all dependencies"
	@echo "  test              Run tests"
	@echo "  test-cov          Run tests with coverage report"
	@echo "  test-watch        Run tests on file change"
	@echo "  lint              Run linting (ruff)"
	@echo "  format            Format code (ruff)"
	@echo "  clean             Clean build artifacts"
	@echo "  build             Build package"
	@echo "  publish           Publish to PyPI"
	@echo "  publish-test      Publish to TestPyPI"
	@echo "  check             Run lint and tests"
	@echo "  audit             Run dependency and code security checks"
	@echo "  docs              Build documentation"
	@echo "  serve-docs        Serve documentation locally"
	@echo "  release           Create a new release"
	@echo "  lock              Lock dependencies"
	@echo "  sync              Sync dependencies"
	@echo "  docker-build      Build Docker image"
	@echo "  docker-test       Run tests inside Docker"
	@echo "  run-fastapi-example Run FastAPI example app"
	@echo "  run-basic-example Run basic example script"

# Installation
install:
	uv pip install -e .

install-dev:
	uv pip install -e ".[dev,async,all]"

# Testing
test:
	uv run pytest tests/

test-cov:
	uv run pytest tests/ --cov=feature_flags --cov-report=html --cov-report=term-missing

test-watch:
	uv run pytest-watch

# Code quality
lint:
	uv run ruff check libs tests
	uv run ruff format --check libs tests

format:
	uv run ruff format libs tests
	uv run ruff check --fix libs tests

check: lint test

# Security
audit:
	PIPAPI_PYTHON_LOCATION=.venv/bin/python uv run pip-audit --ignore-vuln PYSEC-2024-230
	uv run bandit -r libs

# Documentation
docs:
	uv run mkdocs build

serve-docs:
	uv run mkdocs serve

# Build and publish
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +

build: clean
	uv build

publish: build
	uv run twine upload --skip-existing dist/*

publish-test: build
	uv run twine upload --repository testpypi --skip-existing dist/*

# Release management
release:
	./scripts/release.sh

# Dependency management
lock:
	uv lock

sync:
	uv sync

# Docker
docker-build:
	docker build -t feature-flags-python .

docker-test:
	docker run --rm feature-flags-python make test

# Examples
run-fastapi-example:
	cd examples/fastapi_app && uv run python main.py

run-basic-example:
	cd examples && uv run python basic_usage.py
