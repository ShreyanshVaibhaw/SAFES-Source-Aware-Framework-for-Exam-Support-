"""RAG orchestration across retrieval, generation, citations, and verification."""

from __future__ import annotations

from time import perf_counter
from typing import Dict, List, Optional

from src.core.blooms_taxonomy import BloomsTaxonomyService
from src.core.citation_manager import CitationManager
from src.core.hallucination_detector import HallucinationDetector
from src.services.llm_service import LLMService
from src.services.retrieval_service import RetrievalService
from src.utils.config import ConfigLoader
from src.utils.config import config as global_config


class RAGEngine:
    """Main orchestration class for question answering."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_service: Optional[LLMService] = None,
        config: Optional[ConfigLoader] = None,
        nlp_service=None,
        query_history_service=None,
    ) -> None:
        self.config = config or global_config
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service or LLMService()
        self.citation_manager = CitationManager()
        self.hallucination_detector = HallucinationDetector(
            config=self.config,
            llm_service=self.llm_service,
            nlp_service=nlp_service,
        )
        self.blooms = BloomsTaxonomyService()
        self._history = query_history_service

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
        start = perf_counter()

        level = bloom_level or self.blooms.detect_level(question).value
        results = self.retrieval_service.semantic_search(
            query=question,
            top_k=top_k,
            document_ids=document_ids,
        )

        if not results:
            result = {
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
            self._record_history(result, start)
            return result

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

        # Apply on_hallucination action
        on_action = grounding.get("on_hallucination", "warn")
        if not grounding.get("is_grounded", True) and on_action == "refuse":
            answer_with_citations = (
                "I cannot provide a reliable answer based on the uploaded materials. "
                "The generated response did not meet the grounding confidence threshold. "
                "Please upload more relevant source material or rephrase your question."
            )

        result = {
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

        self._record_history(result, start)
        return result

    def _record_history(self, result: Dict, start_time: float) -> None:
        """Record query to history service if available."""
        if self._history is None:
            return
        try:
            elapsed_ms = (perf_counter() - start_time) * 1000
            doc_ids = list({
                c.get("document_id", "")
                for c in result.get("retrieved_chunks", [])
                if c.get("document_id")
            })
            self._history.record_query(
                question=result["question"],
                answer=result["answer"],
                bloom_level=result.get("bloom_level", "understand"),
                confidence=result.get("confidence", 0.0),
                citations_count=len(result.get("citations", [])),
                document_ids=doc_ids,
                response_time_ms=elapsed_ms,
            )
        except Exception:
            pass  # Never let history recording break the query pipeline
