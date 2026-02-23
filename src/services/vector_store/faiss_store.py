"""FAISS-compatible interface backed by the same in-memory logic."""

from __future__ import annotations

from src.services.embedding_service import EmbeddingService
from src.services.vector_store.chroma_store import ChromaStore


class FaissStore(ChromaStore):
    """Drop-in alternative vector store with identical behavior."""

    def __init__(self, embedding_service: EmbeddingService | None = None) -> None:
        super().__init__(embedding_service=embedding_service)
