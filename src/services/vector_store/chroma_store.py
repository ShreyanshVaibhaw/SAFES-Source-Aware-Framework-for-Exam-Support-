"""Chroma-like vector store API backed by in-memory storage."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from src.services.embedding_service import EmbeddingService
from src.utils.logger import get_logger


@dataclass
class StoredChunk:
    """Internal vector record."""

    id: str
    document_id: str
    content: str
    embedding: List[float]
    metadata: Dict


class ChromaStore:
    """Simple in-memory vector store with Chroma-like semantics."""

    def __init__(self, embedding_service: Optional[EmbeddingService] = None) -> None:
        self.logger = get_logger(__name__)
        self.embedding_service = embedding_service or EmbeddingService()
        self._records: Dict[str, StoredChunk] = {}

    def add_documents(self, records: List[Dict]) -> int:
        """Add records to the store.

        Expected keys: id, document_id, content, embedding, metadata.
        """
        for rec in records:
            item = StoredChunk(
                id=rec["id"],
                document_id=rec["document_id"],
                content=rec["content"],
                embedding=rec["embedding"],
                metadata=rec.get("metadata", {}),
            )
            self._records[item.id] = item
        return len(records)

    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        document_ids: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Return top-k similar chunks."""
        scored: List[Dict] = []
        allowed = set(document_ids or [])

        for rec in self._records.values():
            if allowed and rec.document_id not in allowed:
                continue
            score = self.embedding_service.cosine_similarity(query_embedding, rec.embedding)
            scored.append(
                {
                    "id": rec.id,
                    "document_id": rec.document_id,
                    "content": rec.content,
                    "metadata": rec.metadata,
                    "score": score,
                }
            )

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

    def delete_document(self, document_id: str) -> int:
        """Delete all chunks belonging to one document."""
        to_delete = [key for key, rec in self._records.items() if rec.document_id == document_id]
        for key in to_delete:
            del self._records[key]
        return len(to_delete)

    def clear(self) -> None:
        self._records.clear()

    def get_stats(self) -> Dict:
        return {
            "records": len(self._records),
            "documents": len({r.document_id for r in self._records.values()}),
        }
