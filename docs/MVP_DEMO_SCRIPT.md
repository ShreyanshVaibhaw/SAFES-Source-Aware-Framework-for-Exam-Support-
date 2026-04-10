# SAFES - MVP Demo Video Script

**Duration:** 10-12 minutes  
**Presenters:** Team members  
**Format:** Screen recording + face cam overlay  

---

## SCENE 1: THE HOOK (0:00 - 0:45)

**[SCREEN: Show a Google search "What is Newton's Fourth Law of Motion"]**

**SPEAKER 1:**
> "Let me ask ChatGPT a question — What is Newton's Fourth Law of Motion?"

**[SCREEN: Paste into ChatGPT, show it confidently generating a fake answer]**

> "See that? It just made up a Fourth Law that doesn't exist. Newton only had three. But notice how confident it sounds — there's no warning, no citation, no way for a student to know this is completely fabricated."

**[PAUSE — let it sink in]**

> "This is called AI hallucination. And 43% of students have encountered incorrect AI-generated information while studying. 56% have unknowingly submitted hallucinated content. That's the problem we set out to solve."

---

## SCENE 2: THE PROBLEM (0:45 - 1:45)

**[SCREEN: Show the Problem slide or infographic]**

**SPEAKER 2:**
> "Today's AI tools have a fundamental problem when it comes to education. They are trained on broad internet data — they don't know YOUR syllabus, they can't reference YOUR textbooks, and they have no way to verify if what they're saying actually comes from your course material."

> "We identified six specific problems:"

**[SCREEN: Show each problem as bullet points appearing one by one]**

> "One — Hallucination. AI generates false information confidently.  
> Two — No citations. There's no way to verify or cross-reference with your textbook.  
> Three — Syllabus misalignment. Answers may be correct but outside your exam scope.  
> Four — Generic responses. Not optimized for exam-style answers.  
> Five — No cognitive levels. You get the same response whether you need a definition or a critical analysis.  
> Six — No transparency. There's no confidence score telling you how reliable the answer is."

> "No existing system combines solutions to ALL these problems. That's the gap SAFES fills."

---

## SCENE 3: INTRODUCING SAFES (1:45 - 3:00)

**[SCREEN: Open http://139.59.44.122 — Show the SAFES hero header with gradient]**

**SPEAKER 1:**
> "This is SAFES — Source-Aware Framework for Exam Support. It's an AI study assistant that answers your questions ONLY from YOUR uploaded study materials."

**[SCREEN: Point to the hero stats — Documents, Queries, GLM-5]**

> "Every answer includes proper citations with document name, page number, and section. Every answer goes through hallucination detection with a confidence score. And every answer adapts to your cognitive level using Bloom's Taxonomy — whether you need to just remember a fact, or critically analyze a concept."

> "Let me show you how it works."

---

## SCENE 4: LIVE DEMO — DOCUMENT UPLOAD (3:00 - 4:00)

**[SCREEN: Show the sidebar with file uploader]**

**SPEAKER 1:**
> "First, I upload my study material. SAFES supports PDF, Word documents, plain text, and markdown files — up to 50 megabytes."

**[ACTION: Upload the Human_Brain_Study_Notes.pdf]**

> "Behind the scenes, three things happen instantly:"

**[SCREEN: Show the upload success message]**

> "One — the PDF processor extracts text page by page, preserving tables, headings, and section structure using pdfplumber.  
> Two — the text chunker splits the document into 500-token chunks with 50-token overlap, so no information falls between the cracks.  
> Three — each chunk is converted into a 384-dimensional vector embedding and stored in a persistent ChromaDB vector database. This enables meaning-based search, not just keyword matching."

**[SCREEN: Point to the document appearing in the Library section]**

> "The document is now indexed and ready to answer questions."

---

## SCENE 5: LIVE DEMO — QUERYING (4:00 - 6:00)

**[SCREEN: Click on the Query tab]**

**SPEAKER 2:**
> "Now let's ask a question. I'll type: 'Explain how synaptic transmission works in the brain'"

**[ACTION: Type the question, set Bloom level to "understand", click Get Answer]**

> "Notice a few things about the response:"

**[SCREEN: Point to each element as you mention it]**

> "First — the answer itself. It's generated using the GLM-5 language model, but the system prompt strictly instructs it to use ONLY the provided context snippets. No external knowledge contamination."

> "Second — the confidence meter. This shows 85% confidence with a green bar — meaning the answer is well-grounded in the source material. If the confidence drops below 50%, you'd see a red bar with a warning."

**[SCREEN: Scroll to citations]**

> "Third — citations. Every claim is backed by a specific source — document ID, page number, section title, and a relevance score. A student can go directly to page 2, the Neuron section, and verify the answer."

> "Fourth — the Bloom's level badge. The system detected 'Explain' as an 'Understand' level question and adapted the response style to be explanatory with examples, not just factual bullet points."

**[SCREEN: Scroll to practice questions]**

> "And fifth — it automatically generates practice questions at the same cognitive level to reinforce learning."

---

## SCENE 6: LIVE DEMO — HALLUCINATION DETECTION (6:00 - 7:00)

**[SCREEN: Show the grounding alert section]**

**SPEAKER 1:**
> "This is the hallucination control system — the core innovation of SAFES."

> "It works at two levels. First, a heuristic check calculates keyword overlap between the answer and the source context — how much of the answer vocabulary actually comes from the uploaded material. Then it identifies individual sentences that have low overlap and flags them as potentially unsupported claims."

> "Second, when an LLM is available, we run claim-by-claim verification — sending each factual claim back to the model to check if it's supported, partially supported, or unsupported by the context."

**[SCREEN: Show the confidence configuration in config.yaml briefly]**

> "The confidence threshold, the action on hallucination — warn, refuse, or flag — and the maximum unsupported ratio are all configurable. If we set it to 'refuse' mode, the system will actually replace the answer with a message saying it cannot provide a reliable response. This is how we prevent misinformation."

---

## SCENE 7: LIVE DEMO — STUDY TOOLS (7:00 - 8:00)

**[SCREEN: Click Study Guide tab]**

**SPEAKER 2:**
> "Beyond Q&A, SAFES has three study tools built in."

**[ACTION: Type "memory systems, neurotransmitters" and click Generate Guide]**

> "The Study Guide generator creates structured revision notes for any topic, grounded in your materials, with a download button for offline use."

**[SCREEN: Click Compare tab]**

**[ACTION: Type "Alzheimer's" and "Parkinson's", click Compare]**

> "The Topic Comparison tool does side-by-side analysis. Here it's comparing Alzheimer's and Parkinson's disease — pulling context for each from the uploaded PDF and generating a structured comparison with similarities, differences, and exam tips."

**[SCREEN: Click Practice Test tab]**

**[ACTION: Generate 5 medium-difficulty questions on "brain lobes"]**

> "And the Practice Test generator creates exam-style questions with hints, at your chosen difficulty level."

---

## SCENE 8: ARCHITECTURE & TECH STACK (8:00 - 9:30)

**[SCREEN: Show the architecture diagram from README or a prepared slide]**

**SPEAKER 1:**
> "Let me walk you through the architecture."

> "SAFES follows a layered architecture with four main layers:"

> "The Presentation Layer is a Streamlit frontend with 5 switchable themes — Light, Dark, Midnight, Sunset, and Ocean. It communicates with the backend via REST API calls."

> "The API Layer is built with FastAPI — it handles routing, request validation with Pydantic, CORS for cross-origin access, and a custom sliding-window rate limiter that prevents API abuse."

> "The Business Logic Layer contains the RAG Engine — which orchestrates the entire pipeline: retrieval, generation, citation enrichment, and hallucination verification. It also houses the Bloom's Taxonomy detector, the Citation Manager, and the Hallucination Detector."

> "The Service Layer has five core services:"

**[SCREEN: Show each service name as you list them]**

> "The Document Service processes PDFs and Word files. The Embedding Service generates vector embeddings with a deterministic fallback for offline use. The Retrieval Service runs hybrid search — combining semantic vector search with BM25 keyword matching using Reciprocal Rank Fusion, followed by a reranker. The LLM Service supports four providers — OpenAI, Anthropic Claude, Google Gemini, and Ollama for local models. And the Query History Service persists every query for analytics."

> "At the Data Layer, we use ChromaDB and FAISS as persistent vector stores — data survives server restarts."

---

## SCENE 9: DEVELOPMENT JOURNEY & CHALLENGES (9:30 - 11:00)

**[SCREEN: Show timeline or phase breakdown]**

**SPEAKER 2:**
> "Development followed six phases, building up from foundation to production."

> "Phase 1 was vector store persistence. Our initial implementation used in-memory dictionaries — meaning every server restart wiped all uploaded documents. The challenge was integrating real ChromaDB and FAISS while keeping the exact same API contract so nothing else broke. We solved this by preserving the method signatures and writing 14 new unit tests to verify persistence across instance recreation."

> "Phase 2 was retrieval quality. Pure semantic search missed keyword-specific facts. We built a BM25 index from scratch — about 120 lines implementing Okapi BM25 scoring — and combined it with vector search using Reciprocal Rank Fusion. Then we added a reranker that uses keyword and entity overlap to improve precision."

> "Phase 3 was the biggest technical challenge — LLM-based hallucination verification. The heuristic detector had an 85% accuracy rate, but it couldn't understand semantic nuances. We added a claim-by-claim verification prompt that sends each sentence back to the LLM for grounding assessment. The challenge was making this robust — it had to parse JSON responses, handle API timeouts, and gracefully fall back to the heuristic method on any error. We tested this with 7 different scenarios including malformed JSON and API exceptions."

> "Phase 4 added rate limiting — a 40-line ASGI middleware using a sliding window algorithm. Phase 5 added query history with JSON persistence and aggregate analytics."

> "Phase 6 was multi-provider LLM support. The original code only supported OpenAI. We refactored to auto-detect from API keys, with a priority chain: configured provider first, then fallback through OpenAI, Anthropic, Gemini, and Ollama. The challenge was that each provider has a different API format — OpenAI uses chat completions, Anthropic uses messages, Gemini uses generate_content. We unified them behind a single generate_answer interface."

---

## SCENE 10: TESTING & QUALITY (11:00 - 11:30)

**[SCREEN: Show test run output or coverage report]**

**SPEAKER 1:**
> "Quality was non-negotiable. We have 91 automated tests — 73 unit tests and 18 integration tests — covering every component from the text chunker to the full API upload-query-delete flow."

> "We use pytest with async support, httpx for API testing, and maintain test isolation through temporary directories for each test — no test affects another."

> "Code quality is enforced through Black formatting, isort import ordering, flake8 linting, and pre-commit hooks that run automatically on every commit."

---

## SCENE 11: DEPLOYMENT & CLOSING (11:30 - 12:00)

**[SCREEN: Show the live app at http://139.59.44.122]**

**SPEAKER 2:**
> "SAFES is deployed on a DigitalOcean cloud server using Docker — both the FastAPI backend and Streamlit frontend run as containers. The app is accessible from anywhere at this URL."

> "The entire codebase is approximately 6,000 lines of Python across 80 files, with nearly 9,000 lines total including configuration, documentation, and tests."

**[SCREEN: Show the Analytics tab with query history and stats]**

> "To summarize — SAFES solves the AI hallucination problem in education by grounding every answer in the student's own materials, providing verifiable citations, running hallucination checks with confidence scoring, adapting responses to cognitive levels using Bloom's Taxonomy, and offering study tools like guides, practice tests, and topic comparison — all through a beautiful, themed, interactive interface."

**[SCREEN: Show the hero header one last time]**

**SPEAKER 1:**
> "SAFES — because the answer to your exam question should come from your textbook, not from the internet."

> "Thank you."

---

## PRODUCTION NOTES

### Screen Recording Checklist
- [ ] Use **Midnight** or **Dark** theme for better screen recording contrast
- [ ] Upload the Human Brain PDF before recording (or show it live)
- [ ] Have `configs/config.yaml` open in an editor for the hallucination config scene
- [ ] Pre-test all demo queries to ensure GLM-5 responses are good
- [ ] Show the Swagger docs page briefly (`/docs`) to demonstrate API documentation
- [ ] Close unnecessary browser tabs and notifications before recording

### Suggested Demo Queries
1. "Explain how synaptic transmission works" (Bloom: understand)
2. "List the four lobes of the cerebrum and their functions" (Bloom: remember)
3. "Compare Alzheimer's and Parkinson's disease" (Bloom: analyze)
4. "What are the key neurotransmitters and their roles?" (Bloom: remember)
5. "Evaluate the importance of neuroplasticity in brain injury recovery" (Bloom: evaluate)

### Backup Plan
- If GLM-5 API is slow or down during recording, the fallback mode still works — it shows context-based answers without LLM generation
- If the live server is unreachable, run locally: `uvicorn src.api.main:app --reload` + `streamlit run frontend/app.py`

### Video Editing Tips
- Add zoomed-in callouts for citations, confidence meter, and Bloom level badge
- Use transitions between demo and architecture slides
- Add background music at low volume during architecture explanation
- Speed up the PDF upload wait time if it takes more than 3 seconds
- Add text overlays for key terms: RAG, BM25, RRF, Bloom's Taxonomy, ChromaDB
