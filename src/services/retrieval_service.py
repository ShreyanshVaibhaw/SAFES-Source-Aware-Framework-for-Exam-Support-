"""Semantic retrieval service over processed document chunks."""

from __future__ import annotations

from typing import Dict, List, Optional

from src.models.document import ProcessedDocument
from src.services.embedding_service import EmbeddingService
from src.services.vector_store.chroma_store import ChromaStore
from src.services.vector_store.faiss_store import FaissStore
from src.utils.config import ConfigLoader
from src.utils.config import config as global_config
from src.utils.logger import get_logger


class RetrievalService:
    """Indexes chunks and performs semantic retrieval."""

    def __init__(
        self,
        embedding_service: Optional[EmbeddingService] = None,
        vector_store: Optional[object] = None,
        config: Optional[ConfigLoader] = None,
    ) -> None:
        self.config = config or global_config
        self.logger = get_logger(__name__)
        self.embedding_service = embedding_service or EmbeddingService(config=self.config)

        if vector_store is not None:
            self.vector_store = vector_store
        else:
            store_type = self.config.get("vector_database.type", "chromadb").lower()
            persist_dir = str(self.config.vectordb_dir)
            collection_name = self.config.get(
                "vector_database.collection_name", "study_materials"
            )
            if store_type == "faiss":
                embedding_dim = int(
                    self.config.get("vector_database.embedding_dimension", 384)
                )
                self.vector_store = FaissStore(
                    persist_directory=persist_dir,
                    embedding_dimension=embedding_dim,
                    collection_name=collection_name,
                )
            else:
                self.vector_store = ChromaStore(
                    persist_directory=persist_dir,
                    collection_name=collection_name,
                )

    def index_document(self, document: ProcessedDocument) -> int:
        """Generate embeddings and index all chunks of one document."""
        if not document.chunks:
            return 0
        texts = [chunk.content for chunk in document.chunks]
        vectors = self.embedding_service.generate_embeddings(texts)
        records: List[Dict] = []
        for chunk, vector in zip(document.chunks, vectors):
            records.append(
                {
                    "id": chunk.chunk_id,
                    "document_id": document.document_id,
                    "content": chunk.content,
                    "embedding": vector,
                    "metadata": {
                        "chunk_id": chunk.chunk_id,
                        "page_number": chunk.page_number,
                        "section_title": chunk.section_title,
                        "token_count": chunk.token_count,
                        "start_char": chunk.start_char,
                        "end_char": chunk.end_char,
                        "document_id": chunk.document_id,
                    },
                }
            )
        return self.vector_store.add_documents(records)

    def index_documents(self, documents: List[ProcessedDocument]) -> int:
        """Index a batch of processed documents."""
        total = 0
        for document in documents:
            total += self.index_document(document)
        return total

    def semantic_search(
        self,
        query: str,
        top_k: Optional[int] = None,
        document_ids: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Run semantic search for query text."""
        top_k = top_k or int(self.config.get("retrieval.top_k", 5))
        threshold = float(self.config.get("retrieval.similarity_threshold", 0.7))
        query_vector = self.embedding_service.generate_embedding(query)
        results = self.vector_store.similarity_search(
            query_embedding=query_vector,
            top_k=top_k * 2,
            document_ids=document_ids,
        )
        filtered = [result for result in results if float(result["score"]) >= threshold]
        if not filtered:
            return results[:top_k]
        return filtered[:top_k]

    def build_context(self, results: List[Dict], max_tokens: Optional[int] = None) -> Dict:
        """Build LLM context text and structured citation payload."""
        max_tokens = max_tokens or int(self.config.get("retrieval.max_context_tokens", 2000))
        used_tokens = 0
        blocks: List[str] = []
        citations: List[Dict] = []

        for idx, result in enumerate(results, start=1):
            content = result["content"].strip()
            token_count = max(1, len(content.split()))
            if used_tokens + token_count > max_tokens:
                break
            used_tokens += token_count
            meta = result.get("metadata", {})
            blocks.append(f"[{idx}] {content}")
            citations.append(
                {
                    "citation_id": idx,
                    "document_id": result.get("document_id"),
                    "chunk_id": meta.get("chunk_id"),
                    "page_number": meta.get("page_number"),
                    "section_title": meta.get("section_title"),
                    "score": round(float(result.get("score", 0.0)), 4),
                }
            )

        return {"text": "\n\n".join(blocks), "citations": citations, "token_count": used_tokens}

    def delete_document(self, document_id: str) -> int:
        """Delete all indexed chunks for a document."""
        return self.vector_store.delete_document(document_id)

    def stats(self) -> Dict:
        """Return vector index stats."""
        return self.vector_store.get_stats()
