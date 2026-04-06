"""Heuristic and LLM-based grounding and hallucination checks."""

from __future__ import annotations

import json
import re
from typing import Dict, List, Optional

from src.utils.config import ConfigLoader
from src.utils.config import config as global_config
from src.utils.logger import get_logger


class HallucinationDetector:
    """Estimate grounding confidence using lexical overlap, citation checks,
    and optional LLM-based claim verification."""

    def __init__(
        self,
        min_overlap: float = 0.15,
        config: Optional[ConfigLoader] = None,
        llm_service=None,
        nlp_service=None,
    ) -> None:
        self.logger = get_logger(__name__)
        self.min_overlap = min_overlap
        self.config = config or global_config
        self._llm = llm_service
        self._nlp = nlp_service

        # Read config values (with sensible defaults matching original behavior)
        self.confidence_threshold = float(
            self.config.get("hallucination_control.confidence_threshold", 0.5)
        )
        self.max_unsupported_ratio = float(
            self.config.get("hallucination_control.max_unsupported_ratio", 0.2)
        )
        self.on_hallucination = self.config.get(
            "hallucination_control.on_hallucination", "warn"
        )
        self.verify_sources = self.config.get(
            "hallucination_control.verify_sources", True
        )

    def detect(
        self,
        answer: str,
        retrieved_chunks: List[Dict],
        citations_present: bool = True,
    ) -> Dict:
        """Return grounding report for generated answer.

        Uses LLM verification when available and verify_sources is True,
        falls back to heuristic otherwise.
        """
        # Try LLM verification first if available
        if (
            self.verify_sources
            and self._llm is not None
            and getattr(self._llm, "_client", None) is not None
        ):
            try:
                return self._llm_verify(answer, retrieved_chunks, citations_present)
            except Exception as exc:
                self.logger.warning(f"LLM verification failed, using heuristic: {exc}")

        return self._heuristic_detect(answer, retrieved_chunks, citations_present)

    def _heuristic_detect(
        self,
        answer: str,
        retrieved_chunks: List[Dict],
        citations_present: bool = True,
    ) -> Dict:
        """Heuristic grounding check using keyword overlap."""
        context_text = "\n".join(chunk.get("content", "") for chunk in retrieved_chunks)
        overlap = self._keyword_overlap(answer, context_text)
        support_score = min(1.0, overlap * 1.5)
        citation_bonus = 0.1 if citations_present else -0.1
        confidence = max(0.0, min(1.0, support_score + citation_bonus))

        unsupported_claims = self._unsupported_sentences(answer, context_text)

        # Use config thresholds instead of hardcoded values
        max_unsupported = max(1, int(len(self._split_sentences(answer)) * self.max_unsupported_ratio))
        is_grounded = confidence >= self.confidence_threshold and len(unsupported_claims) <= max_unsupported

        recommendations: List[str] = []
        if overlap < self.min_overlap:
            recommendations.append("Retrieve more specific chunks before answering.")
        if not citations_present:
            recommendations.append("Include citations for key factual claims.")
        if unsupported_claims:
            recommendations.append("Revise or remove unsupported statements.")

        result = {
            "is_grounded": is_grounded,
            "confidence": round(confidence, 3),
            "keyword_overlap": round(overlap, 3),
            "unsupported_claims": unsupported_claims,
            "recommendations": recommendations,
            "verification_method": "heuristic",
            "on_hallucination": self.on_hallucination,
        }
        return result

    def _llm_verify(
        self,
        answer: str,
        retrieved_chunks: List[Dict],
        citations_present: bool,
    ) -> Dict:
        """LLM-based claim-by-claim verification."""
        from src.core.prompts import build_verification_prompt

        claims = self._split_sentences(answer)
        if not claims:
            return self._heuristic_detect(answer, retrieved_chunks, citations_present)

        context_text = "\n".join(chunk.get("content", "") for chunk in retrieved_chunks)
        prompt = build_verification_prompt(claims, context_text)

        response = self._llm._client.chat.completions.create(
            model=self._llm.model,
            temperature=0.0,
            max_tokens=1000,
            messages=[
                {"role": "system", "content": "You are a factual verification assistant. Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
        )
        raw = (response.choices[0].message.content or "").strip()

        # Parse JSON response
        try:
            # Handle markdown code blocks
            if "```" in raw:
                raw = re.search(r"```(?:json)?\s*(.*?)```", raw, re.DOTALL)
                raw = raw.group(1).strip() if raw else "{}"
            verification = json.loads(raw)
        except (json.JSONDecodeError, AttributeError):
            self.logger.warning("Failed to parse LLM verification JSON, falling back to heuristic")
            return self._heuristic_detect(answer, retrieved_chunks, citations_present)

        # Compute confidence from claim assessments
        claim_details = verification.get("claims", [])
        if not claim_details:
            return self._heuristic_detect(answer, retrieved_chunks, citations_present)

        supported = sum(1 for c in claim_details if c.get("status") == "supported")
        partial = sum(1 for c in claim_details if c.get("status") == "partially_supported")
        unsupported_count = sum(1 for c in claim_details if c.get("status") == "unsupported")
        total = len(claim_details)

        confidence = (supported + 0.5 * partial) / total if total else 0.0
        citation_bonus = 0.05 if citations_present else -0.05
        confidence = max(0.0, min(1.0, confidence + citation_bonus))

        unsupported_claims = [
            c.get("claim", "") for c in claim_details if c.get("status") == "unsupported"
        ]

        max_unsupported = max(1, int(total * self.max_unsupported_ratio))
        is_grounded = confidence >= self.confidence_threshold and unsupported_count <= max_unsupported

        recommendations: List[str] = []
        if unsupported_claims:
            recommendations.append("Revise or remove unsupported statements.")
        if not citations_present:
            recommendations.append("Include citations for key factual claims.")

        return {
            "is_grounded": is_grounded,
            "confidence": round(confidence, 3),
            "keyword_overlap": round(self._keyword_overlap(answer, context_text), 3),
            "unsupported_claims": unsupported_claims[:5],
            "recommendations": recommendations,
            "verification_method": "llm",
            "claim_details": claim_details,
            "on_hallucination": self.on_hallucination,
        }

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences using NLP service or regex fallback."""
        if self._nlp:
            try:
                return self._nlp.sentence_split(text)
            except Exception:
                pass
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

    def _keyword_overlap(self, answer: str, context: str) -> float:
        answer_terms = self._terms(answer)
        context_terms = self._terms(context)
        if not answer_terms:
            return 0.0
        intersect = answer_terms & context_terms
        return len(intersect) / len(answer_terms)

    def _unsupported_sentences(self, answer: str, context: str) -> List[str]:
        context_terms = self._terms(context)
        unsupported: List[str] = []
        sentences = self._split_sentences(answer)
        for sentence in sentences:
            terms = self._terms(sentence)
            if not terms:
                continue
            overlap = len(terms & context_terms) / len(terms)
            if overlap < self.min_overlap:
                unsupported.append(sentence)
        return unsupported[:5]

    def _terms(self, text: str) -> set[str]:
        stop = {
            "the", "a", "an", "is", "are", "was", "were", "to", "of", "for",
            "in", "on", "and", "or", "with", "that", "this",
        }
        return {term for term in re.findall(r"[a-zA-Z0-9_]+", text.lower()) if term not in stop}
