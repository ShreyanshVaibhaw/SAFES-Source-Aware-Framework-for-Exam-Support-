# User Guide

## 1. Upload Materials
1. Open the Streamlit app (`http://localhost:8501`).
2. In the sidebar, upload a file (`.pdf`, `.docx`, `.txt`, `.md`).
3. Click **Upload** to process and index the document.

## 2. Ask Questions
1. Go to the **Query** tab.
2. Enter your question.
3. Optional: choose Bloom level and retrieval depth.
4. Click **Get Answer**.

Output includes:
- grounded answer text,
- confidence bar,
- citations (document/page/section),
- practice prompts.

## 3. Generate a Study Guide
1. Open the **Study Guide** tab.
2. Enter topic names separated by commas.
3. Choose cognitive level.
4. Click **Generate Guide** and optionally download markdown.

## 4. Generate a Practice Test
1. Open the **Practice Test** tab.
2. Enter topics, difficulty, and question count.
3. Click **Generate Practice Test**.

## 5. Analytics
- Open **Analytics** tab for health and indexed document overview.

## 6. Troubleshooting
- If upload fails, verify extension and file size limits in `configs/config.yaml`.
- If answers are weak, upload more relevant course material.
- If API is unreachable, check backend at `http://localhost:8000/health`.
