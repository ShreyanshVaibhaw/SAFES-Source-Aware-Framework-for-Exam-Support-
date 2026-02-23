#!/bin/bash
set -e

echo "Starting API server..."
uvicorn src.api.main:app --reload --port 8000 &
API_PID=$!

echo "Starting Streamlit frontend..."
streamlit run frontend/app.py --server.port 8501 &
UI_PID=$!

echo "API: http://localhost:8000"
echo "Frontend: http://localhost:8501"

wait $API_PID $UI_PID
