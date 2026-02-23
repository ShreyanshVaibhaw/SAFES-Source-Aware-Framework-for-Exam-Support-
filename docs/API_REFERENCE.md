# API Reference

Base URL: `http://localhost:8000`

## Health
- `GET /health`
- Response: status and vector index stats.

## Documents
- `POST /documents/upload`
  - Multipart form with `file`.
  - Optional fields: `subject`, `course`, `tags`.
- `GET /documents`
- `GET /documents/{document_id}`
- `GET /documents/{document_id}/chunks`
- `DELETE /documents/{document_id}`

## Query
- `POST /query`
  - Body:
    - `question` (string, required)
    - `bloom_level` (optional)
    - `top_k` (int)
    - `document_ids` (optional list)
    - `check_hallucination` (bool)
    - `include_citations` (bool)
- `POST /query/stream`

## Study
- `POST /study/guide`
  - Body: `topics` (list), `level` (string)
- `POST /study/practice-test`
  - Body: `topics` (list), `difficulty` (string), `num_questions` (int)
- `GET /study/key-concepts`

## Errors
- `400`: invalid input or processing failure
- `404`: missing document/resource
- `422`: schema validation error
