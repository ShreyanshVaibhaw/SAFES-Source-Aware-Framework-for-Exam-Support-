from src.services.llm_service import LLMService


def test_fallback_comparison_returns_structured_output():
    """Without LLM, comparison should still return structured text."""
    service = LLMService()
    result = service.generate_comparison(
        topic_a="TCP",
        topic_b="UDP",
        context_a="TCP provides reliable ordered delivery of data packets.",
        context_b="UDP is connectionless and provides faster delivery without guarantees.",
    )
    assert "TCP" in result
    assert "UDP" in result
    assert "Similarities" in result or "Differences" in result


def test_fallback_comparison_empty_context():
    """Comparison with no context still returns structured output."""
    service = LLMService()
    result = service.generate_comparison(
        topic_a="Alpha", topic_b="Beta", context_a="", context_b=""
    )
    assert "Alpha" in result
    assert "Beta" in result
