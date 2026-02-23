from pathlib import Path

from src.services.document_service import DocumentService


def test_document_pipeline_process_and_chunk(tmp_path: Path):
    file_path = tmp_path / "notes.md"
    file_path.write_text(
        "# Topic\nA short note about retrieval augmented generation.", encoding="utf-8"
    )

    service = DocumentService()
    doc = service.process_document(file_path)
    assert doc.processing_status.value == "completed"
    assert doc.total_chunks >= 1
