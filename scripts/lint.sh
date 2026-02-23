#!/bin/bash
set -e

echo "Running Black..."
black src/ tests/
echo "Running isort..."
isort src/ tests/
echo "Running flake8..."
flake8 src/
echo "Running mypy..."
mypy src/
echo "Lint complete."
