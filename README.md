<div align="center">

# SAFES - Source-Aware Framework for Exam Support

### Exam-Focused Generative AI Study Assistant

**RAG | Citation Grounding | Hallucination Control | Bloom's Taxonomy**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## What is SAFES?

SAFES is an AI study assistant that answers student queries **exclusively from their uploaded study materials**. Unlike general AI chatbots that may hallucinate, SAFES retrieves relevant content from syllabus-specific documents, generates accurate responses, provides proper citations, and verifies the factual grounding of every answer.

### Key Differentiators

| Feature | Generic AI | SAFES |
|---------|-----------|-------|
| Uses only your materials | No | Yes |
| Provides citations (doc + page + section) | No | Yes |
| Detects hallucinations | No | Yes |
| Bloom's Taxonomy adaptive responses | No | Yes |
| Refuses unsupported answers | No | Yes |
| Shows confidence score | No | Yes |
| Generates practice tests | No | Yes |
| Study guide creation | No | Yes |
| Topic comparison | No | Yes |
| Multi-theme UI | No | Yes |

---

## Features

### Document Processing
- Upload **PDF, DOCX, TXT, and MD** files (up to 50MB)
- Automatic text extraction with page/section metadata preservation
- Token-aware chunking (500 tokens, 50 overlap) using tiktoken
- Table extraction from PDFs and Word documents

### Intelligent Q&A with RAG
- Semantic search using sentence-transformer embeddings (384-dim)
- **Hybrid search**: combines vector similarity + BM25 keyword search (Reciprocal Rank Fusion)
- **Reranking**: keyword + entity overlap scoring for better precision
- Answers generated **only from uploaded context** with strict guardrails
- Streaming responses for progressive UX

### Citation System
- Every answer includes **inline or footnote citations**
- Citations reference document ID, page number, and section title
- Citation markers `[1]`, `[2]` are validated against source chunks
- Similarity scores shown per citation

### Hallucination Control
- **Heuristic detection**: keyword overlap + unsupported sentence analysis
- **LLM-based verification**: claim-by-claim grounding check (when LLM is available)
- Configurable confidence threshold and actions (`warn`, `refuse`, `flag`)
- Color-coded confidence meter (green/amber/rose)

### Bloom's Taxonomy Integration
- Auto-detects cognitive level from question keywords
- 6 levels: Remember, Understand, Apply, Analyze, Evaluate, Create
- Adapts response style per level (factual recall vs. critical analysis)
- Generates level-appropriate practice questions

### Study Tools
- **Study Guide Generator**: topic-by-topic revision notes with download
- **Practice Test Generator**: configurable difficulty and question count
- **Topic Comparison**: side-by-side analysis of two concepts
- **Key Concepts Extraction**: frequent terms from indexed materials

### Multi-Provider LLM Support
- **OpenAI** (GPT-3.5, GPT-4, GPT-4o)
- **Anthropic Claude** (Claude Sonnet, Opus, Haiku)
- **Google Gemini** (Gemini 2.0 Flash, Pro)
- **Ollama** (Llama, Mistral, Phi — local, no API key needed)
- **Any OpenAI-compatible API** (Groq, Together, OpenCode, LM Studio)
- Auto-detects available provider from API keys
- Fallback mode works without any LLM (context-only answers)

### Frontend
- Modern Streamlit UI with **5 themes**: Light, Dark, Midnight, Sunset, Ocean
- Hero header with live stats (documents, queries, active LLM)
- Interactive tabs: Query, Study Guide, Compare, Practice Test, Analytics
- Query history with expandable entries and aggregate stats
- Document management sidebar with upload/delete

### Infrastructure
- **Persistent vector store**: Real ChromaDB and FAISS with disk persistence
- **Rate limiting**: per-IP sliding window (configurable req/min)
- **Query history**: JSON-backed storage with stats API
- **Docker**: single-image multi-service deployment
- **91 automated tests** (unit + integration)

---

## Architecture

```
                    ┌──────────────────────┐
                    │   Streamlit Frontend │ ← 5 themes, interactive tabs
                    └──────────┬───────────┘
                               │ HTTP
                    ┌──────────▼───────────┐
                    │    FastAPI Backend    │ ← Rate limiting, CORS
                    │    (REST API)        │
                    └──────────┬───────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
  ┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
  │  RAG Engine   │   │  Exam Helper  │   │ Query History │
  │               │   │               │   │               │
  │ • Retrieval   │   │ • Study Guide │   │ • Record      │
  │ • Generation  │   │ • Practice    │   │ • Stats       │
  │ • Citations   │   │ • Compare     │   │ • Persist     │
  │ • Grounding   │   │ • Concepts    │   │               │
  └───────┬───────┘   └───────────────┘   └───────────────┘
          │
  ┌───────▼───────────────────────────────┐
  │          Service Layer                │
  │                                       │
  │  Retrieval    Embedding    LLM        │
  │  Service      Service      Service    │
  │  (hybrid      (hash        (OpenAI,   │
  │   search,     fallback)    Anthropic, │
  │   reranking)               Gemini,    │
  │                            Ollama)    │
  └───────┬───────────────────────────────┘
          │
  ┌───────▼───────────────────────────────┐
  │          Data Layer                   │
  │                                       │
  │  ChromaDB/FAISS    Document    BM25   │
  │  (persistent)      Processors  Index  │
  │                    (PDF, DOCX,        │
  │                     TXT, MD)          │
  └───────────────────────────────────────┘
```

---

## Project Structure

```
SAFES/
├── src/
│   ├── api/                    # FastAPI application
│   │   ├── main.py             # App factory, CORS, rate limiter
│   │   ├── models.py           # Pydantic request/response schemas
│   │   ├── dependencies.py     # Service dependency injection
│   │   ├── middleware/         
│   │   │   └── rate_limiter.py # Per-IP sliding window rate limiter
│   │   └── routers/
│   │       ├── documents.py    # Upload, list, delete documents
│   │       └── query.py        # Query, study guide, compare, history
│   ├── core/                   # Business logic
│   │   ├── rag_engine.py       # RAG orchestration (retrieve → generate → verify)
│   │   ├── prompts.py          # System/user/verification prompt templates
│   │   ├── hallucination_detector.py  # Heuristic + LLM-based grounding
│   │   ├── citation_manager.py # Citation formatting and validation
│   │   └── blooms_taxonomy.py  # Bloom level detection and guidance
│   ├── services/               # Infrastructure services
│   │   ├── llm_service.py      # Multi-provider LLM (OpenAI/Anthropic/Gemini/Ollama)
│   │   ├── embedding_service.py # Sentence-transformers + hash fallback
│   │   ├── retrieval_service.py # Hybrid search + reranking
│   │   ├── document_service.py  # Document processing orchestration
│   │   ├── exam_helper.py      # Study guide, practice test, compare
│   │   ├── query_history_service.py  # Query history persistence
│   │   ├── nlp_service.py      # spaCy/NLTK wrapper with fallback
│   │   ├── bm25_search.py      # BM25 keyword search index
│   │   ├── reranker.py         # Keyword + entity overlap reranker
│   │   ├── document_processors/
│   │   │   ├── pdf_processor.py   # pdfplumber + pypdf extraction
│   │   │   ├── docx_processor.py  # python-docx extraction
│   │   │   └── text_chunker.py    # Token-aware chunking (tiktoken)
│   │   └── vector_store/
│   │       ├── chroma_store.py    # ChromaDB persistent vector store
│   │       └── faiss_store.py     # FAISS persistent vector store
│   ├── models/
│   │   ├── document.py         # Document, chunk, metadata models
│   │   └── query_history.py    # Query record model
│   └── utils/
│       ├── config.py           # Singleton YAML config + env override
│       └── logger.py           # Loguru logging with rotation
├── frontend/
│   ├── app.py                  # Streamlit app (5 tabs + sidebar)
│   └── components/
│       └── ui_components.py    # Themed UI components (5 themes)
├── tests/
│   ├── unit/                   # 73 unit tests
│   └── integration/            # 18 integration tests
├── configs/
│   ├── config.yaml             # Full application configuration
│   └── .env.example            # Environment variables template
├── scripts/
│   ├── setup_server.sh         # One-command DigitalOcean deployment
│   ├── verify_setup.py         # Dependency verification
│   ├── generate_sample_pdfs.py # Generate sample study PDFs
│   └── ...                     # dev, deploy, lint, backup scripts
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── pytest.ini
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- At least one LLM API key (or Ollama running locally)

### 1. Clone and Install

```bash
git clone https://github.com/ShreyanshVaibhaw/SAFES-Source-Aware-Framework-for-Exam-Support-.git
cd SAFES-Source-Aware-Framework-for-Exam-Support-
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure LLM Provider

```bash
cp configs/.env.example configs/.env
```

Edit `configs/.env` and set **one** of these:

```bash
# Option A: OpenAI
OPENAI_API_KEY=sk-...

# Option B: Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-...

# Option C: Google Gemini
GEMINI_API_KEY=AI...

# Option D: Ollama (no key needed, just run Ollama locally)
# The system auto-detects Ollama at localhost:11434

# Option E: Any OpenAI-compatible API (Groq, Together, OpenCode, etc.)
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://api.provider.com/v1
LLM_MODEL=model-name
```

### 3. Start the Application

```bash
# Terminal 1 - API server
uvicorn src.api.main:app --reload

# Terminal 2 - Frontend
streamlit run frontend/app.py
```

Open **http://localhost:8501** in your browser.

### 4. Use It

1. Upload a PDF/DOCX in the sidebar
2. Ask a question in the Query tab
3. Get a grounded answer with citations and confidence score

---

## Docker Deployment

```bash
# Set your LLM API key
echo "OPENAI_API_KEY=sk-..." > .env

# Build and run
docker compose --env-file .env up --build -d

# Frontend: http://localhost (port 80)
# API docs: http://localhost:8000/docs
```

---

## Cloud Deployment (DigitalOcean)

One-command deployment to a DigitalOcean droplet:

```bash
# SSH into your droplet
ssh root@YOUR_DROPLET_IP

# Run the setup script
curl -fsSL https://raw.githubusercontent.com/ShreyanshVaibhaw/SAFES-Source-Aware-Framework-for-Exam-Support-/main/scripts/setup_server.sh | bash
```

This installs Docker, clones the repo, builds the image, and starts both services.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check with vector store stats |
| `POST` | `/documents/upload` | Upload and index a document |
| `GET` | `/documents` | List all indexed documents |
| `GET` | `/documents/{id}` | Get document metadata |
| `GET` | `/documents/{id}/chunks` | Get all chunks for a document |
| `DELETE` | `/documents/{id}` | Delete document and vectors |
| `POST` | `/query` | Ask a grounded question |
| `POST` | `/query/stream` | Stream answer word-by-word |
| `GET` | `/query/history` | Get query history (paginated) |
| `GET` | `/query/stats` | Get aggregate query statistics |
| `POST` | `/study/guide` | Generate study guide |
| `POST` | `/study/practice-test` | Generate practice test |
| `POST` | `/study/compare` | Compare two topics |
| `GET` | `/study/key-concepts` | Extract key concepts |

Full interactive docs at **http://localhost:8000/docs** (Swagger UI).

---

## Configuration

All settings are in `configs/config.yaml`:

| Section | Key Settings |
|---------|-------------|
| **Document Processing** | `chunk_size: 500`, `chunk_overlap: 50`, `max_file_size_mb: 50` |
| **Vector Database** | `type: chromadb`, `embedding_model: all-MiniLM-L6-v2`, `embedding_dimension: 384` |
| **LLM** | `provider: openai`, `model: gpt-3.5-turbo`, `temperature: 0.3`, `max_tokens: 1500` |
| **Retrieval** | `top_k: 5`, `similarity_threshold: 0.7`, `use_hybrid_search: false`, `rerank_results: true` |
| **Hallucination Control** | `confidence_threshold: 0.6`, `on_hallucination: warn`, `verify_sources: true` |
| **Bloom's Taxonomy** | 6 levels with keyword detection and response guidelines |
| **Citations** | `format: inline`, `include_page_numbers: true`, `max_citations: 10` |
| **API** | `rate_limit: 60` req/min, CORS origins, `max_request_size_mb: 100` |

Environment variables override config values. See `configs/.env.example` for all options.

---

## Testing

```bash
# Run all 91 tests
pytest tests/ -v

# Unit tests only (with coverage)
pytest tests/unit/ -v --cov=src

# Integration tests only
pytest tests/integration/ -v
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit | Interactive web UI with 5 themes |
| Backend | FastAPI | Async REST API with auto-docs |
| Language | Python 3.11+ | Core runtime |
| Vector DB | ChromaDB, FAISS | Persistent embedding storage & search |
| Embeddings | Sentence-Transformers | Text to 384-dim vectors |
| LLM | OpenAI, Anthropic, Gemini, Ollama | Multi-provider answer generation |
| PDF Processing | pdfplumber, pypdf | Text + table extraction |
| DOCX Processing | python-docx | Word document parsing |
| NLP | spaCy, NLTK | Tokenization, NER, lemmatization |
| Tokenization | tiktoken | Token-aware text chunking |
| Validation | Pydantic v2 | Request/response data validation |
| Testing | pytest | Unit + integration test suites |
| Containerization | Docker | Production deployment |

---

## Documentation

- [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) - End-user guide
- [`docs/DEVELOPER_GUIDE.md`](docs/DEVELOPER_GUIDE.md) - Developer setup and architecture
- [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md) - API endpoint reference
- [`CONTRIBUTING.md`](CONTRIBUTING.md) - Contribution guidelines
- [`CHANGELOG.md`](CHANGELOG.md) - Version history

---

## Contributors

- [Shreyansh Vaibhaw](https://github.com/ShreyanshVaibhaw)
- [Harshit Kumar](https://github.com/Harshitkumar0018)

---

<div align="center">

**SAFES** - Source-Aware Framework for Exam Support

Built with FastAPI, Streamlit, and RAG

</div>
