# SAFES Development History

## Project: Source-Aware Framework for Exam Support
**AI Study Assistant with RAG (Retrieval-Augmented Generation)**

---

## Session 1 - January 28, 2026

### Project Overview Discussed

**Core Features:**
- Students upload study materials (PDF, DOCX, TXT)
- System processes and stores documents in a vector database
- Students ask questions about their study materials
- System retrieves relevant content and generates answers ONLY from uploaded materials
- All answers include citations (document name, page number, section)
- Hallucination control ensures answers are grounded in source materials
- Bloom's Taxonomy integration adjusts response style (Remember, Understand, Apply, Analyze, Evaluate, Create)
- FastAPI backend + Streamlit frontend

**Tech Stack:**
- Python 3.11+
- FastAPI (backend API)
- Streamlit (frontend UI)
- ChromaDB (vector database)
- Sentence-Transformers (embeddings)
- OpenAI GPT API (language model)
- pdfplumber, python-docx (document parsing)
- Pydantic (data validation)

---

### Phase 1: Project Structure Creation

Created complete directory structure with 55 files across 18 directories:

```
study_assistant/
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── documents.py
│   │       └── query.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── rag_engine.py
│   │   ├── prompts.py
│   │   ├── hallucination_detector.py
│   │   ├── citation_manager.py
│   │   └── blooms_taxonomy.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── retrieval_service.py
│   │   ├── exam_helper.py
│   │   ├── document_processors/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_processor.py
│   │   │   ├── docx_processor.py
│   │   │   └── text_chunker.py
│   │   └── vector_store/
│   │       ├── __init__.py
│   │       ├── chroma_store.py
│   │       └── faiss_store.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── document.py
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
├── frontend/
│   ├── app.py
│   └── components/
│       ├── __init__.py
│       └── ui_components.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_document_service.py
│   │   ├── test_text_chunker.py
│   │   └── test_embedding_service.py
│   └── integration/
│       ├── __init__.py
│       ├── test_rag_pipeline.py
│       └── test_api.py
├── configs/
│   ├── config.yaml
│   └── .env.example
├── data/
│   ├── uploads/
│   ├── processed/
│   └── vectordb/
├── docs/
│   ├── README.md
│   └── USER_GUIDE.md
├── logs/
├── scripts/
│   ├── deploy.sh
│   └── verify_setup.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

---

### Phase 2: Git Repository Setup

1. Initialized Git repository
2. Created `.gitignore` for Python projects
3. Connected to GitHub remote repository
4. **Repository:** https://github.com/ShreyanshVaibhaw/SAFES-Source-Aware-Framework-for-Exam-Support-
5. Initial commit with project structure

**Git Commits:**
- `c1c3320` - Initial project structure for SAFES
- `855c724` - Add configuration, logging, and dependencies

---

### Phase 3: Dependencies (requirements.txt)

Created comprehensive requirements.txt with 25+ packages:

| Category | Packages |
|----------|----------|
| Core Framework | fastapi, uvicorn, python-multipart |
| Frontend | streamlit |
| Document Processing | pypdf, pdfplumber, python-docx, unstructured |
| Vector DB & Embeddings | chromadb, faiss-cpu, sentence-transformers |
| LLM Integration | openai, langchain, langchain-community, langchain-openai, tiktoken |
| NLP & Text | nltk, spacy |
| Utilities | pydantic, pydantic-settings, python-dotenv, loguru, tenacity, pyyaml |
| Testing | pytest, pytest-asyncio, httpx |

---

### Phase 4: Configuration Files

#### configs/config.yaml
Complete application configuration with sections:
- App settings (name, version, debug)
- Document processing (chunk_size: 500, overlap: 50, max_file_size: 50MB)
- Vector database (ChromaDB, all-MiniLM-L6-v2 embeddings)
- LLM configuration (GPT-3.5-turbo, temperature: 0.3)
- Retrieval settings (top_k: 5, similarity_threshold: 0.7)
- Hallucination control (confidence_threshold: 0.6, require_citation: true)
- Bloom's Taxonomy (6 cognitive levels)
- Citation settings (inline format)
- API settings (host: 0.0.0.0, port: 8000)
- Frontend settings
- Logging configuration
- Exam helper settings

#### configs/.env.example
Environment variables template:
- OPENAI_API_KEY
- SECRET_KEY
- ENVIRONMENT
- LOG_LEVEL
- Database paths
- API settings

---

### Phase 5: Utility Modules

#### src/utils/logger.py
Comprehensive logging utility using loguru:
- `setup_logger()` - Configure application-wide logging
- `get_logger(name)` - Get module-specific logger
- Console logging with colors (DEBUG level)
- File logging with rotation (10MB, 7-day retention)
- Separate error log file (ERROR level only)
- Decorators: `@log_function_call`, `@log_async_function_call`
- `LogContext` for temporary context binding

#### src/utils/config.py
Configuration management utility:
- `ConfigLoader` class with singleton pattern
- Dot notation access: `config.get("llm.model")`
- Environment variable override support
- Type conversion (string → bool/int/float)
- Properties for common values:
  - `openai_api_key`, `environment`, `is_debug`, `log_level`
  - `upload_dir`, `processed_dir`, `vectordb_dir`
  - `llm_model`, `llm_temperature`, `llm_max_tokens`
  - `chunk_size`, `chunk_overlap`, `allowed_extensions`
- Global `config` instance for easy importing

---

### Phase 6: Environment Setup & Verification

1. Created Python virtual environment (`venv/`)
2. Installed all dependencies from requirements.txt
3. Downloaded spaCy English model (en_core_web_sm)
4. Created verification script (`scripts/verify_setup.py`)

#### Verification Results (All Passed):
| Category | Status | Key Versions |
|----------|--------|--------------|
| Core Libraries | OK | FastAPI 0.128.0, Streamlit 1.53.1, Pydantic 2.12.5 |
| Document Processing | OK | PyPDF 6.6.2, PDFPlumber 0.11.9, python-docx 1.2.0 |
| Vector & Embeddings | OK | ChromaDB 1.4.1, FAISS, Sentence-Transformers 5.2.2 |
| LLM Integration | OK | OpenAI 2.15.0, LangChain-Core 1.2.7, Tiktoken 0.12.0 |
| NLP Libraries | OK | NLTK 3.9.2, spaCy 3.8.11, en_core_web_sm model |
| Utilities | OK | Loguru 0.7.3, HTTPX 0.28.1 |
| Directories | OK | All 13 directories present |
| Configuration | OK | config.yaml loaded, chunk_size=500 |
| Logger | OK | Configured with file rotation |
| API Key | OK | OPENAI_API_KEY is set |

**Python Version:** 3.12.5

---

### Next Steps (Planned)

1. **Document Models** - Pydantic models for documents, chunks, citations
2. **Document Processors** - PDF/DOCX parsing with metadata extraction
3. **Vector Store** - ChromaDB integration for storing embeddings
4. **Embedding Service** - Generate embeddings using sentence-transformers
5. **RAG Engine** - Core retrieval and generation logic
6. **Hallucination Detection** - Verify answers are grounded in sources
7. **Citation Manager** - Extract and format citations
8. **Bloom's Taxonomy** - Response style adjustment
9. **API Endpoints** - FastAPI routes for documents and queries
10. **Streamlit Frontend** - User interface for upload and chat

---

## Commands Reference

### Running the Project
```bash
# Activate virtual environment
cd "C:/Users/shrey/OneDrive/Desktop/study assistant"
./venv/Scripts/activate  # Windows

# Run verification
python scripts/verify_setup.py

# Start API server (when implemented)
uvicorn src.api.main:app --reload

# Start Streamlit frontend (when implemented)
streamlit run frontend/app.py
```

### Git Commands
```bash
# Check status
git status

# Add and commit
git add .
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

---

## Repository Information

- **GitHub:** https://github.com/ShreyanshVaibhaw/SAFES-Source-Aware-Framework-for-Exam-Support-
- **Owner:** ShreyanshVaibhaw
- **Branch:** main
- **Created:** January 28, 2026

---

*This history file is maintained to track development progress.*
