from pathlib import Path

from src.services.query_history_service import QueryHistoryService


def test_record_and_retrieve(tmp_path: Path):
    service = QueryHistoryService(persist_path=tmp_path / "history.json")
    service.record_query(
        question="What is RAG?",
        answer="RAG is retrieval augmented generation.",
        bloom_level="understand",
        confidence=0.85,
        citations_count=3,
    )
    history = service.get_history(limit=10)
    assert len(history) == 1
    assert history[0]["question"] == "What is RAG?"


def test_pagination(tmp_path: Path):
    service = QueryHistoryService(persist_path=tmp_path / "history.json")
    for i in range(5):
        service.record_query(question=f"Q{i}", answer=f"A{i}")
    page = service.get_history(limit=2, offset=0)
    assert len(page) == 2
    page2 = service.get_history(limit=2, offset=2)
    assert len(page2) == 2


def test_get_stats(tmp_path: Path):
    service = QueryHistoryService(persist_path=tmp_path / "history.json")
    service.record_query(question="Q1", answer="A1", bloom_level="remember", confidence=0.9)
    service.record_query(question="Q2", answer="A2", bloom_level="analyze", confidence=0.7)
    stats = service.get_stats()
    assert stats["total_queries"] == 2
    assert stats["avg_confidence"] == 0.8
    assert stats["queries_by_bloom_level"]["remember"] == 1
    assert stats["queries_by_bloom_level"]["analyze"] == 1


def test_persistence(tmp_path: Path):
    path = tmp_path / "history.json"
    service = QueryHistoryService(persist_path=path)
    service.record_query(question="Q1", answer="A1")
    del service

    service2 = QueryHistoryService(persist_path=path)
    assert len(service2.get_history()) == 1


def test_clear(tmp_path: Path):
    service = QueryHistoryService(persist_path=tmp_path / "history.json")
    service.record_query(question="Q1", answer="A1")
    count = service.clear()
    assert count == 1
    assert service.get_history() == []


def test_empty_stats(tmp_path: Path):
    service = QueryHistoryService(persist_path=tmp_path / "history.json")
    stats = service.get_stats()
    assert stats["total_queries"] == 0
