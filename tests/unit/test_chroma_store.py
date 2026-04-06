import math
from pathlib import Path

from src.services.vector_store.chroma_store import ChromaStore


def _make_record(chunk_id: str, doc_id: str, content: str, dim: int = 384):
    """Build a record with a simple deterministic embedding."""
    vec = [0.0] * dim
    for i, ch in enumerate(content.encode("utf-8")):
        vec[i % dim] += float(ch)
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return {
        "id": chunk_id,
        "document_id": doc_id,
        "content": content,
        "embedding": vec,
        "metadata": {"page_number": 1, "section_title": "Intro", "document_id": doc_id},
    }


def test_add_and_search(tmp_path: Path):
    store = ChromaStore(persist_directory=str(tmp_path), collection_name="test_col")
    rec = _make_record("c1", "doc1", "photosynthesis converts light into energy")
    store.add_documents([rec])

    results = store.similarity_search(rec["embedding"], top_k=1)
    assert len(results) == 1
    assert results[0]["id"] == "c1"
    assert results[0]["document_id"] == "doc1"
    assert results[0]["content"] == rec["content"]
    assert results[0]["score"] > 0.9


def test_persistence_survives_reload(tmp_path: Path):
    store = ChromaStore(persist_directory=str(tmp_path), collection_name="persist_test")
    rec = _make_record("c1", "doc1", "test persistence")
    store.add_documents([rec])
    assert store.get_stats()["records"] == 1

    # Destroy instance and recreate from same directory
    del store
    store2 = ChromaStore(persist_directory=str(tmp_path), collection_name="persist_test")
    assert store2.get_stats()["records"] == 1
    results = store2.similarity_search(rec["embedding"], top_k=1)
    assert results[0]["id"] == "c1"


def test_delete_document(tmp_path: Path):
    store = ChromaStore(persist_directory=str(tmp_path), collection_name="del_test")
    store.add_documents([
        _make_record("c1", "doc1", "first chunk"),
        _make_record("c2", "doc1", "second chunk"),
        _make_record("c3", "doc2", "other document"),
    ])
    assert store.get_stats()["records"] == 3

    removed = store.delete_document("doc1")
    assert removed == 2
    assert store.get_stats()["records"] == 1


def test_clear(tmp_path: Path):
    store = ChromaStore(persist_directory=str(tmp_path), collection_name="clear_test")
    store.add_documents([_make_record("c1", "doc1", "data")])
    store.clear()
    assert store.get_stats()["records"] == 0


def test_filter_by_document_ids(tmp_path: Path):
    store = ChromaStore(persist_directory=str(tmp_path), collection_name="filter_test")
    store.add_documents([
        _make_record("c1", "doc1", "alpha content"),
        _make_record("c2", "doc2", "beta content"),
    ])
    results = store.similarity_search(
        _make_record("q", "q", "alpha")["embedding"],
        top_k=5,
        document_ids=["doc2"],
    )
    assert all(r["document_id"] == "doc2" for r in results)


def test_get_stats(tmp_path: Path):
    store = ChromaStore(persist_directory=str(tmp_path), collection_name="stats_test")
    store.add_documents([
        _make_record("c1", "doc1", "a"),
        _make_record("c2", "doc1", "b"),
        _make_record("c3", "doc2", "c"),
    ])
    stats = store.get_stats()
    assert stats["records"] == 3
    assert stats["documents"] == 2


def test_empty_search(tmp_path: Path):
    store = ChromaStore(persist_directory=str(tmp_path), collection_name="empty_test")
    results = store.similarity_search([0.0] * 384, top_k=5)
    assert results == []
