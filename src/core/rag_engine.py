"""RAG orchestration across retrieval, generation, citations, and verification."""

from __future__ import annotations

from typing import Dict, List, Optional

from src.core.blooms_taxonomy import BloomsTaxonomyService
from src.core.citation_manager import CitationManager
from src.core.hallucination_detector import HallucinationDetector
from src.services.llm_service import LLMService
from src.services.retrieval_service import RetrievalService


class RAGEngine:
    """Main orchestration class for question answering."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_service: Optional[LLMService] = None,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service or LLMService()
        self.citation_manager = CitationManager()
        self.hallucination_detector = HallucinationDetector()
        self.blooms = BloomsTaxonomyService()

    def answer_question(
        self,
        question: str,
        bloom_level: Optional[str] = None,
        top_k: int = 5,
        document_ids: Optional[List[str]] = None,
        check_hallucination: bool = True,
        include_citations: bool = True,
    ) -> Dict:
        """Generate an answer grounded in retrieved chunks."""
        level = bloom_level or self.blooms.detect_level(question).value
        results = self.retrieval_service.semantic_search(
            query=question,
            top_k=top_k,
            document_ids=document_ids,
        )

        if not results:
            return {
                "question": question,
                "answer": "No relevant content found in uploaded documents.",
                "bloom_level": level,
                "citations": [],
                "confidence": 0.0,
                "grounding": {
                    "is_grounded": False,
                    "confidence": 0.0,
                    "recommendations": ["Upload more relevant source material."],
                },
            }

        context_payload = self.retrieval_service.build_context(results)
        answer = self.llm_service.generate_answer(question, context_payload["text"], level)
        citations = self.citation_manager.register_citations(results)

        answer_with_citations = answer
        if include_citations:
            answer_with_citations = self.citation_manager.enrich_response(
                answer, citations, mode="footnote"
            )

        citation_refs_valid = self.citation_manager.verify_citation_references(
            answer_with_citations, citations
        )
        grounding = (
            self.hallucination_detector.detect(
                answer=answer_with_citations,
                retrieved_chunks=results,
                citations_present=citation_refs_valid or bool(citations),
            )
            if check_hallucination
            else {
                "is_grounded": True,
                "confidence": 1.0,
                "keyword_overlap": 1.0,
                "unsupported_claims": [],
                "recommendations": [],
            }
        )

        return {
            "question": question,
            "answer": answer_with_citations,
            "bloom_level": level,
            "citations": citations,
            "confidence": grounding["confidence"],
            "grounding": grounding,
            "retrieved_chunks": [
                {
                    "id": item.get("id"),
                    "document_id": item.get("document_id"),
                    "score": item.get("score"),
                    "page_number": (item.get("metadata") or {}).get("page_number"),
                    "section_title": (item.get("metadata") or {}).get("section_title"),
                }
                for item in results
            ],
            "practice_questions": self.blooms.generate_practice_questions("the topic", level),
        }
