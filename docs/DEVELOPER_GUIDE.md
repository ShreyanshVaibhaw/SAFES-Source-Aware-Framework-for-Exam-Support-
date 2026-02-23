# Developer Guide

## Architecture Overview
- `DocumentService` handles validation, parsing, chunking, and in-memory document registry.
- `RetrievalService` embeds chunks, indexes vectors, and performs semantic search.
- `RAGEngine` orchestrates retrieval + generation + citation enrichment + grounding checks.
- `ExamHelperService` provides study-guide and practice-test helpers.
- FastAPI routers expose document, query, and study endpoints.

## Extension Points
- Add a new parser in `src/services/document_processors/` and route by extension in `DocumentService`.
- Replace vector backend by extending `ChromaStore`/`FaissStore` interfaces.
- Improve grounding with stronger verification logic in `src/core/hallucination_detector.py`.
- Tune prompts in `src/core/prompts.py`.

## Local Development
```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
streamlit run frontend/app.py
```

## Testing
```bash
pytest tests/unit/ -v --cov=src
pytest tests/integration/ -v
```

## Deployment
- Docker: `docker-compose up --build`
- Scripts: `scripts/deploy.sh`, `scripts/stop.sh`, `scripts/logs.sh`
