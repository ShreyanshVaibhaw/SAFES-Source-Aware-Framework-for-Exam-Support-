"""ChromaDB-backed persistent vector store."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Optional

import chromadb

from src.utils.logger import get_logger


class ChromaStore:
    """Persistent vector store using ChromaDB."""

    def __init__(
        self,
        persist_directory: Optional[str] = None,
        collection_name: str = "study_materials",
    ) -> None:
        self.logger = get_logger(__name__)
        self._collection_name = collection_name

        persist_dir = persist_directory or os.getenv(
            "CHROMA_PERSIST_DIR", str(Path(__file__).parent.parent.parent.parent / "data" / "vectordb")
        )
        Path(persist_dir).mkdir(parents=True, exist_ok=True)

        self._client = chromadb.PersistentClient(path=persist_dir)
        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self.logger.info(
            f"ChromaStore initialized: dir={persist_dir}, collection={collection_name}, "
            f"existing_records={self._collection.count()}"
        )

    def add_documents(self, records: List[Dict]) -> int:
        """Add records to the store.

        Expected keys: id, document_id, content, embedding, metadata.
        """
        if not records:
            return 0

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for rec in records:
            ids.append(rec["id"])
            documents.append(rec["content"])
            embeddings.append(rec["embedding"])
            meta = dict(rec.get("metadata", {}))
            meta["document_id"] = rec["document_id"]
            # ChromaDB requires metadata values to be str, int, float, or bool
            cleaned = {}
            for k, v in meta.items():
                if v is None:
                    cleaned[k] = ""
                elif isinstance(v, (str, int, float, bool)):
                    cleaned[k] = v
                else:
                    cleaned[k] = str(v)
            metadatas.append(cleaned)

        self._collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        return len(records)

    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        document_ids: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Return top-k similar chunks."""
        if self._collection.count() == 0:
            return []

        where_filter = None
        if document_ids:
            if len(document_ids) == 1:
                where_filter = {"document_id": document_ids[0]}
            else:
                where_filter = {"document_id": {"$in": document_ids}}

        effective_k = min(top_k, self._collection.count())
        if effective_k <= 0:
            return []

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=effective_k,
            where=where_filter,
            include=["documents", "metadatas", "distances", "embeddings"],
        )

        scored: List[Dict] = []
        if not results or not results.get("ids") or not results["ids"][0]:
            return []

        for i, chunk_id in enumerate(results["ids"][0]):
            distance = results["distances"][0][i] if results.get("distances") else 0.0
            # ChromaDB cosine distance is in [0, 2]; convert to similarity in [-1, 1]
            score = 1.0 - distance
            metadata = results["metadatas"][0][i] if results.get("metadatas") else {}
            content = results["documents"][0][i] if results.get("documents") else ""
            doc_id = metadata.pop("document_id", "")

            scored.append(
                {
                    "id": chunk_id,
                    "document_id": doc_id,
                    "content": content,
                    "metadata": metadata,
                    "score": score,
                }
            )

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored

    def delete_document(self, document_id: str) -> int:
        """Delete all chunks belonging to one document."""
        try:
            existing = self._collection.get(
                where={"document_id": document_id},
                include=[],
            )
            if not existing or not existing.get("ids"):
                return 0
            ids_to_delete = existing["ids"]
            self._collection.delete(ids=ids_to_delete)
            return len(ids_to_delete)
        except Exception as exc:
            self.logger.warning(f"Error deleting document {document_id}: {exc}")
            return 0

    def clear(self) -> None:
        """Clear all records by recreating the collection."""
        self._client.delete_collection(self._collection_name)
        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def get_stats(self) -> Dict:
        """Return vector index statistics."""
        count = self._collection.count()
        if count == 0:
            return {"records": 0, "documents": 0}

        try:
            all_meta = self._collection.get(include=["metadatas"])
            doc_ids = {
                m.get("document_id", "")
                for m in (all_meta.get("metadatas") or [])
                if m
            }
            doc_ids.discard("")
            return {"records": count, "documents": len(doc_ids)}
        except Exception:
            return {"records": count, "documents": 0}
