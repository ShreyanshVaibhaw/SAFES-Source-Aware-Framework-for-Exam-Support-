"""Retrieval result reranker using keyword and entity overlap."""

from __future__ import annotations

import re
from typing import Dict, List, Optional

from src.utils.logger import get_logger


class Reranker:
    """Rerank retrieval results by combining original score with relevance signals."""

    def __init__(self, nlp_service=None) -> None:
        self.logger = get_logger(__name__)
        self._nlp = nlp_service

    def rerank(self, query: str, results: List[Dict], top_k: int = 5) -> List[Dict]:
        """Rerank results and return top_k."""
        if not results:
            return []

        query_tokens = self._tokenize(query)
        query_entities = set()
        if self._nlp:
            try:
                ents = self._nlp.extract_entities(query)
                query_entities = {e["text"].lower() for e in ents}
            except Exception:
                pass

        scored: List[Dict] = []
        for result in results:
            original_score = float(result.get("score", 0.0))
            content = result.get("content", "")

            keyword_score = self._keyword_overlap(query_tokens, content)
            entity_score = self._entity_overlap(query_entities, content) if query_entities else 0.0

            final_score = 0.6 * original_score + 0.25 * keyword_score + 0.15 * entity_score

            reranked = dict(result)
            reranked["score"] = final_score
            reranked["_original_score"] = original_score
            scored.append(reranked)

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def _keyword_overlap(self, query_tokens: List[str], content: str) -> float:
        """Fraction of query tokens found in content."""
        if not query_tokens:
            return 0.0
        content_tokens = set(self._tokenize(content))
        matches = sum(1 for t in query_tokens if t in content_tokens)
        return matches / len(query_tokens)

    def _entity_overlap(self, query_entities: set, content: str) -> float:
        """Fraction of query named entities found in content."""
        if not query_entities:
            return 0.0
        content_lower = content.lower()
        matches = sum(1 for e in query_entities if e in content_lower)
        return matches / len(query_entities)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Simple lowercase tokenization for overlap calculation."""
        stop = {
            "the", "a", "an", "is", "are", "was", "were", "to", "of", "for",
            "in", "on", "and", "or", "with", "that", "this", "it", "be",
        }
        tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())
        return [t for t in tokens if t not in stop and len(t) > 1]
