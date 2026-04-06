from src.services.bm25_search import BM25Index


def _rec(chunk_id, doc_id, content):
    return {"id": chunk_id, "document_id": doc_id, "content": content, "metadata": {}}


def test_add_and_search():
    idx = BM25Index()
    idx.add_documents([
        _rec("c1", "doc1", "TCP provides reliable transport over networks"),
        _rec("c2", "doc1", "UDP is connectionless and faster"),
        _rec("c3", "doc2", "HTTP uses TCP for web communication"),
    ])
    results = idx.search("TCP reliable transport", top_k=2)
    assert len(results) == 2
    assert results[0]["id"] == "c1"  # Best match


def test_filter_by_document_ids():
    idx = BM25Index()
    idx.add_documents([
        _rec("c1", "doc1", "machine learning algorithms"),
        _rec("c2", "doc2", "machine learning models"),
    ])
    results = idx.search("machine learning", top_k=5, document_ids=["doc2"])
    assert all(r["document_id"] == "doc2" for r in results)


def test_delete_document():
    idx = BM25Index()
    idx.add_documents([
        _rec("c1", "doc1", "alpha"),
        _rec("c2", "doc2", "beta"),
    ])
    removed = idx.delete_document("doc1")
    assert removed == 1
    results = idx.search("alpha", top_k=5)
    assert all(r["document_id"] != "doc1" for r in results)


def test_clear():
    idx = BM25Index()
    idx.add_documents([_rec("c1", "doc1", "data")])
    idx.clear()
    assert idx.search("data", top_k=5) == []


def test_empty_search():
    idx = BM25Index()
    assert idx.search("anything", top_k=5) == []
