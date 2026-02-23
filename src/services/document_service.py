"""Document processing orchestration service."""

from __future__ import annotations

import hashlib
import uuid
from pathlib import Path
from time import perf_counter
from typing import Dict, List, Optional

from src.models.document import (
    DocumentChunk,
    DocumentMetadata,
    DocumentType,
    ProcessedDocument,
    ProcessingStatus,
)
from src.services.document_processors.docx_processor import DOCXProcessor
from src.services.document_processors.pdf_processor import PDFProcessor
from src.services.document_processors.text_chunker import ChunkConfig, TextChunker
from src.utils.config import ConfigLoader
from src.utils.config import config as global_config
from src.utils.logger import get_logger


class DocumentService:
    """Main entry point for file validation, extraction, and chunking."""

    def __init__(self, config: Optional[ConfigLoader] = None) -> None:
        self.config = config or global_config
        self.logger = get_logger(__name__)
        self.pdf_processor = PDFProcessor()
        self.docx_processor = DOCXProcessor()
        self.chunker = TextChunker(
            ChunkConfig(
                chunk_size=self.config.get("document_processing.chunk_size", 500),
                chunk_overlap=self.config.get("document_processing.chunk_overlap", 50),
                min_chunk_size=self.config.get("document_processing.min_chunk_size", 100),
            )
        )
        self.upload_dir = Path(self.config.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self._documents: Dict[str, ProcessedDocument] = {}

    def process_document(
        self, file_path: Path, metadata: Optional[dict] = None
    ) -> ProcessedDocument:
        """Process a single document file into validated chunks."""
        start = perf_counter()
        metadata = metadata or {}
        document_id = ""

        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            file_type = self._get_file_type(file_path)
            max_size = int(self.config.max_file_size_mb) * 1024 * 1024
            file_size = file_path.stat().st_size
            if file_size > max_size:
                raise ValueError(
                    f"File exceeds max size {self.config.max_file_size_mb}MB: {file_path.name}"
                )

            document_id = self._generate_document_id(file_path)
            self.logger.info(f"Processing document {file_path.name} ({document_id})")

            if file_type == DocumentType.PDF:
                valid, message = self.pdf_processor.validate_pdf(file_path)
                if not valid:
                    raise ValueError(message)
                pages_data = self.pdf_processor.extract_text_with_metadata(file_path)
                source_meta = self.pdf_processor.get_document_metadata(file_path)
            elif file_type == DocumentType.DOCX:
                valid, message = self.docx_processor.validate_docx(file_path)
                if not valid:
                    raise ValueError(message)
                pages_data = self.docx_processor.extract_text_with_metadata(file_path)
                source_meta = self.docx_processor.get_document_metadata(file_path)
            else:
                pages_data = self._process_text_file(file_path)
                source_meta = {"page_count": 1}

            chunk_dicts = self.chunker.chunk_document(pages_data, document_id)
            chunk_models = [DocumentChunk(**chunk) for chunk in chunk_dicts if chunk.get("content")]

            doc_metadata = DocumentMetadata(
                filename=file_path.name,
                file_type=file_type,
                file_size=file_size,
                page_count=source_meta.get("page_count"),
                subject=metadata.get("subject"),
                course=metadata.get("course"),
                tags=metadata.get("tags") or [],
                original_path=str(file_path.resolve()),
            )

            processed = ProcessedDocument(
                document_id=document_id,
                metadata=doc_metadata,
                chunks=chunk_models,
                total_chunks=len(chunk_models),
                total_tokens=sum(chunk.token_count for chunk in chunk_models),
                processing_status=ProcessingStatus.COMPLETED,
                processing_time=perf_counter() - start,
            )
            self._documents[document_id] = processed
            self.logger.info(
                "Processed %s: chunks=%s, tokens=%s",
                file_path.name,
                processed.total_chunks,
                processed.total_tokens,
            )
            return processed
        except Exception as exc:
            self.logger.exception(f"Failed processing {file_path}: {exc}")
            failed_meta = DocumentMetadata(
                filename=file_path.name if file_path else "unknown",
                file_type=self._safe_file_type(file_path),
                file_size=(file_path.stat().st_size if file_path and file_path.exists() else 1),
                tags=metadata.get("tags") or [],
                subject=metadata.get("subject"),
                course=metadata.get("course"),
                original_path=str(file_path) if file_path else None,
            )
            return ProcessedDocument(
                document_id=document_id or f"doc_failed_{uuid.uuid4().hex[:8]}",
                metadata=failed_meta,
                chunks=[],
                total_chunks=0,
                total_tokens=0,
                processing_status=ProcessingStatus.FAILED,
                processing_time=perf_counter() - start,
                error_message=str(exc),
            )

    def _generate_document_id(self, file_path: Path) -> str:
        """Create stable-ish id using file hash prefix + UUID suffix."""
        md5 = hashlib.md5()
        with file_path.open("rb") as fp:
            for block in iter(lambda: fp.read(8192), b""):
                md5.update(block)
        digest = md5.hexdigest()[:8]
        suffix = uuid.uuid4().hex[:6]
        return f"doc_{digest}_{suffix}"

    def _get_file_type(self, file_path: Path) -> DocumentType:
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            return DocumentType.PDF
        if ext == ".docx":
            return DocumentType.DOCX
        if ext == ".txt":
            return DocumentType.TXT
        if ext == ".md":
            return DocumentType.MD
        raise ValueError(f"Unsupported file type: {ext}")

    def _safe_file_type(self, file_path: Optional[Path]) -> DocumentType:
        try:
            if file_path:
                return self._get_file_type(file_path)
        except Exception:
            pass
        return DocumentType.TXT

    def _process_text_file(self, file_path: Path) -> List[Dict]:
        """Process text/markdown files as a single page."""
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        return [{"page_number": 1, "content": content, "tables": "", "has_images": False}]

    def get_document(self, document_id: str) -> Optional[ProcessedDocument]:
        return self._documents.get(document_id)

    def list_documents(self) -> List[Dict]:
        return [
            {
                "document_id": doc.document_id,
                "filename": doc.metadata.filename,
                "chunks": doc.total_chunks,
                "upload_time": doc.metadata.upload_timestamp.isoformat(),
                "status": doc.processing_status.value,
            }
            for doc in self._documents.values()
        ]

    def delete_document(self, document_id: str) -> bool:
        if document_id in self._documents:
            del self._documents[document_id]
            return True
        return False

    def get_document_chunks(self, document_id: str) -> List[DocumentChunk]:
        doc = self.get_document(document_id)
        return doc.chunks if doc else []

    def search_documents(self, query: str, top_k: int = 5) -> List[Dict]:
        """Lightweight keyword scoring across chunks for quick local search."""
        terms = [term.lower() for term in query.split() if term.strip()]
        if not terms:
            return []

        scored: List[Dict] = []
        for doc in self._documents.values():
            for chunk in doc.chunks:
                content = chunk.content.lower()
                score = sum(content.count(term) for term in terms)
                if score > 0:
                    scored.append(
                        {
                            "document_id": doc.document_id,
                            "chunk_id": chunk.chunk_id,
                            "content": chunk.content,
                            "page_number": chunk.page_number,
                            "section_title": chunk.section_title,
                            "score": float(score),
                        }
                    )
        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]
