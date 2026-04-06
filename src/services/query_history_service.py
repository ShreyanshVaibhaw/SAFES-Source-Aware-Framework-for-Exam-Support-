"""Query history storage and retrieval service."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

from src.models.query_history import QueryRecord
from src.utils.logger import get_logger


class QueryHistoryService:
    """JSON-file-backed query history storage."""

    def __init__(self, persist_path: Optional[Path] = None) -> None:
        self.logger = get_logger(__name__)
        self._persist_path = persist_path or Path("data/query_history.json")
        self._records: List[QueryRecord] = []
        self._load()

    def _load(self) -> None:
        """Load history from disk if exists."""
        if self._persist_path.exists():
            try:
                with self._persist_path.open("r", encoding="utf-8") as fp:
                    data = json.load(fp)
                self._records = [QueryRecord(**item) for item in data]
            except Exception as exc:
                self.logger.warning(f"Failed to load query history: {exc}")
                self._records = []

    def _persist(self) -> None:
        """Save history to disk."""
        try:
            self._persist_path.parent.mkdir(parents=True, exist_ok=True)
            with self._persist_path.open("w", encoding="utf-8") as fp:
                json.dump(
                    [rec.model_dump(mode="json") for rec in self._records],
                    fp,
                    ensure_ascii=False,
                    indent=2,
                    default=str,
                )
        except Exception as exc:
            self.logger.error(f"Failed to persist query history: {exc}")

    def record_query(
        self,
        question: str,
        answer: str,
        bloom_level: str = "understand",
        confidence: float = 0.0,
        citations_count: int = 0,
        document_ids: Optional[List[str]] = None,
        response_time_ms: float = 0.0,
    ) -> QueryRecord:
        """Record a new query."""
        record = QueryRecord(
            question=question,
            answer=answer,
            bloom_level=bloom_level,
            confidence=confidence,
            citations_count=citations_count,
            document_ids=document_ids or [],
            response_time_ms=response_time_ms,
        )
        self._records.append(record)
        self._persist()
        return record

    def get_history(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Return paginated history, newest first."""
        sorted_records = sorted(self._records, key=lambda r: r.timestamp, reverse=True)
        page = sorted_records[offset : offset + limit]
        return [rec.model_dump(mode="json") for rec in page]

    def get_query(self, query_id: str) -> Optional[Dict]:
        """Get a single query record by ID."""
        for rec in self._records:
            if rec.query_id == query_id:
                return rec.model_dump(mode="json")
        return None

    def get_stats(self) -> Dict:
        """Return aggregate stats about query history."""
        if not self._records:
            return {
                "total_queries": 0,
                "avg_confidence": 0.0,
                "avg_response_time_ms": 0.0,
                "queries_by_bloom_level": {},
            }

        total = len(self._records)
        avg_conf = sum(r.confidence for r in self._records) / total
        avg_time = sum(r.response_time_ms for r in self._records) / total
        bloom_counts = Counter(r.bloom_level for r in self._records)

        return {
            "total_queries": total,
            "avg_confidence": round(avg_conf, 3),
            "avg_response_time_ms": round(avg_time, 1),
            "queries_by_bloom_level": dict(bloom_counts),
        }

    def clear(self) -> int:
        """Clear all history records. Returns count of deleted records."""
        count = len(self._records)
        self._records.clear()
        self._persist()
        return count
