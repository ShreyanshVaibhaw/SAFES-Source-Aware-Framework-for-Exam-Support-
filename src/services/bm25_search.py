"""BM25 keyword search index for hybrid retrieval."""

from __future__ import annotations

import math
import re
from typing import Dict, List, Optional


class BM25Index:
    """Okapi BM25 scoring over indexed document chunks."""

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self._docs: List[Dict] = []  # [{id, document_id, content, tokens, metadata}]
        self._avg_dl: float = 0.0
        self._df: Dict[str, int] = {}  # document frequency per term
        self._n: int = 0

    def add_documents(self, records: List[Dict]) -> int:
        """Index records for BM25 search."""
        for rec in records:
            tokens = self._tokenize(rec["content"])
            self._docs.append(
                {
                    "id": rec["id"],
                    "document_id": rec["document_id"],
                    "content": rec["content"],
                    "tokens": tokens,
                    "metadata": rec.get("metadata", {}),
                }
            )
            seen = set(tokens)
            for term in seen:
                self._df[term] = self._df.get(term, 0) + 1

        self._n = len(self._docs)
        total_len = sum(len(d["tokens"]) for d in self._docs)
        self._avg_dl = total_len / self._n if self._n else 0.0
        return len(records)

    def search(
        self,
        query: str,
        top_k: int = 5,
        document_ids: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Score documents against query using BM25."""
        query_tokens = self._tokenize(query)
        if not query_tokens or not self._docs:
            return []

        allowed = set(document_ids) if document_ids else None
        scored: List[Dict] = []

        for doc in self._docs:
            if allowed and doc["document_id"] not in allowed:
                continue
            score = self._score(query_tokens, doc["tokens"])
            scored.append(
                {
                    "id": doc["id"],
                    "document_id": doc["document_id"],
                    "content": doc["content"],
                    "metadata": doc["metadata"],
                    "score": score,
                }
            )

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def delete_document(self, document_id: str) -> int:
        """Remove all entries for a document and rebuild IDF."""
        before = len(self._docs)
        self._docs = [d for d in self._docs if d["document_id"] != document_id]
        removed = before - len(self._docs)
        if removed > 0:
            self._rebuild_stats()
        return removed

    def clear(self) -> None:
        """Reset the index."""
        self._docs.clear()
        self._df.clear()
        self._avg_dl = 0.0
        self._n = 0

    def _rebuild_stats(self) -> None:
        """Recalculate DF and average document length."""
        self._df.clear()
        self._n = len(self._docs)
        total_len = 0
        for doc in self._docs:
            total_len += len(doc["tokens"])
            for term in set(doc["tokens"]):
                self._df[term] = self._df.get(term, 0) + 1
        self._avg_dl = total_len / self._n if self._n else 0.0

    def _score(self, query_tokens: List[str], doc_tokens: List[str]) -> float:
        """Compute BM25 score for a single document."""
        dl = len(doc_tokens)
        tf_map: Dict[str, int] = {}
        for t in doc_tokens:
            tf_map[t] = tf_map.get(t, 0) + 1

        score = 0.0
        for term in query_tokens:
            if term not in tf_map:
                continue
            tf = tf_map[term]
            df = self._df.get(term, 0)
            idf = math.log((self._n - df + 0.5) / (df + 0.5) + 1.0)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * dl / max(self._avg_dl, 1.0))
            score += idf * numerator / denominator
        return score

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Simple lowercase word tokenization."""
        return re.findall(r"[a-zA-Z0-9]+", text.lower())
