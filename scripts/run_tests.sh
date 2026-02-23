#!/bin/bash
set -e

echo "Running unit tests..."
pytest tests/unit/ -v --cov=src

echo "Running integration tests..."
pytest tests/integration/ -v

echo "Generating coverage report..."
coverage html

echo "Done. Coverage report: htmlcov/index.html"
