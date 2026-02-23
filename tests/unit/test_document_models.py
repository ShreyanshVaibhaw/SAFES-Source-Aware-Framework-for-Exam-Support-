from src.models.document import (
    DocumentChunk,
    DocumentMetadata,
    DocumentType,
    ProcessedDocument,
    ProcessingStatus,
)


def test_document_metadata_validation():
    meta = DocumentMetadata(filename="a.txt", file_type=DocumentType.TXT, file_size=10)
    assert meta.filename == "a.txt"
    assert meta.file_type == DocumentType.TXT


def test_document_chunk_and_processed_document():
    chunk = DocumentChunk(
        chunk_id="c1",
        document_id="d1",
        content="hello",
        start_char=0,
        end_char=5,
        token_count=1,
    )
    processed = ProcessedDocument(
        document_id="d1",
        metadata=DocumentMetadata(filename="a.txt", file_type=DocumentType.TXT, file_size=10),
        chunks=[chunk],
        total_chunks=1,
        total_tokens=1,
        processing_status=ProcessingStatus.COMPLETED,
    )
    assert processed.total_chunks == 1
