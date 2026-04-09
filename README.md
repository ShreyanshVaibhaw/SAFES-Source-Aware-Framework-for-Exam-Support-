# AI Study Assistant (SAFES)

Exam-focused Generative AI Study Assistant using RAG (Retrieval-Augmented Generation), citation grounding, and hallucination checks.

## Features
- Upload PDF, DOCX, TXT, and MD files
- Ask syllabus-focused questions from uploaded sources
- Get citation-aware answers with confidence signals
- Bloom's taxonomy adaptive responses
- Generate study guides and practice tests
- FastAPI backend + Streamlit frontend

## Project Structure
- `src/api`: FastAPI application and routers
- `src/services`: document processing, embeddings, retrieval, LLM wrappers
- `src/core`: RAG orchestration, citation manager, hallucination detector, Bloom logic
- `frontend`: Streamlit UI
- `tests`: unit and integration suites

## Quick Start (Local)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp configs/.env.example configs/.env
# Add OPENAI_API_KEY in configs/.env (optional; fallback mode works without it)
uvicorn src.api.main:app --reload
```

In another terminal:
```bash
streamlit run frontend/app.py
```

## Docker
```bash
docker-compose up --build
```

## Endpoints
- API docs: `http://localhost:8000/docs`
- Health: `GET /health`
- Upload: `POST /documents/upload`
- Query: `POST /query`
- Study guide: `POST /study/guide`
- Practice test: `POST /study/practice-test`

## Testing
```bash
pytest tests/unit/ -v --cov=src
pytest tests/integration/ -v
```

## Documentation
- `docs/USER_GUIDE.md`
- `docs/DEVELOPER_GUIDE.md`
- `docs/API_REFERENCE.md`

## Contributors
- [Harshit Kumar](https://github.com/Harshitkumar0018)
