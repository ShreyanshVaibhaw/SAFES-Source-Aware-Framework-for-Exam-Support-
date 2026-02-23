# Complete Claude Code Prompts for AI Study Assistant
## Copy-Paste Ready Prompts for Each Phase

---

# 🚀 INITIAL SETUP PROMPT

**Use this first to give Claude Code context about the entire project:**

```
I'm building an "Exam-Focused Generative AI Study Assistant" using RAG (Retrieval-Augmented Generation). 

PROJECT OVERVIEW:
- Students upload study materials (PDF, DOCX, TXT)
- System processes and stores documents in a vector database
- Students ask questions about their study materials
- System retrieves relevant content and generates answers ONLY from uploaded materials
- All answers include citations (document name, page number, section)
- Hallucination control ensures answers are grounded in source materials
- Bloom's Taxonomy integration adjusts response style (Remember, Understand, Apply, Analyze, Evaluate, Create)
- FastAPI backend + Streamlit frontend

TECH STACK:
- Python 3.11+
- FastAPI (backend API)
- Streamlit (frontend UI)
- ChromaDB (vector database)
- Sentence-Transformers (embeddings)
- OpenAI GPT API (language model)
- pdfplumber, python-docx (document parsing)
- Pydantic (data validation)

Let's build this step by step. Confirm you understand, then we'll start with Phase 1.
```

---

# 📁 PHASE 1: Environment Setup & Foundation

---

## Prompt 1.1: Create Project Structure

```
Create the complete project directory structure for the AI Study Assistant:

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
│   └── deploy.sh
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md

Create all folders and empty __init__.py files. Add a .gitkeep file in empty data folders.
```

---

## Prompt 1.2: Create Requirements File

```
Create requirements.txt with all necessary dependencies for the AI Study Assistant:

CORE FRAMEWORK:
- fastapi (latest stable)
- uvicorn (ASGI server)
- python-multipart (file uploads)

FRONTEND:
- streamlit

DOCUMENT PROCESSING:
- pypdf (PDF reading)
- pdfplumber (PDF text extraction with tables)
- python-docx (Word documents)
- unstructured (general document parsing)

VECTOR DATABASE & EMBEDDINGS:
- chromadb
- faiss-cpu
- sentence-transformers

LLM INTEGRATION:
- openai
- langchain
- langchain-community
- langchain-openai
- tiktoken (token counting)

NLP & TEXT PROCESSING:
- nltk
- spacy

UTILITIES:
- pydantic (data validation)
- pydantic-settings
- python-dotenv (environment variables)
- loguru (logging)
- tenacity (retry logic)
- pyyaml (config files)

TESTING:
- pytest
- pytest-asyncio
- httpx (async HTTP client for testing)

Add version numbers for stability. Include a comment header explaining the project.
```

---

## Prompt 1.3: Create Configuration Files

```
Create the configuration files for the project:

1. configs/config.yaml - Main configuration file with these sections:

APP SETTINGS:
- name: "AI Study Assistant"
- version: "1.0.0"
- debug: true

DOCUMENT PROCESSING:
- max_file_size_mb: 50
- allowed_extensions: [".pdf", ".docx", ".txt", ".md"]
- chunk_size: 500 (tokens)
- chunk_overlap: 50 (tokens)
- min_chunk_size: 100 (tokens)

VECTOR DATABASE:
- type: "chromadb"
- collection_name: "study_materials"
- embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
- persist_directory: "data/vectordb"

LLM CONFIGURATION:
- provider: "openai"
- model: "gpt-3.5-turbo"
- temperature: 0.3
- max_tokens: 1500

RETRIEVAL SETTINGS:
- top_k: 5
- similarity_threshold: 0.7
- max_context_tokens: 2000

HALLUCINATION CONTROL:
- confidence_threshold: 0.6
- require_citation: true
- max_unsupported_ratio: 0.2

API SETTINGS:
- host: "0.0.0.0"
- port: 8000

FRONTEND SETTINGS:
- api_url: "http://localhost:8000"

2. configs/.env.example - Template for environment variables:
- OPENAI_API_KEY=your_api_key_here
- ENVIRONMENT=development
- LOG_LEVEL=DEBUG
- SECRET_KEY=your_secret_key_here

Add helpful comments explaining each setting.
```

---

## Prompt 1.4: Create Logger Utility

```
Create src/utils/logger.py - A comprehensive logging utility using loguru:

REQUIREMENTS:
1. Function setup_logger() that configures logging for the entire application

2. Console logging with:
   - Colored output
   - Format: timestamp | level | module:function:line | message
   - DEBUG level for development

3. File logging with:
   - Rotation at 10 MB
   - Retention for 7 days
   - INFO level minimum
   - Saved to logs/app.log

4. Separate error log file:
   - Only ERROR and above
   - Saved to logs/error.log

5. Function get_logger(name) that returns a configured logger for a specific module

6. Include log formatting that shows:
   - Timestamp (human readable)
   - Log level (colored)
   - Module name
   - Function name
   - Line number
   - Message

Make sure logs directory is created if it doesn't exist.
```

---

## Prompt 1.5: Create Configuration Loader

```
Create src/utils/config.py - Configuration management utility:

REQUIREMENTS:

1. Class ConfigLoader that:
   - Loads config.yaml on initialization
   - Loads environment variables from .env file
   - Provides easy access to nested config values using dot notation
   - Example: config.get('document.chunk_size') returns 500

2. Methods:
   - __init__(config_path): Load config file, default to "configs/config.yaml"
   - get(key, default=None): Get config value using dot notation
   - get_section(section): Get entire config section as dict
   - reload(): Reload configuration from file

3. Properties for common values:
   - openai_api_key: from environment variable
   - environment: development/production
   - is_debug: boolean based on environment
   - log_level: from config or environment

4. Singleton pattern so config is loaded only once

5. Validation:
   - Check required environment variables exist
   - Raise clear errors if config file is missing
   - Type hints for all methods

6. Create a global config instance that can be imported:
   from src.utils.config import config

Include docstrings and usage examples in comments.
```

---

## Prompt 1.6: Install and Verify Setup

```
Now let's verify the setup:

1. Create a Python virtual environment in the project folder

2. Install all dependencies from requirements.txt

3. Download the spaCy English model: python -m spacy download en_core_web_sm

4. Create a simple test script (scripts/verify_setup.py) that:
   - Imports all major libraries
   - Loads the configuration
   - Tests the logger
   - Verifies OpenAI API key is set (without exposing it)
   - Prints success message with versions of key libraries

5. Run the verification script and show me the output

If any errors occur, fix them before proceeding.
```

---

# 📄 PHASE 2: Document Processing Pipeline

---

## Prompt 2.1: Create Document Models

```
Create src/models/document.py with Pydantic models for document handling:

1. ENUMS:
   - DocumentType: PDF, DOCX, TXT, MD
   - ProcessingStatus: PENDING, PROCESSING, COMPLETED, FAILED

2. DocumentMetadata model:
   - filename: str
   - file_type: DocumentType
   - file_size: int (bytes)
   - page_count: Optional[int]
   - upload_timestamp: datetime (auto-generated)
   - subject: Optional[str] (e.g., "Computer Science")
   - course: Optional[str] (e.g., "CS101")
   - tags: List[str] (default empty)
   - original_path: Optional[str]

3. DocumentChunk model:
   - chunk_id: str (unique identifier)
   - document_id: str (parent document)
   - content: str (the actual text)
   - page_number: Optional[int]
   - section_title: Optional[str]
   - start_char: int (position in original)
   - end_char: int
   - token_count: int
   - metadata: dict (flexible additional data)

4. ProcessedDocument model:
   - document_id: str (unique)
   - metadata: DocumentMetadata
   - chunks: List[DocumentChunk]
   - total_chunks: int
   - total_tokens: int
   - processing_status: ProcessingStatus
   - processing_time: Optional[float] (seconds)
   - error_message: Optional[str]

5. DocumentUploadResponse model (for API):
   - document_id: str
   - filename: str
   - chunks_created: int
   - status: str
   - message: str

Add validators where appropriate (e.g., filename not empty, file_size > 0).
Include Config class for JSON serialization settings.
```

---

## Prompt 2.2: Create PDF Processor

```
Create src/services/document_processors/pdf_processor.py:

Class PDFProcessor that handles PDF document extraction:

METHODS:

1. __init__(self):
   - Initialize supported extensions list
   - Set up logger

2. extract_text_with_metadata(self, file_path: Path) -> List[Dict]:
   - Open PDF using pdfplumber
   - For each page, extract:
     - page_number (1-indexed)
     - content (extracted text)
     - tables (converted to text format)
     - has_images (boolean)
   - Return list of page data dictionaries
   - Handle extraction errors gracefully
   - Log progress for large documents

3. _tables_to_text(self, tables: List) -> str:
   - Convert pdfplumber table data to readable text
   - Format as "column1 | column2 | column3"
   - Separate rows with newlines
   - Handle None/empty cells

4. get_document_metadata(self, file_path: Path) -> Dict:
   - Use pypdf to extract PDF metadata
   - Return: title, author, subject, creator, page_count, creation_date
   - Handle missing metadata fields

5. extract_images_info(self, file_path: Path) -> List[Dict]:
   - Get information about images in PDF
   - Return list with page_number, image_count, dimensions
   - (We won't process images, just track them)

6. validate_pdf(self, file_path: Path) -> Tuple[bool, str]:
   - Check if file is valid PDF
   - Check if encrypted/password protected
   - Check if has extractable text
   - Return (is_valid, error_message)

ERROR HANDLING:
- Catch and log specific exceptions
- Return partial results if some pages fail
- Include page number in error messages

Add comprehensive docstrings and type hints.
```

---

## Prompt 2.3: Create DOCX Processor

```
Create src/services/document_processors/docx_processor.py:

Class DOCXProcessor that handles Word document extraction:

METHODS:

1. __init__(self):
   - Initialize supported extensions ['.docx', '.doc']
   - Set up logger

2. extract_text_with_metadata(self, file_path: Path) -> List[Dict]:
   - Open document using python-docx
   - Extract all paragraphs with their styles
   - Identify headings (Heading 1, Heading 2, etc.)
   - Format headings with markdown-style markers (##)
   - Extract tables and convert to text
   - Since DOCX doesn't have pages, treat as single page
   - Return list with single page data dictionary

3. _process_paragraph(self, paragraph) -> Tuple[str, bool]:
   - Get paragraph text
   - Check if it's a heading style
   - Return (formatted_text, is_heading)

4. _tables_to_text(self, tables) -> str:
   - Convert Word tables to readable text
   - Format similar to PDF tables
   - Handle merged cells

5. _extract_headers_footers(self, doc) -> Dict:
   - Extract header and footer text
   - Return as metadata (not main content)

6. get_document_metadata(self, file_path: Path) -> Dict:
   - Extract document properties
   - Return: title, author, subject, created, modified, word_count

7. validate_docx(self, file_path: Path) -> Tuple[bool, str]:
   - Check if valid DOCX file
   - Check if corrupted
   - Return (is_valid, error_message)

Handle the case where .doc files (old format) are uploaded - return helpful error message suggesting conversion to .docx.
```

---

## Prompt 2.4: Create Text Chunker

```
Create src/services/document_processors/text_chunker.py:

DATACLASS ChunkConfig:
- chunk_size: int = 500 (target tokens per chunk)
- chunk_overlap: int = 50 (overlap tokens between chunks)
- min_chunk_size: int = 100 (minimum tokens to create chunk)
- separators: List[str] = ["\n\n", "\n", ". ", " "] (split priorities)

CLASS TextChunker:

METHODS:

1. __init__(self, config: Optional[ChunkConfig] = None):
   - Load config or use defaults
   - Initialize tiktoken encoder for token counting (cl100k_base)
   - Set up logger

2. chunk_document(self, pages_data: List[Dict], document_id: str) -> List[Dict]:
   - Main method to chunk entire document
   - Process each page
   - Detect and preserve section headers
   - Create chunks with metadata
   - Return list of chunk dictionaries with:
     - chunk_id, document_id, content, page_number
     - section_title, token_count, start_position

3. _split_by_sections(self, text: str) -> List[Tuple[str, str]]:
   - Detect section headers using patterns:
     - Markdown headers (# ## ###)
     - Numbered sections (1. 1.1 1.1.1)
     - ALL CAPS HEADERS
   - Return list of (section_title, section_content) tuples

4. _create_chunks(self, text: str) -> List[str]:
   - Split text into chunks of target size
   - Try splitting by separators in order (paragraph, line, sentence, word)
   - Maintain overlap between consecutive chunks
   - Respect minimum chunk size

5. _get_overlap_text(self, previous_chunk: str) -> str:
   - Extract last N tokens from previous chunk for overlap
   - Ensure overlap doesn't break mid-word

6. count_tokens(self, text: str) -> int:
   - Count tokens using tiktoken
   - Cache encoder for performance

7. _find_best_split_point(self, text: str, target_length: int) -> int:
   - Find optimal position to split text
   - Prefer splitting at paragraph/sentence boundaries
   - Avoid splitting mid-word or mid-sentence

IMPORTANT LOGIC:
- If a section is smaller than min_chunk_size, combine with next section
- If a section is larger than chunk_size, split it further
- Always preserve page_number reference for citations
- Include section_title in chunk metadata when available

Add unit test examples in docstrings showing input/output.
```

---

## Prompt 2.5: Create Document Service

```
Create src/services/document_service.py - The main orchestration service:

CLASS DocumentService:

METHODS:

1. __init__(self, config: Optional[ConfigLoader] = None):
   - Load configuration
   - Initialize PDF processor
   - Initialize DOCX processor
   - Initialize text chunker with config values
   - Set up upload directory path
   - Create in-memory document store (dict)
   - Set up logger

2. process_document(self, file_path: Path, metadata: Optional[dict] = None) -> ProcessedDocument:
   - Main entry point for document processing
   - Steps:
     a. Validate file exists and is allowed type
     b. Generate unique document_id using hash + uuid
     c. Determine file type and select processor
     d. Extract text and metadata
     e. Chunk the document
     f. Build ProcessedDocument object
     g. Store in memory
     h. Log processing stats
   - Return ProcessedDocument
   - Handle and log errors, return failed status if needed

3. _generate_document_id(self, file_path: Path) -> str:
   - Create MD5 hash of file contents (first 8 chars)
   - Append 6 random chars from uuid
   - Format: "doc_{hash}_{uuid}"

4. _get_file_type(self, file_path: Path) -> DocumentType:
   - Determine type from extension
   - Raise error for unsupported types

5. _process_text_file(self, file_path: Path) -> List[Dict]:
   - Handle .txt and .md files
   - Read content with UTF-8 encoding
   - Return as single page

6. get_document(self, document_id: str) -> Optional[ProcessedDocument]:
   - Retrieve document from memory store

7. list_documents(self) -> List[Dict]:
   - Return summary of all processed documents
   - Include: document_id, filename, chunks, upload_time

8. delete_document(self, document_id: str) -> bool:
   - Remove document from memory store
   - Return success status

9. get_document_chunks(self, document_id: str) -> List[DocumentChunk]:
   - Get all chunks for a specific document

10. search_documents(self, query: str, filters: Dict = None) -> List[Dict]:
    - Basic search through document metadata
    - Filter by subject, course, tags

VALIDATION:
- Check file size against max_file_size_mb config
- Check extension against allowed_extensions config
- Validate file is readable

Create a simple test at the end that processes a sample text to verify it works.
```

---

## Prompt 2.6: Test Document Processing

```
Let's test the document processing pipeline:

1. Create a test PDF file or use a simple one if available

2. Create tests/unit/test_document_service.py with tests for:
   - File type detection (PDF, DOCX, TXT)
   - Document ID generation (unique, correct format)
   - Processing a text file
   - Chunk creation (correct size, overlap)
   - Error handling for invalid files

3. Create tests/unit/test_text_chunker.py with tests for:
   - Short text (below min_chunk_size) - should not create chunk
   - Long text - should create multiple chunks
   - Overlap between chunks
   - Section header detection
   - Token counting accuracy

4. Run the tests and show results

5. Create a simple script (scripts/test_document_processing.py) that:
   - Creates a sample text document with multiple sections
   - Processes it through DocumentService
   - Prints: document_id, number of chunks, sample chunk content
   - Shows page/section references

Run the script and verify output is correct.
```

---

# 🔍 PHASE 3: Vector Database & Retrieval

---

## Prompt 3.1: Create Embedding Service

```
Create src/services/embedding_service.py:

CLASS EmbeddingService:

PURPOSE: Convert text into numerical vectors (embeddings) for semantic search

METHODS:

1. __init__(self, config: Optional[ConfigLoader] = None):
   - Load configuration
   - Get model name from config (default: sentence-transformers/all-MiniLM-L6-v2)
   - Initialize model as None (lazy loading)
   - Set up logger

2. _load_model(self):
   - Load SentenceTransformer model
   - Log model loading time
   - Handle download if model not cached
   - Store embedding dimension

3. embed_text(self, text: str) -> List[float]:
   - Ensure model is loaded
   - Generate embedding for single text
   - Return as list of floats
   - Handle empty text input

4. embed_batch(self, texts: List[str], batch_size: int = 32, show_progress: bool = True) -> List[List[float]]:
   - Generate embeddings for multiple texts
   - Process in batches for memory efficiency
   - Show progress bar for large batches
   - Return list of embeddings

5. compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
   - Calculate cosine similarity between two embeddings
   - Return float between -1 and 1 (usually 0 to 1 for text)

6. find_most_similar(self, query_embedding: List[float], embeddings: List[List[float]], top_k: int = 5) -> List[Tuple[int, float]]:
   - Find top_k most similar embeddings
   - Return list of (index, similarity_score) tuples
   - Sorted by similarity descending

7. get_embedding_dimension(self) -> int:
   - Return dimension of embeddings (384 for MiniLM)

PROPERTIES:
- model_name: str
- is_loaded: bool
- embedding_dim: int

OPTIMIZATION:
- Lazy load model (only when first needed)
- Normalize embeddings for faster cosine similarity
- Use numpy for efficient calculations

Add example usage in docstring showing embedding and similarity calculation.
```

---

## Prompt 3.2: Create ChromaDB Vector Store

```
Create src/services/vector_store/chroma_store.py:

CLASS ChromaVectorStore:

PURPOSE: Store document chunk embeddings and perform similarity search

METHODS:

1. __init__(self, config: Optional[ConfigLoader] = None, persist_directory: str = None):
   - Load configuration
   - Set persist directory (default: data/vectordb)
   - Get collection name from config
   - Initialize embedding service
   - Call _initialize_client()

2. _initialize_client(self):
   - Create persist directory if not exists
   - Initialize ChromaDB client with persistence settings
   - Get or create collection with cosine similarity metric
   - Log initialization status

3. add_chunks(self, chunks: List[DocumentChunk]) -> int:
   - Extract chunk IDs, contents, and metadata
   - Generate embeddings for all content using embedding service
   - Prepare metadata for each chunk:
     - document_id
     - page_number
     - section_title
     - chunk_id
   - Add to ChromaDB collection
   - Return count of chunks added
   - Handle duplicates gracefully

4. search(self, query: str, top_k: int = 5, filter_dict: Optional[Dict] = None, similarity_threshold: float = 0.0) -> List[Dict]:
   - Generate query embedding
   - Build where clause from filter_dict if provided
   - Query ChromaDB collection
   - Convert distances to similarities (1 - distance for cosine)
   - Filter by similarity threshold
   - Return list of results with:
     - chunk_id, content, metadata, similarity score

5. search_by_embedding(self, embedding: List[float], top_k: int = 5) -> List[Dict]:
   - Search using pre-computed embedding
   - Same return format as search()

6. get_chunk(self, chunk_id: str) -> Optional[Dict]:
   - Retrieve specific chunk by ID
   - Return content and metadata

7. delete_document(self, document_id: str) -> int:
   - Delete all chunks for a document
   - Return count of deleted chunks

8. delete_chunk(self, chunk_id: str) -> bool:
   - Delete specific chunk
   - Return success status

9. update_chunk_metadata(self, chunk_id: str, metadata: Dict) -> bool:
   - Update metadata for existing chunk
   - Return success status

10. get_collection_stats(self) -> Dict:
    - Return statistics:
      - collection_name
      - total_chunks
      - persist_directory
      - embedding_dimension

11. list_documents(self) -> List[str]:
    - Get unique document_ids in collection

12. persist(self):
    - Force persist to disk
    - Log confirmation

13. clear_collection(self):
    - Remove all data from collection
    - Use with caution!

ERROR HANDLING:
- Handle connection errors
- Handle invalid queries
- Log all operations

Add a simple self-test method that adds a test chunk and searches for it.
```

---

## Prompt 3.3: Create FAISS Vector Store (Alternative)

```
Create src/services/vector_store/faiss_store.py:

CLASS FAISSVectorStore:

PURPOSE: Alternative vector store using Facebook's FAISS library (better for large scale)

METHODS:

1. __init__(self, embedding_dim: int = 384, persist_directory: str = "data/vectordb"):
   - Set embedding dimension
   - Set persist directory
   - Initialize embedding service
   - Initialize empty index and metadata storage
   - Call _initialize_index()

2. _initialize_index(self):
   - Create FAISS IndexFlatIP (Inner Product for cosine with normalized vectors)
   - Initialize chunk_data dict (maps index -> chunk info)
   - Initialize id_to_index dict (maps chunk_id -> FAISS index)
   - Log initialization

3. add_chunks(self, chunks: List[DocumentChunk]) -> int:
   - Generate embeddings for all chunks
   - Normalize embeddings (L2 normalization for cosine similarity)
   - Add to FAISS index
   - Store metadata in chunk_data dict
   - Update id_to_index mapping
   - Return count added

4. search(self, query: str, top_k: int = 5, similarity_threshold: float = 0.0) -> List[Dict]:
   - Generate and normalize query embedding
   - Search FAISS index
   - Filter by threshold
   - Return results with chunk info and similarity

5. delete_document(self, document_id: str) -> int:
   - FAISS doesn't support deletion easily
   - Mark chunks as deleted in metadata
   - Rebuild index periodically (separate method)
   - Return count of "deleted" chunks

6. save(self):
   - Save FAISS index to file (index.faiss)
   - Save metadata to pickle file (metadata.pkl)
   - Log save location

7. load(self):
   - Load FAISS index from file
   - Load metadata from pickle
   - Log load status

8. rebuild_index(self):
   - Rebuild index excluding deleted chunks
   - Called periodically for maintenance

9. get_stats(self) -> Dict:
   - Return: total_vectors, embedding_dim, index_type

NOTES:
- FAISS is faster for large datasets
- Less feature-rich than ChromaDB
- Good for production with millions of chunks

Add comparison notes in docstring about when to use FAISS vs ChromaDB.
```

---

## Prompt 3.4: Create Retrieval Service

```
Create src/services/retrieval_service.py:

CLASS RetrievalService:

PURPOSE: High-level retrieval interface that combines vector search with citation generation

METHODS:

1. __init__(self, config: Optional[ConfigLoader] = None):
   - Load configuration
   - Initialize vector store (ChromaDB by default)
   - Initialize document service reference
   - Get retrieval settings from config:
     - top_k (default: 5)
     - similarity_threshold (default: 0.7)
     - max_context_tokens (default: 2000)
   - Set up logger

2. index_document(self, processed_doc: ProcessedDocument) -> Dict:
   - Add all chunks from document to vector store
   - Return: document_id, chunks_indexed, status

3. retrieve(self, query: str, top_k: Optional[int] = None, document_filter: Optional[str] = None, min_similarity: Optional[float] = None) -> List[Dict]:
   - Search vector store for relevant chunks
   - Apply document filter if specified
   - Apply similarity threshold
   - Enhance each result with citation info
   - Return list of results with:
     - chunk_id, content, metadata, similarity, citation

4. _generate_citation(self, result: Dict, document_service: DocumentService) -> str:
   - Build citation string from chunk metadata
   - Format: "filename | Page X | Section: Y"
   - Handle missing metadata gracefully

5. get_context_for_query(self, query: str, max_tokens: int = None) -> Dict:
   - Retrieve relevant chunks
   - Format as numbered context for LLM:
     "[Source 1]: content..."
     "[Source 2]: content..."
   - Track token count, stop when limit reached
   - Return:
     - context: formatted string
     - citations: list of citation info
     - num_sources: count
     - total_tokens: approximate
     - query: original query

6. retrieve_with_reranking(self, query: str, top_k: int = 5, rerank_top: int = 20) -> List[Dict]:
   - First retrieve more candidates (rerank_top)
   - Rerank using more sophisticated scoring
   - Return top_k best results
   - (Future enhancement: use cross-encoder for reranking)

7. get_similar_chunks(self, chunk_id: str, top_k: int = 5) -> List[Dict]:
   - Find chunks similar to a given chunk
   - Useful for "see also" feature

8. hybrid_search(self, query: str, keyword_weight: float = 0.3) -> List[Dict]:
   - Combine semantic search with keyword matching
   - Weight results by both scores
   - (Future enhancement)

9. delete_document_from_index(self, document_id: str) -> Dict:
   - Remove document from vector store
   - Return: document_id, chunks_deleted, status

LOGGING:
- Log all retrieval operations
- Log query, results count, top similarity scores
- Track retrieval time

Add usage example in docstring showing full retrieval flow.
```

---

## Prompt 3.5: Test Vector Storage and Retrieval

```
Test the vector database and retrieval system:

1. Create tests/unit/test_embedding_service.py:
   - Test embedding generation (correct dimension)
   - Test batch embedding
   - Test similarity calculation
   - Test with empty/short text

2. Create tests/integration/test_vector_store.py:
   - Test adding chunks to ChromaDB
   - Test search returns relevant results
   - Test similarity threshold filtering
   - Test document deletion
   - Test persistence (save and reload)

3. Create a test script (scripts/test_retrieval.py) that:
   - Creates sample document chunks about a topic (e.g., "Machine Learning")
   - Indexes them in vector store
   - Performs several test queries:
     - Direct match: "What is machine learning?"
     - Semantic match: "How do computers learn from data?"
     - Unrelated query: "What is the capital of France?"
   - Prints results with similarity scores
   - Shows citation generation

4. Run all tests and the script, verify:
   - Relevant queries return high similarity scores (>0.7)
   - Unrelated queries return low scores (<0.5)
   - Citations are correctly formatted

Show the output and confirm retrieval is working correctly.
```

---

# 🧠 PHASE 4: RAG Core Implementation

---

## Prompt 4.1: Create LLM Service

```
Create src/services/llm_service.py:

CLASS LLMService:

PURPOSE: Handle all communication with the LLM (OpenAI GPT)

METHODS:

1. __init__(self, config: Optional[ConfigLoader] = None):
   - Load configuration
   - Initialize OpenAI client with API key from config
   - Get model settings:
     - model name (default: gpt-3.5-turbo)
     - temperature (default: 0.3 for factual responses)
     - max_tokens (default: 1500)
   - Set up logger
   - Validate API key exists

2. generate(self, messages: List[Dict], temperature: Optional[float] = None, max_tokens: Optional[int] = None, stop_sequences: List[str] = None) -> str:
   - Send messages to OpenAI API
   - Use provided or default parameters
   - Implement retry logic with exponential backoff (3 attempts)
   - Return response content
   - Log token usage

3. generate_stream(self, messages: List[Dict], temperature: Optional[float] = None) -> Generator[str, None, None]:
   - Stream response chunks
   - Yield each text chunk as received
   - Handle stream errors
   - Log when stream completes

4. generate_with_metadata(self, messages: List[Dict], **kwargs) -> Dict:
   - Generate response with full metadata
   - Return:
     - content: response text
     - model: model used
     - tokens_prompt: input tokens
     - tokens_completion: output tokens
     - tokens_total: total tokens
     - finish_reason: why generation stopped

5. count_tokens(self, text: str) -> int:
   - Count tokens using tiktoken
   - Use encoding for current model

6. count_messages_tokens(self, messages: List[Dict]) -> int:
   - Count tokens in message list
   - Account for message formatting overhead

7. validate_context_length(self, messages: List[Dict], max_response_tokens: int) -> bool:
   - Check if messages fit within model context window
   - Leave room for response
   - Return True if valid

8. get_model_info(self) -> Dict:
   - Return model name, context window size, default settings

RETRY LOGIC (using tenacity):
- Retry on rate limit errors
- Retry on temporary API errors
- Exponential backoff: 2, 4, 8 seconds
- Max 3 attempts
- Log each retry

ERROR HANDLING:
- Handle API key errors clearly
- Handle rate limits gracefully
- Handle network errors
- Raise informative exceptions

Include example of message format in docstring.
```

---

## Prompt 4.2: Create Prompt Templates

```
Create src/core/prompts.py:

CLASS PromptTemplates:

PURPOSE: Store and manage all prompts used in the RAG system

PROMPTS TO CREATE:

1. RAG_SYSTEM_PROMPT (string):
   """
   You are an AI Study Assistant designed to help students prepare for exams.
   
   CRITICAL RULES - YOU MUST FOLLOW THESE:
   1. ONLY use information from the provided study material context
   2. If the context doesn't contain enough information, say "I don't have enough information in the study materials to answer this question"
   3. ALWAYS cite your sources using [Source X] format where X is the source number
   4. NEVER make up or hallucinate information not in the context
   5. If uncertain, express that uncertainty
   6. Be helpful, clear, and educational
   
   Your responses should be:
   - Accurate and grounded in the provided materials only
   - Well-structured and easy to understand
   - Appropriate for exam preparation
   - Include relevant citations for every claim
   """

2. RAG_USER_PROMPT (Template with $context and $question):
   """
   Based on the following study materials, please answer the question.

   === STUDY MATERIAL CONTEXT ===
   $context
   === END CONTEXT ===

   QUESTION: $question

   Provide a comprehensive answer using ONLY information from the context above.
   Cite sources as [Source 1], [Source 2], etc.
   If the context doesn't contain relevant information, clearly state that.
   """

3. HALLUCINATION_CHECK_PROMPT (Template with $context and $response):
   - Prompt that asks LLM to verify each claim in response against context
   - Request JSON output with claim verification status

4. BLOOM_LEVEL_PROMPTS (Dict mapping level to Template):
   
   - "remember": Focus on facts, definitions, lists, memorization aids
   - "understand": Explain concepts, use examples, draw connections
   - "apply": Show practical usage, step-by-step procedures, worked examples
   - "analyze": Break down topics, compare/contrast, examine relationships
   - "evaluate": Present arguments, assess strengths/weaknesses, support with evidence
   - "create": Propose solutions, synthesize information, generate new ideas

   Each template should have $context and $question placeholders

5. INSUFFICIENT_CONTEXT_RESPONSE:
   - Standard response when no relevant context found

6. CITATION_INSTRUCTION:
   - Reusable instruction about how to cite sources

CLASS METHODS:

1. get_rag_prompt(context: str, question: str) -> str:
   - Format RAG prompt with context and question

2. get_blooms_prompt(level: str, context: str, question: str) -> str:
   - Get prompt for specific Bloom's level
   - Default to "understand" if invalid level

3. get_hallucination_check_prompt(context: str, response: str) -> str:
   - Format verification prompt

4. get_system_prompt() -> str:
   - Return system prompt

5. format_context(sources: List[Dict]) -> str:
   - Format multiple sources into context string
   - Number each source [Source 1], [Source 2], etc.

All prompts should be well-crafted for optimal LLM performance.
```

---

## Prompt 4.3: Create RAG Engine

```
Create src/core/rag_engine.py:

DATACLASS RAGResponse:
- answer: str
- citations: List[Dict]
- confidence: float
- bloom_level: str
- context_used: str
- is_grounded: bool
- sources_count: int
- processing_time: float

CLASS RAGEngine:

PURPOSE: Main engine that orchestrates retrieval and generation

METHODS:

1. __init__(self, config: Optional[ConfigLoader] = None):
   - Load configuration
   - Initialize retrieval service
   - Initialize LLM service
   - Initialize hallucination detector (placeholder for now)
   - Initialize citation manager (placeholder for now)
   - Set up logger

2. query(self, question: str, bloom_level: str = "understand", document_filter: Optional[str] = None) -> RAGResponse:
   - Main query method
   - Steps:
     a. Start timer
     b. Retrieve relevant context using retrieval service
     c. Check if sufficient context (has citations)
     d. If no context: return insufficient context response
     e. Format prompt using PromptTemplates with Bloom's level
     f. Build messages (system + user)
     g. Generate response via LLM service
     h. Calculate confidence from average similarity scores
     i. Build and return RAGResponse
   - Log query and response stats

3. query_with_verification(self, question: str, bloom_level: str = "understand", verify_hallucination: bool = True) -> Dict:
   - Get base response using query()
   - Register citations with citation manager
   - If verify_hallucination: run hallucination check
   - Add warnings if not grounded
   - Enrich answer with formatted citations
   - Return comprehensive result dict with:
     - answer, enriched_answer, citations, confidence
     - bloom_info, is_grounded, hallucination_check
     - practice_questions (placeholder)

4. query_stream(self, question: str, bloom_level: str = "understand") -> Generator:
   - Streaming version of query
   - First yield citations info
   - Then yield answer chunks
   - Yield completion signal at end

5. _build_messages(self, context: str, question: str, bloom_level: str) -> List[Dict]:
   - Build message list for LLM
   - Include system prompt
   - Include user prompt with context and question

6. _calculate_confidence(self, citations: List[Dict]) -> float:
   - Calculate overall confidence score
   - Average of similarity scores
   - Weight by citation count

7. _add_grounding_warning(self, answer: str, recommendations: List[str]) -> str:
   - Add warning header to answer if not fully grounded
   - Include recommendations

8. _format_response_with_citations(self, answer: str, citations: List[Dict]) -> str:
   - Add formatted reference list to answer
   - Format each citation with index and details

PROPERTIES:
- retrieval_service: access to retrieval
- llm_service: access to LLM

ERROR HANDLING:
- Handle retrieval failures
- Handle LLM failures
- Return helpful error messages
- Log all errors

Add comprehensive example in docstring showing full query flow.
```

---

## Prompt 4.4: Test RAG Pipeline

```
Test the RAG pipeline end-to-end:

1. Create tests/integration/test_rag_pipeline.py:
   - Test query with sufficient context returns grounded answer
   - Test query without context returns appropriate message
   - Test different Bloom's levels produce different response styles
   - Test citations are included in response
   - Test confidence calculation

2. Create a comprehensive test script (scripts/test_rag_pipeline.py) that:

   a. Creates a test document about a clear topic (e.g., "Python Programming"):
      - Include several paragraphs about variables, loops, functions
      - Include some facts and definitions
   
   b. Processes and indexes the document
   
   c. Tests multiple query types:
      - "What are variables in Python?" (Remember level)
      - "Explain how loops work" (Understand level)
      - "How would you use a function to calculate factorial?" (Apply level)
      - "What is the capital of Spain?" (Unrelated - should say no info)
   
   d. For each query, print:
      - Question
      - Bloom's level
      - Answer (truncated to 200 chars)
      - Number of citations
      - Confidence score
      - Is grounded: Yes/No
   
   e. Verify:
      - Related queries have confidence > 0.7
      - Unrelated queries handled gracefully
      - Citations are present for related queries

3. Run the test script and show output

Confirm the RAG pipeline is working correctly before moving to Phase 5.
```

---

# 🛡️ PHASE 5: Hallucination Control & Citation System

---

## Prompt 5.1: Create Hallucination Detector

```
Create src/core/hallucination_detector.py:

DATACLASS HallucinationResult:
- is_grounded: bool
- confidence_score: float (0.0 to 1.0)
- claims: List[Dict] (each with: claim, status, evidence)
- unsupported_claims: List[str]
- partially_supported_claims: List[str]
- recommendations: List[str]

CLASS HallucinationDetector:

PURPOSE: Verify that AI responses are grounded in provided context

METHODS:

1. __init__(self, config: Optional[ConfigLoader] = None):
   - Load configuration
   - Initialize LLM service (for LLM-based verification)
   - Get thresholds from config:
     - confidence_threshold (default: 0.6)
     - max_unsupported_ratio (default: 0.2)
   - Set up logger

2. check_response(self, response: str, context: str) -> HallucinationResult:
   - Main verification method
   - Run three verification methods:
     a. LLM-based claim verification
     b. Citation presence verification
     c. Keyword overlap calculation
   - Combine scores with weights (0.5, 0.3, 0.2)
   - Determine is_grounded based on thresholds
   - Generate recommendations
   - Return HallucinationResult

3. _llm_verification(self, response: str, context: str) -> Dict:
   - Use LLM to analyze each claim
   - Prompt asks to classify claims as:
     - SUPPORTED: directly in context
     - PARTIALLY_SUPPORTED: inferable from context
     - UNSUPPORTED: not in context
   - Parse JSON response
   - Return: claims list, confidence_score, overall_grounded
   - Handle parsing errors gracefully

4. _verify_citations(self, response: str, context: str) -> Dict:
   - Find all [Source X] citations in response
   - Count sentences with citations
   - Calculate citation coverage (% of sentences cited)
   - Check if cited source numbers are valid
   - Return: citations_found, citation_coverage, valid_citations

5. _calculate_keyword_overlap(self, response: str, context: str) -> float:
   - Extract keywords from response (remove stop words)
   - Extract keywords from context
   - Calculate Jaccard similarity
   - Higher overlap = more likely grounded
   - Return overlap score (0.0 to 1.0)

6. _extract_claims(self, response: str) -> List[str]:
   - Split response into individual claims/sentences
   - Filter out questions and citations
   - Return list of claim strings

7. _generate_recommendations(self, is_grounded: bool, unsupported: List[str], citation_result: Dict) -> List[str]:
   - Generate helpful recommendations based on results
   - Examples:
     - "Verify these claims with your textbook: ..."
     - "Consider adding more citations"
     - "The response may include information not in study materials"

8. quick_check(self, response: str, context: str) -> Tuple[bool, float]:
   - Faster verification using only keyword overlap and citation check
   - Skip LLM verification
   - Return (is_grounded, confidence)
   - Use for streaming or quick feedback

STOP WORDS (define as class constant):
- Common English stop words that shouldn't affect overlap

ERROR HANDLING:
- Handle LLM verification failures (fall back to other methods)
- Handle malformed responses
- Log all verification steps

Add examples showing detected hallucinations vs grounded responses.
```

---

## Prompt 5.2: Create Citation Manager

```
Create src/core/citation_manager.py:

DATACLASS Citation:
- index: int
- document_id: str
- document_name: str
- page_number: Optional[int]
- section_title: Optional[str]
- similarity_score: float
- content_preview: str (first 200 chars of chunk)
- chunk_id: str

CLASS CitationManager:

PURPOSE: Track, validate, and format citations throughout the RAG process

METHODS:

1. __init__(self):
   - Initialize empty citations dict (index -> Citation)
   - Set up logger

2. register_citations(self, retrieval_results: List[Dict]) -> List[Citation]:
   - Take retrieval results and create Citation objects
   - Assign sequential indices (1, 2, 3...)
   - Store in internal dict
   - Return list of created Citations

3. format_citations_for_display(self) -> str:
   - Create formatted string of all citations
   - Format:
     **Sources Referenced:**
     [1] filename.pdf | Page 5 | Section: Introduction | Relevance: 85%
     [2] notes.docx | Page 2 | Relevance: 72%
   - Handle missing metadata gracefully

4. format_citations_markdown(self) -> str:
   - Format citations as markdown list
   - Include content preview in collapsible format

5. format_citations_json(self) -> List[Dict]:
   - Return citations as list of dicts for API response

6. get_citation_by_index(self, index: int) -> Optional[Citation]:
   - Retrieve specific citation

7. get_citation_by_chunk_id(self, chunk_id: str) -> Optional[Citation]:
   - Find citation by chunk ID

8. validate_citations_in_response(self, response: str) -> Dict:
   - Find all [Source X] references in response
   - Check each against registered citations
   - Return:
     - valid: bool (all citations valid)
     - used_citations: List[int]
     - missing_citations: List[int] (referenced but not registered)
     - unused_citations: List[int] (registered but not used)
     - coverage_percentage: float

9. enrich_response_with_citations(self, response: str) -> str:
   - Add formatted citation footnotes to response
   - Add reference section at end
   - Format:
     [response text]
     
     ---
     **References:**
     [1]: document.pdf, Page 5
     [2]: notes.docx, Page 2

10. extract_citations_from_response(self, response: str) -> List[int]:
    - Use regex to find all [Source X] patterns
    - Return list of indices

11. replace_citation_format(self, response: str, format_type: str = "academic") -> str:
    - Replace [Source X] with different format
    - Formats: "academic" (Author, Year), "numeric" ([1]), "footnote" (¹)

12. generate_bibliography(self) -> str:
    - Generate full bibliography from citations
    - Sorted by index or alphabetically

13. clear(self):
    - Clear all registered citations
    - Call at start of new query

PROPERTIES:
- count: int (number of citations)
- citations: Dict[int, Citation] (read-only)

Add example showing full citation workflow from retrieval to display.
```

---

## Prompt 5.3: Update RAG Engine with Hallucination Control

```
Update src/core/rag_engine.py to integrate hallucination detection and citation management:

ADD TO __init__:
- Initialize HallucinationDetector
- Initialize CitationManager

UPDATE query_with_verification method:

def query_with_verification(
    self,
    question: str,
    bloom_level: str = "understand",
    verify_hallucination: bool = True
) -> Dict:
    
    # 1. Get base RAG response
    rag_response = self.query(question, bloom_level)
    
    # 2. Clear and register citations
    self.citation_manager.clear()
    self.citation_manager.register_citations(rag_response.citations)
    
    # 3. Initialize result
    result = {
        'answer': rag_response.answer,
        'citations': self.citation_manager.format_citations_for_display(),
        'citations_json': self.citation_manager.format_citations_json(),
        'confidence': rag_response.confidence,
        'bloom_level': bloom_level,
        'is_grounded': rag_response.is_grounded,
        'sources_count': rag_response.sources_count,
        'hallucination_check': None,
        'enriched_answer': None
    }
    
    # 4. Validate citations in response
    citation_validation = self.citation_manager.validate_citations_in_response(
        rag_response.answer
    )
    result['citation_validation'] = citation_validation
    
    # 5. Perform hallucination check if requested and context exists
    if verify_hallucination and rag_response.context_used:
        hall_result = self.hallucination_detector.check_response(
            response=rag_response.answer,
            context=rag_response.context_used
        )
        
        result['is_grounded'] = hall_result.is_grounded
        result['hallucination_check'] = {
            'confidence_score': hall_result.confidence_score,
            'unsupported_claims': hall_result.unsupported_claims,
            'partially_supported_claims': hall_result.partially_supported_claims,
            'recommendations': hall_result.recommendations,
            'claims_analysis': hall_result.claims
        }
        
        # Add warning if not fully grounded
        if not hall_result.is_grounded:
            result['answer'] = self._add_grounding_warning(
                rag_response.answer,
                hall_result.recommendations
            )
    
    # 6. Enrich answer with formatted citations
    result['enriched_answer'] = self.citation_manager.enrich_response_with_citations(
        result['answer']
    )
    
    return result

ADD new method for streaming with verification:

def query_stream_with_verification(self, question: str, bloom_level: str):
    - Stream answer first
    - Collect full response
    - Run quick hallucination check at end
    - Yield verification results last

ADD new method:

def get_verification_summary(self, result: Dict) -> str:
    - Generate human-readable summary of verification
    - Include confidence, grounding status, warnings
    - Suitable for display to user

Test that integration works correctly with both grounded and ungrounded responses.
```

---

## Prompt 5.4: Test Hallucination Control

```
Create comprehensive tests for hallucination detection:

1. Create tests/unit/test_hallucination_detector.py:

   Test cases:
   
   a. test_fully_grounded_response:
      - Context: "Python is a programming language created by Guido van Rossum"
      - Response: "Python is a programming language [Source 1]. It was created by Guido van Rossum [Source 1]."
      - Expected: is_grounded = True, confidence > 0.8
   
   b. test_hallucinated_response:
      - Context: "Python is a programming language"
      - Response: "Python was created in 1989 and is the most popular language in the world"
      - Expected: is_grounded = False, unsupported_claims not empty
   
   c. test_partially_supported_response:
      - Context: "Machine learning uses algorithms"
      - Response: "Machine learning uses algorithms [Source 1] like neural networks and decision trees"
      - Expected: partially_supported_claims includes extra claims
   
   d. test_no_citations_response:
      - Response without any [Source X] citations
      - Expected: citation_coverage = 0
   
   e. test_keyword_overlap:
      - Test overlap calculation with various inputs

2. Create tests/unit/test_citation_manager.py:

   Test cases:
   - test_register_citations
   - test_format_citations
   - test_validate_citations_in_response
   - test_missing_citation_detection
   - test_enrich_response

3. Create a demo script (scripts/test_hallucination_control.py):

   a. Create a document about a specific topic
   
   b. Test various responses:
      - Fully grounded response (copy from context)
      - Partially grounded (some true, some made up)
      - Completely hallucinated (unrelated facts)
      - Response with proper citations
      - Response without citations
   
   c. Print for each:
      - Original response
      - Is Grounded: Yes/No
      - Confidence Score
      - Unsupported claims (if any)
      - Recommendations

4. Run all tests and demo script, verify hallucination detection works correctly.
```

---

# 📚 PHASE 6: Bloom's Taxonomy Integration

---

## Prompt 6.1: Create Bloom's Taxonomy Module

```
Create src/core/blooms_taxonomy.py:

ENUM BloomLevel:
- REMEMBER = "remember"
- UNDERSTAND = "understand"
- APPLY = "apply"
- ANALYZE = "analyze"
- EVALUATE = "evaluate"
- CREATE = "create"

DATACLASS BloomLevelConfig:
- level: BloomLevel
- name: str (display name)
- description: str (what this level means)
- keywords: List[str] (words that indicate this level)
- question_starters: List[str] (how questions at this level start)
- response_style: str (how to style responses)
- cognitive_process: str (what thinking is involved)

CLASS BloomsTaxonomy:

PURPOSE: Classify questions and adapt responses based on Bloom's Taxonomy

CLASS CONSTANT LEVELS (Dict[BloomLevel, BloomLevelConfig]):

1. REMEMBER:
   - Description: "Recall facts and basic concepts"
   - Keywords: ["define", "list", "name", "state", "identify", "recall", "recognize", "match", "memorize", "label"]
   - Question starters: ["What is...", "List the...", "Define...", "Name the...", "Who was...", "When did..."]
   - Response style: "factual_recall"
   - Cognitive process: "Retrieving relevant knowledge from memory"

2. UNDERSTAND:
   - Description: "Explain ideas or concepts"
   - Keywords: ["explain", "describe", "summarize", "interpret", "classify", "compare", "discuss", "illustrate", "paraphrase"]
   - Question starters: ["Explain how...", "Describe the...", "What does... mean", "Summarize...", "Why does..."]
   - Response style: "explanatory"
   - Cognitive process: "Constructing meaning from information"

3. APPLY:
   - Description: "Use information in new situations"
   - Keywords: ["apply", "demonstrate", "solve", "use", "implement", "calculate", "execute", "show", "compute"]
   - Question starters: ["How would you use...", "Apply the...", "Solve...", "Calculate...", "Demonstrate..."]
   - Response style: "practical_application"
   - Cognitive process: "Carrying out a procedure"

4. ANALYZE:
   - Description: "Draw connections among ideas"
   - Keywords: ["analyze", "compare", "contrast", "examine", "differentiate", "organize", "distinguish", "categorize", "investigate"]
   - Question starters: ["Why does...", "Compare and contrast...", "What is the relationship...", "How does... relate to...", "Analyze..."]
   - Response style: "analytical"
   - Cognitive process: "Breaking material into parts and determining relationships"

5. EVALUATE:
   - Description: "Justify a decision or position"
   - Keywords: ["evaluate", "judge", "critique", "justify", "argue", "defend", "assess", "prioritize", "recommend"]
   - Question starters: ["Do you agree...", "What is the importance...", "Evaluate the...", "Which is better...", "Justify..."]
   - Response style: "evaluative"
   - Cognitive process: "Making judgments based on criteria"

6. CREATE:
   - Description: "Produce new or original work"
   - Keywords: ["create", "design", "develop", "construct", "formulate", "propose", "invent", "compose", "plan"]
   - Question starters: ["Design a...", "How would you create...", "Propose a solution...", "Develop a plan...", "What would happen if..."]
   - Response style: "creative"
   - Cognitive process: "Putting elements together to form a new whole"

METHODS:

1. detect_level(cls, question: str) -> BloomLevel:
   - Analyze question text
   - Score each level based on keyword matches
   - Consider question starters
   - Return highest scoring level
   - Default to UNDERSTAND if unclear

2. get_level_config(cls, level: BloomLevel) -> BloomLevelConfig:
   - Return configuration for level

3. get_response_guidelines(cls, level: BloomLevel) -> str:
   - Return detailed guidelines for how to respond at this level
   - Include formatting suggestions
   - Include what to include/avoid

4. generate_practice_questions(cls, topic: str, level: BloomLevel, count: int = 3) -> List[str]:
   - Generate practice questions for a topic at specified level
   - Use question starters as templates
   - Return list of questions

5. get_all_levels_info(cls) -> List[Dict]:
   - Return info about all levels for display

6. suggest_higher_level_question(cls, current_question: str, current_level: BloomLevel) -> str:
   - Suggest a higher-order thinking question on same topic
   - Help students progress in their understanding

Add comprehensive docstrings explaining Bloom's Taxonomy and its educational purpose.
```

---

## Prompt 6.2: Create Exam Helper Service

```
Create src/services/exam_helper.py:

CLASS ExamHelperService:

PURPOSE: Provide exam-focused learning features using RAG and Bloom's Taxonomy

METHODS:

1. __init__(self, rag_engine: RAGEngine):
   - Store RAG engine reference
   - Initialize BloomsTaxonomy reference
   - Set up logger

2. get_answer_for_exam(self, question: str, bloom_level: Optional[str] = None, auto_detect: bool = True) -> Dict:
   - Main method for exam-style answers
   - If auto_detect and no level provided: detect level from question
   - Get answer using RAG with appropriate level
   - Add exam-specific enhancements:
     - Bloom's level info
     - Practice questions at same level
     - Study tips for this question type
   - Return comprehensive result

3. generate_study_guide(self, topics: List[str], levels: List[str] = None) -> Dict:
   - Generate comprehensive study guide
   - For each topic, for each level:
     - Get relevant content from documents
     - Generate level-appropriate explanation
     - Add practice questions
   - Structure output as:
     {
       'topics': [
         {
           'topic': 'Topic Name',
           'sections': [
             {'level': 'remember', 'content': '...', 'practice_questions': [...]}
           ]
         }
       ]
     }

4. get_key_concepts(self, topic: str) -> Dict:
   - Extract key concepts for a topic
   - Use REMEMBER level query
   - Return: topic, key_concepts, definitions, citations

5. explain_concept(self, concept: str, depth: str = "basic") -> Dict:
   - Explain a concept at specified depth
   - "basic" = UNDERSTAND level
   - "detailed" = ANALYZE level
   - Return explanation with examples

6. generate_practice_test(self, topics: List[str], questions_per_topic: int = 3, levels: List[str] = None) -> Dict:
   - Generate practice questions for topics
   - Mix of specified Bloom's levels
   - Return:
     {
       'questions': [
         {'question': '...', 'topic': '...', 'bloom_level': '...', 'suggested_answer_points': [...]}
       ],
       'total_questions': int,
       'estimated_time_minutes': int
     }

7. get_topic_summary(self, topic: str) -> Dict:
   - Quick summary of a topic
   - Key points
   - Related concepts
   - Recommended study approach

8. compare_concepts(self, concept1: str, concept2: str) -> Dict:
   - Compare and contrast two concepts
   - Use ANALYZE level
   - Return similarities, differences, relationships

9. get_study_tips(self, bloom_level: str) -> List[str]:
   - Return study tips for mastering this cognitive level
   - E.g., for REMEMBER: "Use flashcards", "Create mnemonics"

10. assess_answer(self, question: str, student_answer: str) -> Dict:
    - Compare student answer against model answer from documents
    - Identify missing points
    - Provide feedback
    - Return: score estimate, missing_points, feedback, suggestions

HELPER METHODS:

11. _extract_topic_from_question(self, question: str) -> str:
    - Extract main topic from question text
    - Use for generating related content

12. _format_for_exam(self, content: str, level: str) -> str:
    - Format content appropriately for exam context
    - Add structure based on level

Add examples showing each method's usage for exam preparation scenarios.
```

---

## Prompt 6.3: Test Bloom's Taxonomy Integration

```
Create tests for Bloom's Taxonomy:

1. Create tests/unit/test_blooms_taxonomy.py:

   Test cases:
   
   a. test_detect_remember_level:
      - "Define photosynthesis" → REMEMBER
      - "List the planets" → REMEMBER
      - "What is a variable?" → REMEMBER
   
   b. test_detect_understand_level:
      - "Explain how photosynthesis works" → UNDERSTAND
      - "Describe the water cycle" → UNDERSTAND
      - "Why do plants need sunlight?" → UNDERSTAND
   
   c. test_detect_apply_level:
      - "Calculate the area of a circle with radius 5" → APPLY
      - "How would you solve this equation?" → APPLY
      - "Demonstrate the process" → APPLY
   
   d. test_detect_analyze_level:
      - "Compare and contrast mitosis and meiosis" → ANALYZE
      - "What is the relationship between X and Y?" → ANALYZE
      - "Analyze the causes of WWI" → ANALYZE
   
   e. test_generate_practice_questions:
      - Generate questions for "Machine Learning" at UNDERSTAND level
      - Verify questions start with appropriate starters
   
   f. test_get_response_guidelines:
      - Each level returns different guidelines

2. Create tests/integration/test_exam_helper.py:

   Test cases:
   - test_get_answer_for_exam with auto-detect
   - test_generate_study_guide
   - test_get_key_concepts
   - test_generate_practice_test

3. Create demo script (scripts/test_blooms.py):

   a. Create a test document about a clear subject (e.g., "Cell Biology")
   
   b. Test questions at different levels:
      - REMEMBER: "What are the parts of a cell?"
      - UNDERSTAND: "Explain the function of mitochondria"
      - APPLY: "How would you identify a cell type under microscope?"
      - ANALYZE: "Compare plant and animal cells"
   
   c. For each, print:
      - Detected Bloom's level
      - Response style
      - Generated answer (excerpt)
      - Practice questions
   
   d. Generate a mini study guide for the topic

4. Run all tests and demo, verify:
   - Level detection is accurate
   - Responses vary appropriately by level
   - Practice questions are relevant

Show output and confirm Bloom's integration works.
```

---

# 🔌 PHASE 7: Backend API Development

---

## Prompt 7.1: Create API Models

```
Create src/api/models.py with all Pydantic models for the API:

ENUMS:

1. BloomLevelEnum:
   - remember, understand, apply, analyze, evaluate, create

REQUEST MODELS:

2. DocumentUploadRequest:
   - subject: Optional[str]
   - course: Optional[str]
   - tags: List[str] = []

3. QueryRequest:
   - question: str (min 3 chars, max 1000 chars)
   - bloom_level: Optional[BloomLevelEnum]
   - auto_detect_level: bool = True
   - document_filter: Optional[str] (filter by document_id)
   - verify_hallucination: bool = True
   - include_citations: bool = True

4. StudyGuideRequest:
   - topics: List[str] (min 1, max 10 items)
   - levels: List[BloomLevelEnum] = [remember, understand, apply]

5. PracticeTestRequest:
   - topics: List[str]
   - questions_per_topic: int = 3
   - levels: List[BloomLevelEnum]

RESPONSE MODELS:

6. CitationResponse:
   - index: int
   - document_name: str
   - page_number: Optional[int]
   - section_title: Optional[str]
   - similarity: float
   - content_preview: Optional[str]

7. HallucinationCheckResponse:
   - is_grounded: bool
   - confidence_score: float
   - unsupported_claims: List[str]
   - recommendations: List[str]

8. QueryResponse:
   - answer: str
   - enriched_answer: str (with citations formatted)
   - citations: List[CitationResponse]
   - bloom_level: str
   - bloom_description: str
   - confidence: float
   - is_grounded: bool
   - hallucination_check: Optional[HallucinationCheckResponse]
   - practice_questions: List[str]
   - processing_time: float
   - sources_count: int

9. DocumentResponse:
   - document_id: str
   - filename: str
   - file_type: str
   - file_size: int
   - chunks_count: int
   - upload_time: datetime
   - status: str
   - subject: Optional[str]
   - course: Optional[str]

10. DocumentListResponse:
    - documents: List[DocumentResponse]
    - total_count: int

11. StudyGuideResponse:
    - topics: List[TopicSection]
    - generated_at: datetime
    - total_sections: int

12. TopicSection:
    - topic: str
    - sections: List[LevelSection]

13. LevelSection:
    - level: str
    - content: str
    - practice_questions: List[str]
    - citations: List[CitationResponse]

14. HealthResponse:
    - status: str
    - version: str
    - vector_db_status: str
    - documents_indexed: int
    - uptime_seconds: float

15. ErrorResponse:
    - error: str
    - detail: str
    - status_code: int

Add Config class to each model for JSON serialization.
Add validators where appropriate (e.g., question length, topic count limits).
Add examples in Field() for API documentation.
```

---

## Prompt 7.2: Create FastAPI Application

```
Create src/api/main.py - The main FastAPI application:

SETUP:
- Import all dependencies
- Initialize FastAPI app with:
  - title: "AI Study Assistant API"
  - description: "Exam-focused Generative AI Study Assistant with RAG and Citation Control"
  - version: "1.0.0"
- Add CORS middleware (allow all origins for development)
- Initialize services:
  - ConfigLoader
  - DocumentService
  - RAGEngine
  - ExamHelperService
- Create upload directory
- Track start time for uptime

ENDPOINTS:

1. GET /health
   - Return HealthResponse
   - Check vector store connection
   - Include version, status, document count

2. GET /
   - Return welcome message and API info
   - Link to /docs

3. POST /documents/upload
   - Accept file upload (multipart/form-data)
   - Accept optional subject, course query params
   - Validate file type and size
   - Process document
   - Index in vector store
   - Return DocumentResponse
   - Handle errors with appropriate status codes

4. GET /documents
   - Return DocumentListResponse
   - List all uploaded documents

5. GET /documents/{document_id}
   - Return specific DocumentResponse
   - 404 if not found

6. DELETE /documents/{document_id}
   - Delete document and its vectors
   - Return success message

7. POST /query
   - Accept QueryRequest
   - Process through ExamHelperService
   - Return QueryResponse
   - Handle insufficient context gracefully

8. POST /query/stream
   - Accept QueryRequest
   - Return StreamingResponse (Server-Sent Events)
   - Stream answer chunks
   - End with citations and metadata

9. POST /study-guide
   - Accept StudyGuideRequest
   - Generate comprehensive study guide
   - Return StudyGuideResponse

10. POST /practice-test
    - Accept PracticeTestRequest
    - Generate practice questions
    - Return practice test data

11. GET /key-concepts/{topic}
    - Extract key concepts for topic
    - Return concepts with citations

12. GET /bloom-levels
    - Return information about all Bloom's levels
    - Useful for UI dropdowns

ERROR HANDLING:
- Global exception handler
- Return ErrorResponse for all errors
- Log all errors
- Don't expose internal details in production

STARTUP EVENT:
- Log startup message
- Verify all services initialized
- Log configuration summary

SHUTDOWN EVENT:
- Persist vector store
- Log shutdown message

Add if __name__ == "__main__" block to run with uvicorn.
```

---

## Prompt 7.3: Create API Routers (Modular)

```
Split the API into modular routers for better organization:

1. Create src/api/routers/documents.py:

   Router prefix: "/documents"
   Tags: ["Documents"]
   
   Endpoints:
   - POST / (upload)
   - GET / (list all)
   - GET /{document_id} (get one)
   - DELETE /{document_id} (delete)
   - GET /{document_id}/chunks (get document chunks)
   - GET /{document_id}/stats (get document statistics)

2. Create src/api/routers/query.py:

   Router prefix: "/query"
   Tags: ["Query"]
   
   Endpoints:
   - POST / (standard query)
   - POST /stream (streaming query)
   - POST /quick (quick answer without verification)
   - GET /history (if we implement history)

3. Create src/api/routers/study.py:

   Router prefix: "/study"
   Tags: ["Study Tools"]
   
   Endpoints:
   - POST /guide (generate study guide)
   - POST /practice-test (generate practice test)
   - GET /key-concepts/{topic}
   - POST /compare (compare two concepts)
   - GET /tips/{bloom_level} (study tips)

4. Create src/api/routers/bloom.py:

   Router prefix: "/bloom"
   Tags: ["Bloom's Taxonomy"]
   
   Endpoints:
   - GET /levels (list all levels)
   - GET /levels/{level} (get level details)
   - POST /detect (detect level from question)
   - POST /practice-questions (generate practice questions)

5. Update src/api/main.py:
   - Import all routers
   - Include routers with prefixes
   - Keep only /health and / endpoints in main

6. Create src/api/dependencies.py:
   - Shared dependencies for routers
   - get_config() dependency
   - get_document_service() dependency
   - get_rag_engine() dependency
   - get_exam_helper() dependency

This modular structure allows easier maintenance and testing.
```

---

## Prompt 7.4: Test API Endpoints

```
Create comprehensive API tests:

1. Create tests/integration/test_api.py:

   Setup:
   - Use TestClient from fastapi.testclient
   - Create test fixtures

   Test cases:

   a. test_health_check:
      - GET /health returns 200
      - Response has required fields

   b. test_upload_document:
      - Create test PDF or TXT file
      - POST /documents/upload
      - Verify 200 response
      - Verify document_id returned
      - Verify chunks_count > 0

   c. test_upload_invalid_file:
      - Upload .exe file
      - Verify 400 response

   d. test_list_documents:
      - Upload a document first
      - GET /documents
      - Verify document in list

   e. test_get_document:
      - GET /documents/{id}
      - Verify correct document returned

   f. test_delete_document:
      - DELETE /documents/{id}
      - Verify success
      - Verify GET returns 404

   g. test_query_with_documents:
      - Upload document
      - POST /query with relevant question
      - Verify answer returned
      - Verify citations present

   h. test_query_without_documents:
      - POST /query with no documents
      - Verify appropriate response

   i. test_query_bloom_levels:
      - Test with each Bloom's level
      - Verify response includes level info

   j. test_study_guide:
      - POST /study/guide
      - Verify response structure

   k. test_bloom_endpoints:
      - GET /bloom/levels
      - POST /bloom/detect

2. Create scripts/test_api_manual.py:
   - Start server
   - Run manual tests with requests library
   - Print formatted results

3. Run tests:
   - pytest tests/integration/test_api.py -v
   - Show results

Verify all endpoints work correctly before moving to frontend.
```

---

# 🖥️ PHASE 8: Frontend Interface (Streamlit)

---

## Prompt 8.1: Create Main Streamlit Application

```
Create frontend/app.py - The main Streamlit application:

PAGE CONFIG:
- Title: "AI Study Assistant"
- Icon: 📚
- Layout: wide
- Sidebar: expanded

CUSTOM CSS:
- Style for main header
- Style for citation boxes
- Confidence indicator colors (green/yellow/red)
- Bloom's level badges
- Warning boxes
- Card-like containers

GLOBAL STATE (st.session_state):
- api_url: str (default http://localhost:8000)
- auto_detect_bloom: bool (default True)
- verify_hallucination: bool (default True)
- show_citations: bool (default True)
- chat_history: List

MAIN FUNCTION:
1. Render header with title and description
2. Render sidebar
3. Render main content with tabs:
   - Tab 1: Ask Questions
   - Tab 2: Study Guide
   - Tab 3: Practice Test
   - Tab 4: Analytics

SIDEBAR CONTENTS:
1. Document Management section:
   - File uploader (PDF, DOCX, TXT)
   - Subject and Course inputs
   - Upload button
   - Progress indicator
   
2. Uploaded Documents list:
   - Show each document with expander
   - Display: filename, chunks, upload time
   - Delete button for each

3. Settings section:
   - Auto-detect Bloom's level checkbox
   - Enable hallucination check checkbox
   - Show detailed citations checkbox
   - API URL input (for development)

HELPER FUNCTIONS:
- api_request(endpoint, method, data): Make API calls
- render_document_upload(): Document upload UI
- render_document_list(): List documents
- render_settings(): Settings UI
- show_error(message): Display error
- show_success(message): Display success

ERROR HANDLING:
- Handle API connection errors
- Show friendly error messages
- Retry logic for failed requests

Add loading spinners for all API calls.
```

---

## Prompt 8.2: Create Query Interface

```
Add to frontend/app.py - The query interface (Tab 1):

FUNCTION render_query_interface():

1. HEADER:
   - "💬 Ask Questions About Your Study Materials"
   - Brief instruction text

2. BLOOM'S LEVEL SELECTOR:
   - Create two columns
   - Left (larger): Question input
   - Right (smaller): Bloom's level
   
   If auto-detect enabled:
     - Show info message "Level will be auto-detected"
   Else:
     - Show selectbox with levels:
       🧠 Remember, 💡 Understand, 🔧 Apply, 
       🔍 Analyze, ⚖️ Evaluate, 🎨 Create
     - Show description of selected level

3. QUESTION INPUT:
   - Text area (height: 100px)
   - Placeholder: "Enter your study question here..."
   - Character counter

4. SUBMIT BUTTON:
   - "🔍 Get Answer" (primary button)
   - Full width
   - Disabled if question empty

5. ON SUBMIT:
   - Show spinner "Searching study materials..."
   - Make API call to /query
   - Handle errors
   - Call render_answer() with response

FUNCTION render_answer(result: Dict):

1. METRICS ROW (3 columns):
   - Bloom's Level: with icon
   - Confidence: percentage with color
   - Processing Time: seconds

2. GROUNDING STATUS:
   - If not grounded: Show warning box
   - "⚠️ Some parts may not be fully supported..."

3. ANSWER SECTION:
   - Header "### Answer"
   - Display enriched_answer (with citations embedded)
   - Use markdown rendering

4. SOURCES/CITATIONS:
   - Collapsible section "📚 Sources"
   - For each citation:
     - Index, document name, page, section
     - Relevance percentage bar
     - Content preview (truncated)

5. HALLUCINATION CHECK DETAILS:
   - Collapsible expander "🔍 Verification Details"
   - Confidence score
   - Unsupported claims (if any) in red
   - Recommendations

6. PRACTICE QUESTIONS:
   - Collapsible expander "📝 Practice Questions"
   - List generated practice questions
   - Button to "Try this question" (fills input)

7. FEEDBACK BUTTONS:
   - Thumbs up / Thumbs down
   - "Copy answer" button

Make the interface clean, intuitive, and informative.
```

---

## Prompt 8.3: Create Study Guide Interface

```
Add to frontend/app.py - Study Guide interface (Tab 2):

FUNCTION render_study_guide_interface():

1. HEADER:
   - "📖 Generate Study Guide"
   - Description: "Create comprehensive study materials for your topics"

2. TOPIC INPUT:
   - Text area for topics (one per line)
   - Placeholder with example topics
   - Helper text: "Enter topics separated by new lines"

3. BLOOM'S LEVEL SELECTION:
   - Subheader "Select Cognitive Levels to Include"
   - 3 columns of checkboxes:
     - Column 1: Remember ✓, Understand ✓
     - Column 2: Apply ✓, Analyze
     - Column 3: Evaluate, Create
   - At least one must be selected

4. GENERATE BUTTON:
   - "📚 Generate Study Guide"
   - Show estimated time based on topics/levels

5. ON GENERATE:
   - Validate at least 1 topic and 1 level
   - Show progress bar
   - Make API call to /study/guide
   - Render results

6. RENDER STUDY GUIDE:
   
   For each topic:
   a. Topic Header:
      - "📌 {topic name}"
      - Divider line
   
   b. For each level section:
      - Expander with level name and icon
      - Content formatted with markdown
      - Citations inline
      - Practice questions at end of section
   
   c. Visual separation between topics

7. EXPORT OPTIONS:
   - "📥 Download as PDF" button
   - "📥 Download as Markdown" button
   - "📋 Copy to Clipboard" button

8. STUDY TIPS SIDEBAR:
   - Show tips based on selected levels
   - E.g., "For Remember level: Use flashcards..."

Handle loading states and errors gracefully.
```

---

## Prompt 8.4: Create Practice Test & Analytics

```
Add to frontend/app.py - Practice Test (Tab 3) and Analytics (Tab 4):

=== PRACTICE TEST TAB ===

FUNCTION render_practice_test_interface():

1. HEADER:
   - "📝 Generate Practice Test"

2. CONFIGURATION:
   a. Topics input (same as study guide)
   b. Questions per topic: number input (1-10, default 3)
   c. Bloom's levels: checkboxes
   d. Estimated time display

3. GENERATE BUTTON:
   - "🎯 Generate Practice Test"

4. RENDER PRACTICE TEST:
   
   a. Test Header:
      - Total questions
      - Estimated completion time
      - Instructions
   
   b. For each question:
      - Question number and bloom level badge
      - Question text in box
      - "Show Suggested Answer Points" collapsible
      - Space for student notes (text area)
   
   c. Progress indicator (X of Y questions)

5. ACTIONS:
   - "🔄 Generate New Test" button
   - "📥 Export Test" button
   - "📥 Export with Answers" button

=== ANALYTICS TAB ===

FUNCTION render_analytics():

1. HEADER:
   - "📊 Study Analytics & System Status"

2. SYSTEM STATUS (from /health):
   - 3 metric columns:
     - System Status: 🟢 Healthy
     - Vector DB: Connected
     - Total Chunks: number

3. DOCUMENT STATISTICS:
   - Total documents uploaded
   - Total chunks indexed
   - Breakdown by subject/course (if tagged)
   - Pie chart of document types

4. USAGE STATISTICS (if implemented):
   - Questions asked today
   - Most queried topics
   - Average confidence score

5. BLOOM'S LEVEL DISTRIBUTION:
   - Bar chart showing questions by level
   - (Requires tracking query history)

6. QUICK ACTIONS:
   - "🔄 Refresh Statistics"
   - "🗑️ Clear All Documents" (with confirmation)
   - "💾 Export Data"

Use st.metric for key numbers.
Use st.plotly_chart or st.bar_chart for visualizations.
```

---

## Prompt 8.5: Create UI Components Module

```
Create frontend/components/ui_components.py - Reusable UI components:

1. FUNCTION render_citation_card(citation: Dict):
   - Styled container with:
     - Source index badge
     - Document name
     - Page/Section info
     - Relevance bar (visual)
     - Preview text (truncated)
   - Returns None (renders directly)

2. FUNCTION render_confidence_indicator(score: float):
   - Green (>0.8): "High Confidence"
   - Yellow (0.6-0.8): "Medium Confidence"  
   - Red (<0.6): "Low Confidence"
   - Progress bar with color
   - Score percentage

3. FUNCTION render_bloom_badge(level: str):
   - Colored badge based on level
   - Icon + level name
   - Tooltip with description

4. FUNCTION render_grounding_warning(recommendations: List[str]):
   - Warning box with icon
   - List of recommendations
   - Link to "Learn more about verification"

5. FUNCTION render_loading_skeleton():
   - Placeholder boxes while loading
   - Animated shimmer effect

6. FUNCTION render_empty_state(message: str, icon: str = "📭"):
   - Centered message
   - Icon
   - Call-to-action suggestion

7. FUNCTION render_error_message(error: str, details: str = None):
   - Red error box
   - Error message
   - Collapsible details (for debugging)
   - "Try again" suggestion

8. FUNCTION render_success_message(message: str):
   - Green success box
   - Auto-dismiss after 3 seconds (using st.empty())

9. FUNCTION render_document_card(doc: Dict):
   - Card with document info
   - Icon based on file type
   - Key stats (chunks, size)
   - Action buttons

10. FUNCTION render_question_card(question: Dict):
    - Question text
    - Bloom's level badge
    - Topic tag
    - Expandable answer section

11. FUNCTION create_download_button(content: str, filename: str, mime: str):
    - Download button with proper mime type
    - Handles different formats

CSS_STYLES constant:
- All custom CSS used by components
- Call st.markdown(CSS_STYLES, unsafe_allow_html=True) once

Update frontend/app.py to use these components.
```

---

## Prompt 8.6: Test Frontend

```
Test the Streamlit frontend thoroughly:

1. MANUAL TESTING CHECKLIST:

   a. Sidebar - Documents:
      [ ] Upload PDF file - verify success message
      [ ] Upload TXT file - verify success message
      [ ] Upload invalid file - verify error message
      [ ] View uploaded documents list
      [ ] Delete a document - verify removal
   
   b. Sidebar - Settings:
      [ ] Toggle auto-detect Bloom's - verify behavior
      [ ] Toggle hallucination check - verify behavior
      [ ] Toggle show citations - verify display
   
   c. Query Tab:
      [ ] Ask question with documents - verify answer
      [ ] Ask question without documents - verify message
      [ ] Select different Bloom's levels - verify responses differ
      [ ] Verify citations display correctly
      [ ] Verify confidence indicator
      [ ] Verify practice questions appear
      [ ] Test "Copy answer" functionality
   
   d. Study Guide Tab:
      [ ] Enter multiple topics
      [ ] Select different levels
      [ ] Generate guide - verify structure
      [ ] Test export buttons
   
   e. Practice Test Tab:
      [ ] Configure test parameters
      [ ] Generate test - verify questions
      [ ] Verify answer hints
   
   f. Analytics Tab:
      [ ] Verify system status displays
      [ ] Verify statistics load

2. Create a test script (scripts/run_frontend_test.py):
   - Automatically start API server
   - Start Streamlit app
   - Print URLs for testing
   - Wait for user input to stop

3. Run the test:
   - Start backend: uvicorn src.api.main:app --reload
   - Start frontend: streamlit run frontend/app.py
   - Test all functionality manually
   - Note any issues

4. Fix any issues found during testing

Report the status of each test item.
```

---

# 🧪 PHASE 9: Testing & Quality Assurance

---

## Prompt 9.1: Complete Unit Tests

```
Create comprehensive unit tests for all components:

1. tests/unit/test_document_models.py:
   - Test DocumentMetadata validation
   - Test DocumentChunk validation
   - Test ProcessedDocument creation
   - Test enum values

2. tests/unit/test_pdf_processor.py:
   - Test text extraction (mock PDF)
   - Test table extraction
   - Test metadata extraction
   - Test error handling for invalid PDF

3. tests/unit/test_docx_processor.py:
   - Test text extraction
   - Test heading detection
   - Test table extraction

4. tests/unit/test_text_chunker.py:
   - Test chunk size limits
   - Test overlap calculation
   - Test section detection
   - Test minimum chunk filtering
   - Test edge cases (empty text, very long text)

5. tests/unit/test_embedding_service.py:
   - Test embedding generation
   - Test batch embedding
   - Test similarity calculation
   - Test dimension consistency

6. tests/unit/test_hallucination_detector.py:
   - Test fully grounded response
   - Test hallucinated response
   - Test citation verification
   - Test keyword overlap
   - Test recommendation generation

7. tests/unit/test_citation_manager.py:
   - Test citation registration
   - Test formatting methods
   - Test validation
   - Test enrichment

8. tests/unit/test_blooms_taxonomy.py:
   - Test level detection for all levels
   - Test practice question generation
   - Test response guidelines

Create pytest fixtures in tests/conftest.py:
- sample_document fixture
- sample_chunks fixture
- mock_llm_response fixture
- test_config fixture

Run all unit tests and ensure >80% coverage:
pytest tests/unit/ -v --cov=src --cov-report=html
```

---

## Prompt 9.2: Complete Integration Tests

```
Create comprehensive integration tests:

1. tests/integration/test_document_pipeline.py:
   - Test full document processing flow
   - Upload → Process → Chunk → Index
   - Verify chunks are searchable

2. tests/integration/test_retrieval_pipeline.py:
   - Test indexing documents
   - Test semantic search
   - Test filtering by document
   - Test similarity thresholds

3. tests/integration/test_rag_pipeline.py:
   - Test full RAG query flow
   - Test with sufficient context
   - Test with insufficient context
   - Test different Bloom's levels
   - Test hallucination detection integration

4. tests/integration/test_api_documents.py:
   - Test POST /documents/upload
   - Test GET /documents
   - Test GET /documents/{id}
   - Test DELETE /documents/{id}

5. tests/integration/test_api_query.py:
   - Test POST /query with valid data
   - Test POST /query with invalid data
   - Test query with different parameters
   - Test streaming endpoint

6. tests/integration/test_api_study.py:
   - Test POST /study/guide
   - Test POST /study/practice-test
   - Test GET /study/key-concepts

7. tests/integration/test_end_to_end.py:
   - Full user journey test:
     1. Upload document
     2. Query document
     3. Generate study guide
     4. Generate practice test
     5. Delete document
   - Verify all steps work together

Create test fixtures in tests/integration/conftest.py:
- test_client fixture (FastAPI TestClient)
- sample_pdf_file fixture
- indexed_document fixture

Run integration tests:
pytest tests/integration/ -v
```

---

## Prompt 9.3: Create Test Configuration

```
Set up test configuration:

1. Create pytest.ini:
   [pytest]
   testpaths = tests
   python_files = test_*.py
   python_classes = Test*
   python_functions = test_*
   asyncio_mode = auto
   addopts = -v --tb=short --strict-markers
   markers =
       unit: Unit tests
       integration: Integration tests
       slow: Slow running tests
       api: API tests

2. Create tests/conftest.py (root):
   - Import all fixtures
   - Set up test environment variables
   - Create temporary directories for tests
   - Clean up after tests

3. Create .coveragerc:
   [run]
   source = src
   omit = 
       tests/*
       */__pycache__/*
       */migrations/*
   
   [report]
   exclude_lines =
       pragma: no cover
       def __repr__
       raise NotImplementedError
   
   [html]
   directory = htmlcov

4. Create scripts/run_tests.sh:
   #!/bin/bash
   
   echo "Running unit tests..."
   pytest tests/unit/ -v --cov=src
   
   echo "Running integration tests..."
   pytest tests/integration/ -v
   
   echo "Generating coverage report..."
   coverage html
   
   echo "Tests complete. Coverage report at htmlcov/index.html"

5. Run full test suite and generate report:
   - Execute run_tests.sh
   - Show test results summary
   - Show coverage percentage
   - List any failing tests

Target: >80% code coverage, all tests passing.
```

---

## Prompt 9.4: Code Quality Checks

```
Set up code quality tools and run checks:

1. Create pyproject.toml with tool configurations:

   [tool.black]
   line-length = 100
   target-version = ['py311']
   
   [tool.isort]
   profile = "black"
   line_length = 100
   
   [tool.mypy]
   python_version = "3.11"
   warn_return_any = true
   warn_unused_configs = true
   ignore_missing_imports = true

2. Create .flake8:
   [flake8]
   max-line-length = 100
   exclude = .git,__pycache__,build,dist,venv
   ignore = E203,W503

3. Add to requirements.txt (dev dependencies):
   black
   isort
   flake8
   mypy
   pre-commit

4. Create .pre-commit-config.yaml:
   repos:
     - repo: https://github.com/psf/black
       hooks:
         - id: black
     - repo: https://github.com/pycqa/isort
       hooks:
         - id: isort
     - repo: https://github.com/pycqa/flake8
       hooks:
         - id: flake8

5. Run code quality checks:
   - black src/ --check (formatting)
   - isort src/ --check (import sorting)
   - flake8 src/ (linting)
   - mypy src/ (type checking)

6. Fix any issues found

7. Create scripts/lint.sh:
   #!/bin/bash
   echo "Running Black..."
   black src/ tests/
   echo "Running isort..."
   isort src/ tests/
   echo "Running flake8..."
   flake8 src/
   echo "Running mypy..."
   mypy src/
   echo "Done!"

Run all checks and show results.
```

---

# 🚀 PHASE 10: Deployment & Documentation

---

## Prompt 10.1: Create Docker Configuration

```
Create Docker configuration for deployment:

1. Create Dockerfile:
   
   FROM python:3.11-slim
   
   # Set working directory
   WORKDIR /app
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       build-essential \
       curl \
       && rm -rf /var/lib/apt/lists/*
   
   # Copy requirements first (for caching)
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Download spacy model
   RUN python -m spacy download en_core_web_sm
   
   # Copy application code
   COPY . .
   
   # Create necessary directories
   RUN mkdir -p data/uploads data/processed data/vectordb logs
   
   # Expose ports
   EXPOSE 8000 8501
   
   # Health check
   HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
       CMD curl -f http://localhost:8000/health || exit 1
   
   # Default command (API server)
   CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

2. Create docker-compose.yml:
   
   version: '3.8'
   
   services:
     api:
       build: .
       ports:
         - "8000:8000"
       volumes:
         - ./data:/app/data
         - ./logs:/app/logs
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - ENVIRONMENT=production
         - LOG_LEVEL=INFO
       restart: unless-stopped
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
         interval: 30s
         timeout: 10s
         retries: 3
     
     frontend:
       build: .
       command: streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
       ports:
         - "8501:8501"
       environment:
         - API_URL=http://api:8000
       depends_on:
         api:
           condition: service_healthy
       restart: unless-stopped
   
   volumes:
     data:
     logs:

3. Create .dockerignore:
   .git
   .gitignore
   __pycache__
   *.pyc
   .env
   venv/
   .pytest_cache/
   htmlcov/
   *.egg-info/
   .mypy_cache/

4. Test Docker build:
   docker-compose build
   docker-compose up

Verify both services start correctly.
```

---

## Prompt 10.2: Create Deployment Scripts

```
Create deployment and management scripts:

1. Create scripts/deploy.sh:
   #!/bin/bash
   set -e
   
   echo "🚀 Deploying AI Study Assistant..."
   
   # Check for required environment variables
   if [ -z "$OPENAI_API_KEY" ]; then
       echo "Error: OPENAI_API_KEY not set"
       exit 1
   fi
   
   # Pull latest code (if using git)
   echo "📥 Pulling latest changes..."
   git pull origin main || true
   
   # Build containers
   echo "🔨 Building containers..."
   docker-compose build
   
   # Stop existing containers
   echo "⏹️ Stopping existing containers..."
   docker-compose down
   
   # Start new containers
   echo "▶️ Starting containers..."
   docker-compose up -d
   
   # Wait for health check
   echo "⏳ Waiting for services to be healthy..."
   sleep 10
   
   # Check status
   docker-compose ps
   
   echo "✅ Deployment complete!"
   echo "📊 API: http://localhost:8000"
   echo "🖥️ Frontend: http://localhost:8501"
   echo "📚 API Docs: http://localhost:8000/docs"

2. Create scripts/stop.sh:
   #!/bin/bash
   echo "Stopping AI Study Assistant..."
   docker-compose down
   echo "Stopped."

3. Create scripts/logs.sh:
   #!/bin/bash
   # View logs for specified service or all
   SERVICE=${1:-""}
   if [ -z "$SERVICE" ]; then
       docker-compose logs -f
   else
       docker-compose logs -f $SERVICE
   fi

4. Create scripts/backup.sh:
   #!/bin/bash
   BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
   mkdir -p $BACKUP_DIR
   
   echo "Backing up data..."
   cp -r data/vectordb $BACKUP_DIR/
   cp -r data/uploads $BACKUP_DIR/
   
   echo "Backup complete: $BACKUP_DIR"

5. Create scripts/restore.sh:
   #!/bin/bash
   BACKUP_DIR=$1
   
   if [ -z "$BACKUP_DIR" ]; then
       echo "Usage: ./restore.sh <backup_directory>"
       exit 1
   fi
   
   echo "Restoring from $BACKUP_DIR..."
   cp -r $BACKUP_DIR/vectordb data/
   cp -r $BACKUP_DIR/uploads data/
   echo "Restore complete."

6. Create scripts/dev.sh:
   #!/bin/bash
   # Development mode - run without Docker
   
   # Terminal 1: API
   echo "Starting API server..."
   uvicorn src.api.main:app --reload --port 8000 &
   
   # Terminal 2: Frontend
   echo "Starting Streamlit..."
   streamlit run frontend/app.py &
   
   echo "Development servers started."
   echo "API: http://localhost:8000"
   echo "Frontend: http://localhost:8501"
   
   wait

Make all scripts executable: chmod +x scripts/*.sh
```

---

## Prompt 10.3: Create Documentation

```
Create comprehensive documentation:

1. Create README.md (root):
   
   # 📚 AI Study Assistant
   
   Exam-focused Generative AI Study Assistant with RAG and Citation Control
   
   ## Features
   - Upload PDF, DOCX, TXT study materials
   - Ask questions answered from YOUR materials only
   - Automatic citations with page/section references
   - Hallucination detection and warnings
   - Bloom's Taxonomy adaptive responses
   - Study guide generation
   - Practice test creation
   
   ## Quick Start
   
   ### Prerequisites
   - Python 3.11+
   - OpenAI API key
   - Docker (optional)
   
   ### Installation
   ```bash
   git clone <repo>
   cd study_assistant
   pip install -r requirements.txt
   cp configs/.env.example configs/.env
   # Add your OPENAI_API_KEY to .env
   ```
   
   ### Run with Docker
   ```bash
   docker-compose up
   ```
   
   ### Run without Docker
   ```bash
   # Terminal 1
   uvicorn src.api.main:app --reload
   
   # Terminal 2
   streamlit run frontend/app.py
   ```
   
   ## Access
   - Frontend: http://localhost:8501
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   
   ## Documentation
   - [User Guide](docs/USER_GUIDE.md)
   - [API Documentation](http://localhost:8000/docs)
   - [Developer Guide](docs/DEVELOPER_GUIDE.md)
   
   ## License
   MIT

2. Create docs/USER_GUIDE.md:
   - How to upload documents
   - How to ask questions
   - Understanding Bloom's levels
   - Using study guide feature
   - Using practice tests
   - Understanding citations
   - Understanding confidence scores
   - Troubleshooting

3. Create docs/DEVELOPER_GUIDE.md:
   - Architecture overview
   - Component descriptions
   - How to extend
   - Adding new document types
   - Customizing prompts
   - Configuration options
   - Testing guide
   - Deployment guide

4. Create docs/API_REFERENCE.md:
   - All endpoints documented
   - Request/response examples
   - Error codes
   - Rate limits

5. Create CONTRIBUTING.md:
   - How to contribute
   - Code style
   - PR process
   - Issue reporting

6. Create CHANGELOG.md:
   - Version history
   - v1.0.0 initial release features
```

---

## Prompt 10.4: Final Testing and Cleanup

```
Perform final testing and cleanup:

1. FULL SYSTEM TEST:
   
   a. Start fresh (remove all data):
      rm -rf data/uploads/* data/vectordb/*
   
   b. Start services:
      docker-compose up -d
   
   c. Test complete workflow:
      - Upload a real PDF document
      - Ask various questions
      - Generate study guide
      - Generate practice test
      - Verify citations
      - Check hallucination detection
      - Delete document
   
   d. Verify logs are clean (no errors)

2. PERFORMANCE CHECK:
   - Upload 5 documents
   - Measure query response time
   - Should be < 5 seconds

3. CODE CLEANUP:
   - Remove any debug print statements
   - Remove unused imports
   - Remove commented code
   - Ensure all TODO items addressed

4. SECURITY CHECK:
   - API key not exposed in code
   - No hardcoded credentials
   - CORS configured appropriately
   - Input validation on all endpoints

5. DOCUMENTATION CHECK:
   - All functions have docstrings
   - README is accurate
   - API docs generate correctly
   - User guide matches current UI

6. CREATE RELEASE CHECKLIST (docs/RELEASE_CHECKLIST.md):
   [ ] All tests passing
   [ ] Code coverage > 80%
   [ ] No linting errors
   [ ] Documentation complete
   [ ] Docker builds successfully
   [ ] Manual testing complete
   [ ] Environment variables documented
   [ ] Backup/restore tested
   [ ] Performance acceptable

7. TAG RELEASE:
   git tag -a v1.0.0 -m "Initial release"
   git push origin v1.0.0

Run final verification and report status of all checks.
```

---

# ✅ PROJECT COMPLETION CHECKLIST

```
Use this checklist to verify project is complete:

PHASE 1: Environment Setup
[ ] Project structure created
[ ] Dependencies installed
[ ] Configuration files created
[ ] Logger utility working
[ ] Config loader working

PHASE 2: Document Processing
[ ] PDF processor working
[ ] DOCX processor working
[ ] Text chunker working
[ ] Document service orchestrating correctly

PHASE 3: Vector Database
[ ] Embedding service working
[ ] ChromaDB store working
[ ] Retrieval service working
[ ] Citations generated correctly

PHASE 4: RAG Core
[ ] LLM service working
[ ] Prompts defined
[ ] RAG engine working
[ ] Responses include citations

PHASE 5: Hallucination Control
[ ] Hallucination detector working
[ ] Citation manager working
[ ] Warnings shown for ungrounded content

PHASE 6: Bloom's Taxonomy
[ ] Level detection working
[ ] Different levels produce different responses
[ ] Practice questions generated

PHASE 7: Backend API
[ ] All endpoints working
[ ] Error handling correct
[ ] API documentation generated

PHASE 8: Frontend
[ ] Document upload working
[ ] Query interface working
[ ] Study guide working
[ ] Practice test working
[ ] Analytics displaying

PHASE 9: Testing
[ ] Unit tests passing
[ ] Integration tests passing
[ ] Coverage > 80%
[ ] Code quality checks passing

PHASE 10: Deployment
[ ] Docker configuration working
[ ] Scripts working
[ ] Documentation complete
[ ] Final testing passed

🎉 PROJECT COMPLETE!
```

---

# TIPS FOR USING THESE PROMPTS

1. **Copy one prompt at a time** - Don't overwhelm Claude Code
2. **Wait for completion** - Let each step finish before moving on
3. **Test as you go** - Run tests after each phase
4. **Ask for clarification** - If something isn't clear, ask
5. **Save your work** - Commit to git after each phase
6. **Debug together** - If errors occur, share them with Claude Code

Good luck building your AI Study Assistant! 🚀
