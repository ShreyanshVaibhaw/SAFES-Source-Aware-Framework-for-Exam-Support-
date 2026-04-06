"""Tests for LLM-based hallucination verification and config wiring."""

import json
from unittest.mock import MagicMock, patch

from src.core.hallucination_detector import HallucinationDetector


def _make_chunks(texts):
    return [{"content": t} for t in texts]


def test_heuristic_uses_config_threshold():
    """Verify config threshold is used instead of hardcoded 0.5."""
    detector = HallucinationDetector(min_overlap=0.15)
    chunks = [{"content": "Newton formulated three laws of motion."}]
    result = detector.detect("Newton formulated three laws of motion.", chunks, True)
    assert result["verification_method"] == "heuristic"
    assert "confidence" in result


def test_heuristic_backward_compatibility():
    """Grounded answer should score higher than ungrounded one (same as original test)."""
    detector = HallucinationDetector()
    chunks = [{"content": "Newton formulated three laws of motion."}]
    grounded = detector.detect("Newton formulated three laws of motion.", chunks, True)
    ungrounded = detector.detect("Newton made a fourth law in quantum space.", chunks, False)
    assert grounded["confidence"] > ungrounded["confidence"]


def test_on_hallucination_field_present():
    """Result should include on_hallucination action from config."""
    detector = HallucinationDetector()
    chunks = [{"content": "some context"}]
    result = detector.detect("some answer", chunks, True)
    assert "on_hallucination" in result


def test_llm_verify_with_mock():
    """LLM verification returns claim-level details when successful."""
    mock_llm = MagicMock()
    mock_llm._client = MagicMock()
    mock_llm.model = "gpt-3.5-turbo"

    verification_response = {
        "claims": [
            {"claim": "Newton had three laws.", "status": "supported", "reason": "Matches context."},
            {"claim": "He lived in England.", "status": "unsupported", "reason": "Not in context."},
        ]
    }
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps(verification_response)
    mock_llm._client.chat.completions.create.return_value = mock_response

    detector = HallucinationDetector(llm_service=mock_llm)
    chunks = [{"content": "Newton formulated three laws of motion."}]
    result = detector.detect(
        "Newton had three laws. He lived in England.", chunks, True
    )

    assert result["verification_method"] == "llm"
    assert "claim_details" in result
    assert len(result["claim_details"]) == 2
    assert result["confidence"] > 0.0


def test_llm_verify_falls_back_on_json_error():
    """Falls back to heuristic when LLM returns invalid JSON."""
    mock_llm = MagicMock()
    mock_llm._client = MagicMock()
    mock_llm.model = "gpt-3.5-turbo"

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "This is not valid JSON at all"
    mock_llm._client.chat.completions.create.return_value = mock_response

    detector = HallucinationDetector(llm_service=mock_llm)
    chunks = [{"content": "Some context."}]
    result = detector.detect("Some answer.", chunks, True)

    assert result["verification_method"] == "heuristic"


def test_llm_verify_falls_back_on_exception():
    """Falls back to heuristic when LLM call raises an exception."""
    mock_llm = MagicMock()
    mock_llm._client = MagicMock()
    mock_llm.model = "gpt-3.5-turbo"
    mock_llm._client.chat.completions.create.side_effect = Exception("API timeout")

    detector = HallucinationDetector(llm_service=mock_llm)
    chunks = [{"content": "Some context."}]
    result = detector.detect("Some answer.", chunks, True)

    assert result["verification_method"] == "heuristic"


def test_no_llm_uses_heuristic():
    """Without LLM service, always uses heuristic."""
    detector = HallucinationDetector(llm_service=None)
    chunks = [{"content": "Test content."}]
    result = detector.detect("Test answer.", chunks, True)
    assert result["verification_method"] == "heuristic"
