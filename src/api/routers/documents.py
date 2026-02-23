"""Document upload and management API routes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from src.api.dependencies import get_document_service, get_retrieval_service
from src.models.document import DocumentUploadResponse
from src.services.document_service import DocumentService
from src.services.retrieval_service import RetrievalService
from src.utils.config import config

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    subject: Optional[str] = Form(default=None),
    course: Optional[str] = Form(default=None),
    tags: Optional[str] = Form(default=None),
    document_service: DocumentService = Depends(get_document_service),
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
) -> DocumentUploadResponse:
    """Upload and process a document, then index its chunks."""
    ext = Path(file.filename).suffix.lower()
    if ext not in config.allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {ext}. Allowed: {config.allowed_extensions}",
        )

    upload_dir = Path(config.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    destination = upload_dir / file.filename
    content = await file.read()
    destination.write_bytes(content)

    parsed_tags = []
    if tags:
        try:
            parsed_tags = (
                json.loads(tags) if tags.startswith("[") else [t.strip() for t in tags.split(",")]
            )
        except Exception:
            parsed_tags = [t.strip() for t in tags.split(",") if t.strip()]

    processed = document_service.process_document(
        destination,
        metadata={"subject": subject, "course": course, "tags": parsed_tags},
    )
    if processed.processing_status.value == "failed":
        raise HTTPException(status_code=400, detail=processed.error_message or "Processing failed.")

    retrieval_service.index_document(processed)
    return DocumentUploadResponse(
        document_id=processed.document_id,
        filename=processed.metadata.filename,
        chunks_created=processed.total_chunks,
        status=processed.processing_status.value,
        message="Document uploaded, processed, and indexed successfully.",
    )


@router.get("")
def list_documents(document_service: DocumentService = Depends(get_document_service)):
    """List uploaded documents."""
    return {"documents": document_service.list_documents()}


@router.get("/{document_id}")
def get_document(
    document_id: str, document_service: DocumentService = Depends(get_document_service)
):
    """Get one processed document."""
    document = document_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")
    return document.model_dump()


@router.get("/{document_id}/chunks")
def get_document_chunks(
    document_id: str, document_service: DocumentService = Depends(get_document_service)
):
    """Get all chunks for one document."""
    chunks = document_service.get_document_chunks(document_id)
    if not chunks:
        raise HTTPException(status_code=404, detail="No chunks found for document.")
    return {"document_id": document_id, "chunks": [chunk.model_dump() for chunk in chunks]}


@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    document_service: DocumentService = Depends(get_document_service),
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
):
    """Delete document and indexed vectors."""
    removed_doc = document_service.delete_document(document_id)
    removed_vectors = retrieval_service.delete_document(document_id)
    if not removed_doc and removed_vectors == 0:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {"document_id": document_id, "deleted": True, "vectors_removed": removed_vectors}
