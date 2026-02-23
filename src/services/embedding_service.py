"""Embedding service with deterministic fallback for offline/test use."""

from __future__ import annotations

import hashlib
import math
import os
import re
from typing import List, Optional

import numpy as np

from src.utils.config import ConfigLoader
from src.utils.config import config as global_config
from src.utils.logger import get_logger

try:  # pragma: no cover - optional runtime path
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover - optional runtime path
    SentenceTransformer = None  # type: ignore


class EmbeddingService:
    """Generate embeddings using SentenceTransformers or deterministic hashing."""

    def __init__(
        self,
        model_name: Optional[str] = None,
        config: Optional[ConfigLoader] = None,
    ) -> None:
        self.config = config or global_config
        self.logger = get_logger(__name__)
        self.model_name = model_name or self.config.get(
            "vector_database.embedding_model", "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.embedding_dim = int(self.config.get("vector_database.embedding_dimension", 384))
        self._model = None

        use_transformer = os.getenv("SAFES_USE_SENTENCE_TRANSFORMERS", "0").strip() == "1"
        if use_transformer and SentenceTransformer is not None:
            try:
                self._model = SentenceTransformer(self.model_name)
                self.embedding_dim = int(self._model.get_sentence_embedding_dimension())
                self.logger.info(f"Loaded embedding model: {self.model_name}")
            except Exception as exc:  # pragma: no cover - network/model dependent
                self.logger.warning(f"Failed to load transformer model, falling back: {exc}")
                self._model = None

    def generate_embedding(self, text: str) -> List[float]:
        """Generate one embedding vector."""
        if self._model is not None:
            vector = self._model.encode(text, normalize_embeddings=True)
            return vector.tolist()
        return self._fallback_embedding(text)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts."""
        if not texts:
            return []
        if self._model is not None:
            vectors = self._model.encode(texts, normalize_embeddings=True)
            return [row.tolist() for row in vectors]
        return [self._fallback_embedding(text) for text in texts]

    def cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Compute cosine similarity between two vectors."""
        a = np.array(vec_a, dtype=float)
        b = np.array(vec_b, dtype=float)
        denom = np.linalg.norm(a) * np.linalg.norm(b)
        if denom == 0:
            return 0.0
        return float(np.dot(a, b) / denom)

    def _fallback_embedding(self, text: str) -> List[float]:
        """Hash-based bag-of-words embedding for deterministic local behavior."""
        tokens = re.findall(r"[a-zA-Z0-9_]+", text.lower())
        vec = np.zeros(self.embedding_dim, dtype=float)
        if not tokens:
            return vec.tolist()

        for token in tokens:
            digest = hashlib.md5(token.encode("utf-8")).hexdigest()
            idx = int(digest, 16) % self.embedding_dim
            vec[idx] += 1.0

        norm = math.sqrt(float(np.dot(vec, vec)))
        if norm > 0:
            vec = vec / norm
        return vec.tolist()
