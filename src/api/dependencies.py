"""Shared API service dependency helpers."""

from __future__ import annotations

from fastapi import Request

from src.core.rag_engine import RAGEngine
from src.services.document_service import DocumentService
from src.services.embedding_service import EmbeddingService
from src.services.exam_helper import ExamHelperService
from src.services.llm_service import LLMService
from src.services.retrieval_service import RetrievalService
from src.utils.config import config


def init_services() -> dict:
    """Initialize application service graph once."""
    embedding = EmbeddingService(config=config)
    retrieval = RetrievalService(embedding_service=embedding, config=config)
    llm = LLMService(config=config)
    document = DocumentService(config=config)
    rag = RAGEngine(retrieval_service=retrieval, llm_service=llm)
    exam = ExamHelperService(retrieval_service=retrieval, llm_service=llm)
    return {
        "embedding_service": embedding,
        "retrieval_service": retrieval,
        "llm_service": llm,
        "document_service": document,
        "rag_engine": rag,
        "exam_helper": exam,
    }


def get_document_service(request: Request) -> DocumentService:
    return request.app.state.services["document_service"]


def get_retrieval_service(request: Request) -> RetrievalService:
    return request.app.state.services["retrieval_service"]


def get_rag_engine(request: Request) -> RAGEngine:
    return request.app.state.services["rag_engine"]


def get_exam_helper(request: Request) -> ExamHelperService:
    return request.app.state.services["exam_helper"]
