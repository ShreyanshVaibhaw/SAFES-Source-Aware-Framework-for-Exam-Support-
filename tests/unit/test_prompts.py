from src.core.prompts import build_system_prompt, build_user_prompt


def test_build_system_prompt_contains_guardrails():
    prompt = build_system_prompt("understand")
    assert "provided context snippets" in prompt
    assert "Bloom guidance" in prompt


def test_build_user_prompt_contains_question_and_context():
    prompt = build_user_prompt("What is RAG?", "RAG uses retrieval + generation.")
    assert "What is RAG?" in prompt
    assert "Context snippets" in prompt
