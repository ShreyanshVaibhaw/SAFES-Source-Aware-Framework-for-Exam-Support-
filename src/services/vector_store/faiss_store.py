"""FAISS-backed persistent vector store."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

import faiss
import numpy as np

from src.utils.logger import get_logger


class FaissStore:
    """Persistent vector store using FAISS IndexFlatIP (cosine via normalized inner product)."""

    def __init__(
        self,
        persist_directory: Optional[str] = None,
        embedding_dimension: int = 384,
        collection_name: str = "study_materials",
    ) -> None:
        self.logger = get_logger(__name__)
        self._dim = embedding_dimension
        self._collection_name = collection_name

        persist_dir = persist_directory or str(
            Path(__file__).parent.parent.parent.parent / "data" / "vectordb"
        )
        self._persist_dir = Path(persist_dir)
        self._persist_dir.mkdir(parents=True, exist_ok=True)

        self._index_path = self._persist_dir / f"{collection_name}.faiss.index"
        self._meta_path = self._persist_dir / f"{collection_name}.faiss.meta.json"

        self._metadata: List[Dict] = []
        self._index: faiss.IndexFlatIP = faiss.IndexFlatIP(self._dim)

        self._load()
        self.logger.info(
            f"FaissStore initialized: dir={persist_dir}, dim={embedding_dimension}, "
            f"existing_records={self._index.ntotal}"
        )

    def _load(self) -> None:
        """Load persisted index and metadata if they exist."""
        if self._index_path.exists() and self._meta_path.exists():
            try:
                self._index = faiss.read_index(str(self._index_path))
                with self._meta_path.open("r", encoding="utf-8") as fp:
                    self._metadata = json.load(fp)
                if self._index.ntotal != len(self._metadata):
                    self.logger.warning("Index/metadata size mismatch, resetting.")
                    self._index = faiss.IndexFlatIP(self._dim)
                    self._metadata = []
            except Exception as exc:
                self.logger.warning(f"Failed to load FAISS index, starting fresh: {exc}")
                self._index = faiss.IndexFlatIP(self._dim)
                self._metadata = []

    def _persist(self) -> None:
        """Save index and metadata to disk."""
        try:
            faiss.write_index(self._index, str(self._index_path))
            with self._meta_path.open("w", encoding="utf-8") as fp:
                json.dump(self._metadata, fp, ensure_ascii=False)
        except Exception as exc:
            self.logger.error(f"Failed to persist FAISS store: {exc}")

    def add_documents(self, records: List[Dict]) -> int:
        """Add records to the store."""
        if not records:
            return 0

        vectors = np.array(
            [rec["embedding"] for rec in records], dtype=np.float32
        )
        faiss.normalize_L2(vectors)
        self._index.add(vectors)

        for rec in records:
            meta = dict(rec.get("metadata", {}))
            meta["document_id"] = rec["document_id"]
            self._metadata.append(
                {
                    "id": rec["id"],
                    "document_id": rec["document_id"],
                    "content": rec["content"],
                    "metadata": meta,
                }
            )

        self._persist()
        return len(records)

    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        document_ids: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Return top-k similar chunks."""
        if self._index.ntotal == 0:
            return []

        query_vec = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_vec)

        effective_k = min(top_k, self._index.ntotal)
        if document_ids:
            effective_k = min(self._index.ntotal, top_k * 5)

        scores, indices = self._index.search(query_vec, effective_k)

        allowed = set(document_ids or [])
        results: List[Dict] = []

        for i in range(len(indices[0])):
            idx = int(indices[0][i])
            if idx < 0 or idx >= len(self._metadata):
                continue
            entry = self._metadata[idx]
            if allowed and entry["document_id"] not in allowed:
                continue
            results.append(
                {
                    "id": entry["id"],
                    "document_id": entry["document_id"],
                    "content": entry["content"],
                    "metadata": entry["metadata"],
                    "score": float(scores[0][i]),
                }
            )
            if len(results) >= top_k:
                break

        return results

    def delete_document(self, document_id: str) -> int:
        """Delete all chunks belonging to one document (rebuild index)."""
        keep_indices = [
            i for i, m in enumerate(self._metadata) if m["document_id"] != document_id
        ]
        removed = len(self._metadata) - len(keep_indices)
        if removed == 0:
            return 0

        if keep_indices:
            kept_vectors = np.array(
                [self._index.reconstruct(i) for i in keep_indices], dtype=np.float32
            )
            self._metadata = [self._metadata[i] for i in keep_indices]
            self._index = faiss.IndexFlatIP(self._dim)
            self._index.add(kept_vectors)
        else:
            self._metadata = []
            self._index = faiss.IndexFlatIP(self._dim)

        self._persist()
        return removed

    def clear(self) -> None:
        """Clear all records."""
        self._index = faiss.IndexFlatIP(self._dim)
        self._metadata = []
        self._persist()

    def get_stats(self) -> Dict:
        """Return vector index statistics."""
        doc_ids = {m["document_id"] for m in self._metadata}
        return {"records": self._index.ntotal, "documents": len(doc_ids)}
