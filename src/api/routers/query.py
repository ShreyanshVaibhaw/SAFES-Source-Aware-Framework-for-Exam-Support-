"""Query, study guide, practice test, and history routes."""

from __future__ import annotations

from typing import AsyncGenerator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from src.api.dependencies import get_exam_helper, get_query_history, get_rag_engine
from src.api.models import (
    PracticeTestRequest,
    PracticeTestResponse,
    QueryHistoryResponse,
    QueryRequest,
    QueryResponse,
    QueryStatsResponse,
    StudyGuideRequest,
    StudyGuideResponse,
    TopicCompareRequest,
    TopicCompareResponse,
)
from src.core.rag_engine import RAGEngine
from src.services.exam_helper import ExamHelperService
from src.services.query_history_service import QueryHistoryService

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


@router.get("/query/history", response_model=QueryHistoryResponse)
def get_history(
    limit: int = 20,
    offset: int = 0,
    history: QueryHistoryService = Depends(get_query_history),
) -> QueryHistoryResponse:
    """Get query history, newest first."""
    records = history.get_history(limit=limit, offset=offset)
    return QueryHistoryResponse(history=records, total=len(history._records))


@router.get("/query/stats", response_model=QueryStatsResponse)
def get_query_stats(
    history: QueryHistoryService = Depends(get_query_history),
) -> QueryStatsResponse:
    """Get aggregate query statistics."""
    stats = history.get_stats()
    return QueryStatsResponse(**stats)


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


@router.post("/study/compare", response_model=TopicCompareResponse)
def compare_topics(
    request: TopicCompareRequest,
    exam_helper: ExamHelperService = Depends(get_exam_helper),
) -> TopicCompareResponse:
    """Compare two topics using uploaded materials."""
    result = exam_helper.compare_topics(topic_a=request.topic_a, topic_b=request.topic_b)
    return TopicCompareResponse(**result)


@router.get("/study/key-concepts")
def get_key_concepts(exam_helper: ExamHelperService = Depends(get_exam_helper)):
    return {"concepts": exam_helper.extract_key_concepts()}
