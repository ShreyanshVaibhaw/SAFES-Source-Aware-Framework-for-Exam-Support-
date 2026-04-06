"""Exam helper features for guides, tests, and key concept extraction."""

from __future__ import annotations

from collections import Counter
from typing import Dict, List

from src.core.blooms_taxonomy import BloomsTaxonomyService
from src.services.llm_service import LLMService
from src.services.retrieval_service import RetrievalService


class ExamHelperService:
    """Service for exam preparation utilities."""

    def __init__(self, retrieval_service: RetrievalService, llm_service: LLMService) -> None:
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service
        self.blooms = BloomsTaxonomyService()

    def generate_study_guide(self, topics: List[str], level: str = "understand") -> str:
        query = " ".join(topics) if topics else "core concepts"
        results = self.retrieval_service.semantic_search(query, top_k=8)
        context = self.retrieval_service.build_context(results)["text"] if results else ""
        return self.llm_service.generate_study_guide(topics=topics, context=context, level=level)

    def generate_practice_test(
        self,
        topics: List[str],
        num_questions: int = 5,
        difficulty: str = "medium",
    ) -> Dict:
        query = " ".join(topics) if topics else "exam questions"
        results = self.retrieval_service.semantic_search(query, top_k=10)
        context = self.retrieval_service.build_context(results)["text"] if results else ""
        return self.llm_service.generate_practice_test(
            topics=topics,
            context=context,
            num_questions=num_questions,
            difficulty=difficulty,
        )

    def compare_topics(self, topic_a: str, topic_b: str) -> Dict:
        """Compare two topics using retrieved context."""
        results_a = self.retrieval_service.semantic_search(topic_a, top_k=5)
        results_b = self.retrieval_service.semantic_search(topic_b, top_k=5)
        context_a = self.retrieval_service.build_context(results_a)["text"] if results_a else ""
        context_b = self.retrieval_service.build_context(results_b)["text"] if results_b else ""

        comparison = self.llm_service.generate_comparison(
            topic_a=topic_a, topic_b=topic_b, context_a=context_a, context_b=context_b
        )
        return {
            "topic_a": topic_a,
            "topic_b": topic_b,
            "comparison": comparison,
            "sources_a": len(results_a),
            "sources_b": len(results_b),
        }

    def extract_key_concepts(self, max_terms: int = 20) -> List[Dict]:
        """Extract frequent terms from all indexed chunks."""
        all_results = self.retrieval_service.vector_store.similarity_search(
            query_embedding=[0.0] * self.retrieval_service.embedding_service.embedding_dim,
            top_k=5000,
            document_ids=None,
        )
        words: List[str] = []
        for item in all_results:
            text = item.get("content", "")
            words.extend([w.lower() for w in text.split() if len(w) > 4])
        counts = Counter(words)
        return [
            {"concept": term, "frequency": freq} for term, freq in counts.most_common(max_terms)
        ]
