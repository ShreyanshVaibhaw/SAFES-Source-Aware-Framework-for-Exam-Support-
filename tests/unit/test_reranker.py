from src.services.reranker import Reranker


def test_rerank_changes_order():
    reranker = Reranker()
    results = [
        {"id": "c1", "document_id": "d1", "content": "unrelated content about cooking", "score": 0.9, "metadata": {}},
        {"id": "c2", "document_id": "d1", "content": "TCP provides reliable transport protocol", "score": 0.7, "metadata": {}},
    ]
    reranked = reranker.rerank("TCP transport protocol", results, top_k=2)
    # c2 should rank higher because of keyword overlap even though original score was lower
    assert reranked[0]["id"] == "c2"


def test_rerank_respects_top_k():
    reranker = Reranker()
    results = [
        {"id": f"c{i}", "document_id": "d1", "content": f"chunk {i}", "score": 0.5, "metadata": {}}
        for i in range(10)
    ]
    reranked = reranker.rerank("chunk", results, top_k=3)
    assert len(reranked) == 3


def test_rerank_empty():
    reranker = Reranker()
    assert reranker.rerank("query", [], top_k=5) == []


def test_rerank_preserves_original_score():
    reranker = Reranker()
    results = [
        {"id": "c1", "document_id": "d1", "content": "test data", "score": 0.8, "metadata": {}},
    ]
    reranked = reranker.rerank("test", results, top_k=5)
    assert "_original_score" in reranked[0]
    assert reranked[0]["_original_score"] == 0.8
