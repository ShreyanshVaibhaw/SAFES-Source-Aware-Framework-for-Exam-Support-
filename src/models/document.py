"""Document models used across processing, retrieval, and API layers."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class DocumentType(str, Enum):
    """Supported document types."""

    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MD = "md"


class ProcessingStatus(str, Enum):
    """Processing lifecycle status."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentMetadata(BaseModel):
    """Metadata for an uploaded document."""

    filename: str
    file_type: DocumentType
    file_size: int
    page_count: Optional[int] = None
    upload_timestamp: datetime = Field(default_factory=datetime.utcnow)
    subject: Optional[str] = None
    course: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    original_path: Optional[str] = None

    @field_validator("filename")
    @classmethod
    def validate_filename(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("filename must not be empty")
        return value.strip()

    @field_validator("file_size")
    @classmethod
    def validate_file_size(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("file_size must be > 0")
        return value


class DocumentChunk(BaseModel):
    """A chunk of text derived from a source document."""

    chunk_id: str
    document_id: str
    content: str
    page_number: Optional[int] = None
    section_title: Optional[str] = None
    start_char: int = 0
    end_char: int = 0
    token_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("chunk_id", "document_id")
    @classmethod
    def validate_ids(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("ids must not be empty")
        return value.strip()

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("chunk content must not be empty")
        return cleaned

    @field_validator("start_char", "end_char", "token_count")
    @classmethod
    def validate_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("numeric values must be >= 0")
        return value


class ProcessedDocument(BaseModel):
    """Container for the full processed output of an uploaded document."""

    document_id: str
    metadata: DocumentMetadata
    chunks: List[DocumentChunk] = Field(default_factory=list)
    total_chunks: int = 0
    total_tokens: int = 0
    processing_status: ProcessingStatus = ProcessingStatus.PENDING
    processing_time: Optional[float] = None
    error_message: Optional[str] = None

    @field_validator("document_id")
    @classmethod
    def validate_document_id(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("document_id must not be empty")
        return value.strip()

    @field_validator("total_chunks", "total_tokens")
    @classmethod
    def validate_totals(cls, value: int) -> int:
        if value < 0:
            raise ValueError("totals must be >= 0")
        return value


class DocumentUploadResponse(BaseModel):
    """Response model for successful upload/process calls."""

    document_id: str
    filename: str
    chunks_created: int
    status: str
    message: str
