from pathlib import Path

from src.services.document_service import DocumentService
from src.services.retrieval_service import RetrievalService


def test_retrieval_returns_relevant_chunks(tmp_path: Path):
    file_path = tmp_path / "network.txt"
    file_path.write_text(
        "TCP provides reliable transport. UDP is connectionless.", encoding="utf-8"
    )

    doc_service = DocumentService()
    retrieval = RetrievalService()
    doc = doc_service.process_document(file_path)
    retrieval.index_document(doc)

    results = retrieval.semantic_search("What is TCP?", top_k=3)
    assert results
