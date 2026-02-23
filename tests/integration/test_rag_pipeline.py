from pathlib import Path

from src.core.rag_engine import RAGEngine
from src.services.document_service import DocumentService
from src.services.llm_service import LLMService
from src.services.retrieval_service import RetrievalService


def test_rag_pipeline_end_to_end(tmp_path: Path):
    text_path = tmp_path / "law.txt"
    text_path.write_text("Newton has three laws of motion.", encoding="utf-8")

    document_service = DocumentService()
    retrieval = RetrievalService()
    llm = LLMService()
    rag = RAGEngine(retrieval_service=retrieval, llm_service=llm)

    doc = document_service.process_document(text_path)
    retrieval.index_document(doc)

    result = rag.answer_question("How many laws of motion did Newton define?")
    assert "answer" in result
    assert result["confidence"] >= 0.0
