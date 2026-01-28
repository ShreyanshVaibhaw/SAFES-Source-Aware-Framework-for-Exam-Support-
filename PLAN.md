# SAFES Development Plan

## Project: Source-Aware Framework for Exam Support
**AI Study Assistant with RAG (Retrieval-Augmented Generation)**

---

## Executive Summary

SAFES is an exam-focused generative AI study assistant that helps students prepare for exams by answering questions based solely on their uploaded study materials. The system uses Retrieval-Augmented Generation (RAG) to ensure all responses are grounded in source documents with proper citations.

### Key Value Propositions:
- **Source Grounding**: All answers derived ONLY from uploaded materials
- **Citation Tracking**: Every response includes document source and page references
- **Hallucination Prevention**: Built-in controls to ensure answer accuracy
- **Bloom's Taxonomy Integration**: Adjusts response complexity based on learning level
- **User-Friendly**: Simple upload-and-ask interface

---

## Technology Stack

### Backend
- **Framework**: FastAPI (async REST API)
- **Language**: Python 3.11+
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **LLM**: OpenAI GPT-3.5-turbo / GPT-4
- **Document Processing**: pdfplumber, python-docx, unstructured

### Frontend
- **Framework**: Streamlit
- **UI Components**: Custom Streamlit components

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Testing**: pytest, pytest-asyncio
- **Logging**: loguru
- **Configuration**: YAML + environment variables

---

## Development Phases

### Phase 1: Foundation (COMPLETED) ✓
- [x] Project structure setup
- [x] Git repository initialization
- [x] Dependencies configuration (requirements.txt)
- [x] Configuration management (config.yaml, .env)
- [x] Logging utility
- [x] Environment verification

**Status**: ✅ All files created, dependencies installed, verification passed

---

### Phase 2: Document Processing (IN PROGRESS)

#### 2.1 Document Models
**File**: `src/models/document.py`

**Tasks**:
- [ ] Create `Document` Pydantic model
  - Fields: id, filename, content, metadata, upload_date
- [ ] Create `DocumentChunk` model
  - Fields: id, document_id, content, chunk_index, metadata
- [ ] Create `Citation` model
  - Fields: document_name, page_number, section, confidence
- [ ] Add validation for file types and size limits

**Priority**: HIGH  
**Estimated Time**: 2 hours

---

#### 2.2 Document Processors
**Files**: 
- `src/services/document_processors/pdf_processor.py`
- `src/services/document_processors/docx_processor.py`
- `src/services/document_processors/text_chunker.py`

**Tasks**:
- [ ] **PDF Processor**:
  - Parse PDF files with pdfplumber
  - Extract text, tables, and metadata
  - Handle multi-page documents
  - Extract page numbers for citations
  
- [ ] **DOCX Processor**:
  - Parse Word documents with python-docx
  - Extract text, tables, and metadata
  - Handle headings and section structure
  
- [ ] **Text Chunker**:
  - Implement semantic chunking (500 tokens, 50 overlap)
  - Preserve sentence boundaries
  - Maintain metadata through chunks
  - Handle edge cases (very short/long documents)

**Priority**: HIGH  
**Estimated Time**: 4 hours

---

#### 2.3 Document Service
**File**: `src/services/document_service.py`

**Tasks**:
- [ ] Implement `DocumentService` class
- [ ] File upload handling (validation, storage)
- [ ] Document parsing orchestration
- [ ] Document retrieval by ID
- [ ] Document deletion
- [ ] List all documents for a user

**Priority**: HIGH  
**Estimated Time**: 3 hours

---

### Phase 3: Vector Store & Embeddings

#### 3.1 Embedding Service
**File**: `src/services/embedding_service.py`

**Tasks**:
- [ ] Initialize Sentence-Transformer model (all-MiniLM-L6-v2)
- [ ] Implement batch embedding generation
- [ ] Add caching for repeated queries
- [ ] Handle embedding dimensions (384-dim)
- [ ] Error handling for large inputs

**Priority**: HIGH  
**Estimated Time**: 2 hours

---

#### 3.2 Vector Store (ChromaDB)
**File**: `src/services/vector_store/chroma_store.py`

**Tasks**:
- [ ] Initialize ChromaDB client
- [ ] Create collection with metadata
- [ ] Implement `add_documents()` method
- [ ] Implement `search()` method (top-k retrieval)
- [ ] Implement `delete_document()` method
- [ ] Add similarity threshold filtering
- [ ] Implement metadata filtering

**Priority**: HIGH  
**Estimated Time**: 3 hours

---

#### 3.3 Retrieval Service
**File**: `src/services/retrieval_service.py`

**Tasks**:
- [ ] Implement hybrid retrieval (vector + keyword)
- [ ] Query expansion for better recall
- [ ] Reranking of retrieved chunks
- [ ] Context window management
- [ ] Return chunks with source metadata

**Priority**: MEDIUM  
**Estimated Time**: 3 hours

---

### Phase 4: LLM Integration & RAG Engine

#### 4.1 LLM Service
**File**: `src/services/llm_service.py`

**Tasks**:
- [ ] Initialize OpenAI API client
- [ ] Implement `generate_answer()` method
- [ ] Token counting and management
- [ ] Temperature control
- [ ] Retry logic with exponential backoff
- [ ] Stream responses (optional)

**Priority**: HIGH  
**Estimated Time**: 2 hours

---

#### 4.2 RAG Engine (Core)
**File**: `src/core/rag_engine.py`

**Tasks**:
- [ ] Implement end-to-end RAG pipeline
- [ ] Query → Retrieval → Generation flow
- [ ] Context building from retrieved chunks
- [ ] Prompt engineering for source-grounded answers
- [ ] Response post-processing

**Priority**: CRITICAL  
**Estimated Time**: 4 hours

---

#### 4.3 Prompts
**File**: `src/core/prompts.py`

**Tasks**:
- [ ] System prompt for RAG
- [ ] Few-shot examples
- [ ] Citation instruction prompts
- [ ] Bloom's Taxonomy level prompts (6 levels)
- [ ] Hallucination prevention instructions

**Priority**: HIGH  
**Estimated Time**: 2 hours

---

### Phase 5: Advanced Features

#### 5.1 Hallucination Detector
**File**: `src/core/hallucination_detector.py`

**Tasks**:
- [ ] Implement entailment checking
- [ ] Fact verification against sources
- [ ] Confidence scoring
- [ ] Flag unsupported claims
- [ ] Return verification results

**Priority**: HIGH  
**Estimated Time**: 4 hours

---

#### 5.2 Citation Manager
**File**: `src/core/citation_manager.py`

**Tasks**:
- [ ] Extract citations from LLM responses
- [ ] Map citations to source documents
- [ ] Format citations (inline, footnotes)
- [ ] Validate citation accuracy
- [ ] Handle multiple citations per answer

**Priority**: HIGH  
**Estimated Time**: 3 hours

---

#### 5.3 Bloom's Taxonomy Integration
**File**: `src/core/blooms_taxonomy.py`

**Tasks**:
- [ ] Define 6 cognitive levels (Remember, Understand, Apply, Analyze, Evaluate, Create)
- [ ] Classify user questions by level
- [ ] Adjust response style based on level
- [ ] Add level-specific prompts
- [ ] Provide level-appropriate examples

**Priority**: MEDIUM  
**Estimated Time**: 3 hours

---

#### 5.4 Exam Helper
**File**: `src/services/exam_helper.py`

**Tasks**:
- [ ] Generate practice questions from documents
- [ ] Create flashcards
- [ ] Summarize key concepts
- [ ] Identify important topics
- [ ] Generate study schedules (optional)

**Priority**: LOW  
**Estimated Time**: 4 hours

---

### Phase 6: API Development

#### 6.1 API Models
**File**: `src/api/models.py`

**Tasks**:
- [ ] Define request/response models
- [ ] `UploadDocumentRequest`
- [ ] `QueryRequest` (question, bloom_level, filters)
- [ ] `QueryResponse` (answer, citations, confidence)
- [ ] Error response models

**Priority**: HIGH  
**Estimated Time**: 1 hour

---

#### 6.2 Document Router
**File**: `src/api/routers/documents.py`

**Endpoints**:
- [ ] `POST /documents/upload` - Upload document
- [ ] `GET /documents/` - List all documents
- [ ] `GET /documents/{id}` - Get document details
- [ ] `DELETE /documents/{id}` - Delete document
- [ ] `GET /documents/{id}/chunks` - Get document chunks

**Priority**: HIGH  
**Estimated Time**: 3 hours

---

#### 6.3 Query Router
**File**: `src/api/routers/query.py`

**Endpoints**:
- [ ] `POST /query` - Ask a question
- [ ] `GET /query/history` - Get query history
- [ ] `POST /query/feedback` - Submit feedback on answer

**Priority**: HIGH  
**Estimated Time**: 2 hours

---

#### 6.4 Main API App
**File**: `src/api/main.py`

**Tasks**:
- [ ] Initialize FastAPI app
- [ ] Add CORS middleware
- [ ] Register routers
- [ ] Add exception handlers
- [ ] Health check endpoint
- [ ] API documentation (Swagger)

**Priority**: HIGH  
**Estimated Time**: 2 hours

---

### Phase 7: Frontend Development

#### 7.1 UI Components
**File**: `frontend/components/ui_components.py`

**Tasks**:
- [ ] File uploader component
- [ ] Document list display
- [ ] Chat interface component
- [ ] Citation display component
- [ ] Bloom's level selector
- [ ] Loading indicators

**Priority**: MEDIUM  
**Estimated Time**: 3 hours

---

#### 7.2 Main Streamlit App
**File**: `frontend/app.py`

**Pages**:
- [ ] **Upload Page**: Upload and manage documents
- [ ] **Query Page**: Ask questions and view answers
- [ ] **History Page**: View past queries
- [ ] **Settings Page**: Configure preferences

**Features**:
- [ ] Session state management
- [ ] API integration
- [ ] Error handling
- [ ] Responsive layout

**Priority**: MEDIUM  
**Estimated Time**: 4 hours

---

### Phase 8: Testing

#### 8.1 Unit Tests
**Files**: `tests/unit/test_*.py`

**Coverage**:
- [ ] Test document processors (PDF, DOCX)
- [ ] Test text chunker
- [ ] Test embedding service
- [ ] Test vector store operations
- [ ] Test citation extraction
- [ ] Test Bloom's classification

**Priority**: HIGH  
**Estimated Time**: 4 hours

---

#### 8.2 Integration Tests
**Files**: `tests/integration/test_*.py`

**Coverage**:
- [ ] End-to-end RAG pipeline
- [ ] API endpoints
- [ ] Document upload → Query → Response flow
- [ ] Error scenarios

**Priority**: MEDIUM  
**Estimated Time**: 3 hours

---

### Phase 9: Deployment & DevOps

#### 9.1 Docker Setup
**Tasks**:
- [ ] Update Dockerfile (multi-stage build)
- [ ] Update docker-compose.yml
- [ ] Add health checks
- [ ] Configure volumes for persistence

**Priority**: MEDIUM  
**Estimated Time**: 2 hours

---

#### 9.2 Deployment Scripts
**File**: `scripts/deploy.sh`

**Tasks**:
- [ ] Build Docker images
- [ ] Run database migrations (if any)
- [ ] Start services
- [ ] Run health checks

**Priority**: LOW  
**Estimated Time**: 1 hour

---

### Phase 10: Documentation & Polish

#### 10.1 Documentation
**Files**: `docs/*.md`

**Tasks**:
- [ ] Complete README.md
- [ ] Write USER_GUIDE.md
- [ ] API documentation
- [ ] Deployment guide
- [ ] Architecture diagram

**Priority**: MEDIUM  
**Estimated Time**: 3 hours

---

#### 10.2 Code Quality
**Tasks**:
- [ ] Add type hints throughout
- [ ] Add docstrings to all functions
- [ ] Code formatting (black, isort)
- [ ] Linting (flake8, pylint)
- [ ] Security scan

**Priority**: MEDIUM  
**Estimated Time**: 2 hours

---

## Success Metrics

### Functional Requirements
- ✅ Users can upload PDF, DOCX, TXT files
- ✅ System processes and stores documents
- ✅ Users can ask questions about their materials
- ✅ System generates answers with citations
- ✅ Bloom's Taxonomy levels are supported
- ✅ No hallucination (answers only from sources)

### Performance Requirements
- Response time < 5 seconds (95th percentile)
- Support 100+ page documents
- Handle 10+ concurrent users
- 90%+ citation accuracy

### Quality Requirements
- 90%+ code coverage
- No critical security vulnerabilities
- All API endpoints documented
- User guide available

---

## Timeline Estimate

| Phase | Duration | Status |
|-------|----------|--------|
| 1. Foundation | 1 day | ✅ Complete |
| 2. Document Processing | 2 days | 📋 Planned |
| 3. Vector Store & Embeddings | 2 days | 📋 Planned |
| 4. LLM & RAG Engine | 2 days | 📋 Planned |
| 5. Advanced Features | 3 days | 📋 Planned |
| 6. API Development | 2 days | 📋 Planned |
| 7. Frontend Development | 2 days | 📋 Planned |
| 8. Testing | 2 days | 📋 Planned |
| 9. Deployment | 1 day | 📋 Planned |
| 10. Documentation | 1 day | 📋 Planned |
| **Total** | **~18 days** | **5% Complete** |

---

## Risk Mitigation

### Technical Risks
1. **Risk**: OpenAI API rate limits
   - **Mitigation**: Implement caching, use local LLM fallback

2. **Risk**: Large documents exceed context windows
   - **Mitigation**: Implement smart chunking, use map-reduce pattern

3. **Risk**: Low citation accuracy
   - **Mitigation**: Post-processing validation, user feedback loop

4. **Risk**: Slow retrieval performance
   - **Mitigation**: Index optimization, caching, batch processing

### Non-Technical Risks
1. **Risk**: OpenAI API costs
   - **Mitigation**: Token usage monitoring, cheaper model for embeddings

2. **Risk**: User adoption
   - **Mitigation**: Focus on UX, provide examples, collect feedback

---

## Next Immediate Steps

1. ✅ Complete Phase 1 (Foundation)
2. 🔄 Start Phase 2.1: Create Document Models
3. 🔄 Implement PDF processor
4. 🔄 Implement text chunker
5. 🔄 Set up ChromaDB integration

---

## Notes

- All development follows Test-Driven Development (TDD) where applicable
- Code reviews required for critical components (RAG engine, hallucination detection)
- User feedback sessions planned after Phase 7 (Frontend)
- Performance profiling after Phase 8 (Testing)

---

*Last Updated: January 28, 2026*
*Project Status: Foundation Complete, Document Processing In Progress*
