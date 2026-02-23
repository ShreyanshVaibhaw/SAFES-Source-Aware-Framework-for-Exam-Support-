"""Query, study guide, and practice test routes."""

from __future__ import annotations

from typing import AsyncGenerator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from src.api.dependencies import get_exam_helper, get_rag_engine
from src.api.models import (
    PracticeTestRequest,
    PracticeTestResponse,
    QueryRequest,
    QueryResponse,
    StudyGuideRequest,
    StudyGuideResponse,
)
from src.core.rag_engine import RAGEngine
from src.services.exam_helper import ExamHelperService

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
def query_documents(
    request: QueryRequest, rag_engine: RAGEngine = Depends(get_rag_engine)
) -> QueryResponse:
    """Run a grounded RAG query."""
    result = rag_engine.answer_question(
        question=request.question,
        bloom_level=request.bloom_level,
        top_k=request.top_k,
        document_ids=request.document_ids,
        check_hallucination=request.check_hallucination,
        include_citations=request.include_citations,
    )
    return QueryResponse(**result)


@router.post("/query/stream")
def stream_query(
    request: QueryRequest, rag_engine: RAGEngine = Depends(get_rag_engine)
) -> StreamingResponse:
    """Stream answer word-by-word for simple progressive UX."""
    result = rag_engine.answer_question(
        question=request.question,
        bloom_level=request.bloom_level,
        top_k=request.top_k,
        document_ids=request.document_ids,
        check_hallucination=request.check_hallucination,
        include_citations=request.include_citations,
    )
    text = result["answer"]

    async def token_stream() -> AsyncGenerator[str, None]:
        for token in text.split():
            yield token + " "

    return StreamingResponse(token_stream(), media_type="text/plain")


@router.post("/study/guide", response_model=StudyGuideResponse)
def generate_study_guide(
    request: StudyGuideRequest,
    exam_helper: ExamHelperService = Depends(get_exam_helper),
) -> StudyGuideResponse:
    guide = exam_helper.generate_study_guide(topics=request.topics, level=request.level)
    return StudyGuideResponse(guide=guide)


@router.post("/study/practice-test", response_model=PracticeTestResponse)
def generate_practice_test(
    request: PracticeTestRequest,
    exam_helper: ExamHelperService = Depends(get_exam_helper),
) -> PracticeTestResponse:
    payload = exam_helper.generate_practice_test(
        topics=request.topics,
        num_questions=request.num_questions,
        difficulty=request.difficulty,
    )
    return PracticeTestResponse(**payload)


@router.get("/study/key-concepts")
def get_key_concepts(exam_helper: ExamHelperService = Depends(get_exam_helper)):
    return {"concepts": exam_helper.extract_key_concepts()}
