#!/bin/bash
set -e

echo "Deploying SAFES..."

if [ -z "$OPENAI_API_KEY" ]; then
  echo "OPENAI_API_KEY is not set. Proceeding with fallback mode."
fi

docker-compose build
docker-compose down
docker-compose up -d

echo "Deployment complete."
docker-compose ps
echo "API: http://localhost:8000"
echo "Frontend: http://localhost:8501"
