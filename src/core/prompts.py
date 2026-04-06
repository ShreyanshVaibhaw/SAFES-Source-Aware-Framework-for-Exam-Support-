"""Prompt templates for grounded RAG responses."""

from __future__ import annotations

from typing import List

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


def build_verification_prompt(claims: List[str], context: str) -> str:
    """Build prompt for LLM-based claim verification."""
    claims_text = "\n".join(f"{i+1}. {claim}" for i, claim in enumerate(claims))
    return (
        "Verify each claim below against the provided context.\n"
        "For each claim, determine if it is 'supported', 'partially_supported', or 'unsupported' by the context.\n\n"
        f"Context:\n{context}\n\n"
        f"Claims to verify:\n{claims_text}\n\n"
        "Respond with a JSON object in this exact format:\n"
        '{"claims": [\n'
        '  {"claim": "<claim text>", "status": "supported|partially_supported|unsupported", "reason": "<brief explanation>"}\n'
        "]}\n"
    )
