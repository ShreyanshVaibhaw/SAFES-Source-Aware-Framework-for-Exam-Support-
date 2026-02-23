"""Prompt templates for grounded RAG responses."""

from __future__ import annotations

from src.core.blooms_taxonomy import BloomsLevel, BloomsTaxonomyService


def build_system_prompt(level: BloomsLevel | str) -> str:
    """Build system instruction text."""
    blooms = BloomsTaxonomyService()
    guideline = blooms.get_response_guideline(level)
    return (
        "You are an exam-focused study assistant.\n"
        "Answer only using the provided context snippets.\n"
        "If context is insufficient, explicitly say so.\n"
        "Always be concise, accurate, and citation-oriented.\n"
        f"Bloom guidance: {guideline}"
    )


def build_user_prompt(question: str, context: str) -> str:
    """Build user prompt with retrieval context."""
    return (
        f"Question:\n{question}\n\n"
        f"Context snippets:\n{context}\n\n"
        "Instructions:\n"
        "- Use only the context snippets.\n"
        "- Prefer short exam-ready language.\n"
        "- Avoid adding external facts.\n"
    )
