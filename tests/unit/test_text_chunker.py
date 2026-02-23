from src.services.document_processors.text_chunker import ChunkConfig, TextChunker


def test_count_tokens_non_zero():
    chunker = TextChunker()
    assert chunker.count_tokens("hello world") > 0


def test_create_chunks_respects_size():
    chunker = TextChunker(ChunkConfig(chunk_size=20, chunk_overlap=5, min_chunk_size=3))
    text = " ".join(["token"] * 80)
    chunks = chunker._create_chunks(text)
    assert len(chunks) >= 3
    assert all(chunker.count_tokens(chunk) <= 20 for chunk in chunks)


def test_chunk_document_includes_metadata():
    chunker = TextChunker(ChunkConfig(chunk_size=30, chunk_overlap=5, min_chunk_size=5))
    pages = [{"page_number": 1, "content": "# Intro\nThis is a test " * 20}]
    chunks = chunker.chunk_document(pages, "doc_x")
    assert chunks
    assert chunks[0]["document_id"] == "doc_x"
    assert "page_number" in chunks[0]
