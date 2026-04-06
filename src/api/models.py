"""API request/response schemas."""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=2)
    bloom_level: Optional[str] = None
    top_k: int = 5
    document_ids: Optional[List[str]] = None
    check_hallucination: bool = True
    include_citations: bool = True


class QueryResponse(BaseModel):
    question: str
    answer: str
    bloom_level: str
    citations: List[Dict]
    confidence: float
    grounding: Dict
    retrieved_chunks: List[Dict] = Field(default_factory=list)
    practice_questions: List[str] = Field(default_factory=list)


class StudyGuideRequest(BaseModel):
    topics: List[str] = Field(default_factory=list)
    level: str = "understand"


class StudyGuideResponse(BaseModel):
    guide: str


class PracticeTestRequest(BaseModel):
    topics: List[str] = Field(default_factory=list)
    difficulty: str = "medium"
    num_questions: int = 5


class PracticeTestResponse(BaseModel):
    difficulty: str
    questions: List[Dict]


class TopicCompareRequest(BaseModel):
    topic_a: str = Field(..., min_length=1)
    topic_b: str = Field(..., min_length=1)


class TopicCompareResponse(BaseModel):
    topic_a: str
    topic_b: str
    comparison: str
    sources_a: int
    sources_b: int


class QueryHistoryResponse(BaseModel):
    history: List[Dict]
    total: int


class QueryStatsResponse(BaseModel):
    total_queries: int
    avg_confidence: float
    avg_response_time_ms: float
    queries_by_bloom_level: Dict
