"""Query history data models."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class QueryRecord(BaseModel):
    """A single recorded query and its result."""

    query_id: str = Field(default_factory=lambda: f"qh_{uuid.uuid4().hex[:12]}")
    question: str
    answer: str
    bloom_level: str = "understand"
    confidence: float = 0.0
    citations_count: int = 0
    document_ids: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    response_time_ms: float = 0.0

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
