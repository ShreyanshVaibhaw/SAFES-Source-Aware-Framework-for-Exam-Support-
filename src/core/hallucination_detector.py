"""Heuristic grounding and hallucination checks."""

from __future__ import annotations

import re
from typing import Dict, List


class HallucinationDetector:
    """Estimate grounding confidence using lexical overlap and citation checks."""

    def __init__(self, min_overlap: float = 0.15) -> None:
        self.min_overlap = min_overlap

    def detect(
        self,
        answer: str,
        retrieved_chunks: List[Dict],
        citations_present: bool = True,
    ) -> Dict:
        """Return grounding report for generated answer."""
        context_text = "\n".join(chunk.get("content", "") for chunk in retrieved_chunks)
        overlap = self._keyword_overlap(answer, context_text)
        support_score = min(1.0, overlap * 1.5)
        citation_bonus = 0.1 if citations_present else -0.1
        confidence = max(0.0, min(1.0, support_score + citation_bonus))

        unsupported_claims = self._unsupported_sentences(answer, context_text)
        is_grounded = confidence >= 0.5 and len(unsupported_claims) <= 2

        recommendations: List[str] = []
        if overlap < self.min_overlap:
            recommendations.append("Retrieve more specific chunks before answering.")
        if not citations_present:
            recommendations.append("Include citations for key factual claims.")
        if unsupported_claims:
            recommendations.append("Revise or remove unsupported statements.")

        return {
            "is_grounded": is_grounded,
            "confidence": round(confidence, 3),
            "keyword_overlap": round(overlap, 3),
            "unsupported_claims": unsupported_claims,
            "recommendations": recommendations,
        }

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
        sentences = [s.strip() for s in re.split(r"[.!?]\s*", answer) if s.strip()]
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
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "to",
            "of",
            "for",
            "in",
            "on",
            "and",
            "or",
            "with",
            "that",
            "this",
        }
        return {term for term in re.findall(r"[a-zA-Z0-9_]+", text.lower()) if term not in stop}
