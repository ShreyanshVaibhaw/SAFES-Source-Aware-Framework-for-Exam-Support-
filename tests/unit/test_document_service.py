from pathlib import Path

from src.services.document_service import DocumentService


def test_process_text_document(tmp_path: Path):
    service = DocumentService()
    file_path = tmp_path / "sample.txt"
    file_path.write_text("This is chapter one.\n\nThis is chapter two.", encoding="utf-8")

    doc = service.process_document(file_path)
    assert doc.processing_status.value == "completed"
    assert doc.total_chunks >= 1
    assert service.get_document(doc.document_id) is not None


def test_list_and_delete_document(tmp_path: Path):
    service = DocumentService()
    file_path = tmp_path / "delete_me.md"
    file_path.write_text("# Notes\nhello world", encoding="utf-8")

    doc = service.process_document(file_path)
    listed = service.list_documents()
    assert any(item["document_id"] == doc.document_id for item in listed)

    deleted = service.delete_document(doc.document_id)
    assert deleted is True
    assert service.get_document(doc.document_id) is None


def test_search_documents_returns_scored_chunks(tmp_path: Path):
    service = DocumentService()
    file_path = tmp_path / "search.txt"
    file_path.write_text("retrieval retrieval generation", encoding="utf-8")
    service.process_document(file_path)
    hits = service.search_documents("retrieval")
    assert hits
