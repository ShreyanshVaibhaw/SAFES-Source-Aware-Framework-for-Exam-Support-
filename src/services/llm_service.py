"""LLM provider wrapper with safe local fallback."""

from __future__ import annotations

from typing import Dict, List, Optional

from src.core.prompts import build_system_prompt, build_user_prompt
from src.utils.config import ConfigLoader
from src.utils.config import config as global_config
from src.utils.logger import get_logger

try:  # pragma: no cover - optional runtime
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


class LLMService:
    """Generate grounded responses through OpenAI when available, else fallback."""

    def __init__(self, config: Optional[ConfigLoader] = None) -> None:
        self.config = config or global_config
        self.logger = get_logger(__name__)
        self.api_key = self.config.openai_api_key
        self.model = self.config.llm_model
        self.temperature = float(self.config.llm_temperature)
        self.max_tokens = int(self.config.llm_max_tokens)
        self._client = None
        if self.api_key and OpenAI is not None:
            self._client = OpenAI(api_key=self.api_key)

    def generate_answer(self, question: str, context: str, bloom_level: str = "understand") -> str:
        """Return grounded answer text."""
        if self._client is None:
            return self._fallback_answer(question=question, context=context)

        try:  # pragma: no cover - external API
            system_prompt = build_system_prompt(bloom_level)
            user_prompt = build_user_prompt(question, context)
            result = self._client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return (result.choices[0].message.content or "").strip()
        except Exception as exc:  # pragma: no cover - external API
            self.logger.warning(f"OpenAI call failed; using fallback answer: {exc}")
            return self._fallback_answer(question=question, context=context)

    def generate_study_guide(
        self, topics: List[str], context: str, level: str = "understand"
    ) -> str:
        """Generate simple topic-by-topic study guide."""
        sections = [f"# Study Guide ({level.title()})", ""]
        context_lines = [line.strip() for line in context.splitlines() if line.strip()]
        sample = " ".join(context_lines[:8])[:400]
        for topic in topics:
            sections.append(f"## {topic}")
            sections.append(f"- Core concept: {sample or 'No indexed context available yet.'}")
            sections.append("- Key terms to revise: define, compare, apply.")
            sections.append("- Exam tip: reference cited definitions and examples.")
            sections.append("")
        return "\n".join(sections).strip()

    def generate_practice_test(
        self,
        topics: List[str],
        context: str,
        num_questions: int = 5,
        difficulty: str = "medium",
    ) -> Dict:
        """Generate deterministic practice questions from topics."""
        questions = []
        topic_cycle = topics or ["General"]
        for i in range(num_questions):
            topic = topic_cycle[i % len(topic_cycle)]
            questions.append(
                {
                    "id": i + 1,
                    "topic": topic,
                    "difficulty": difficulty,
                    "question": (f"Q{i + 1}. Explain {topic} and give one exam-relevant example."),
                    "hint": f"Use definitions and evidence from uploaded sources on {topic}.",
                }
            )
        return {"difficulty": difficulty, "questions": questions}

    def _fallback_answer(self, question: str, context: str) -> str:
        """Context-only fallback to keep system operational offline."""
        snippets = [line.strip() for line in context.splitlines() if line.strip()]
        if not snippets:
            return (
                "I could not find enough information in the uploaded materials "
                "to answer this question."
            )
        preview = " ".join(snippets[:5])[:600]
        return (
            f"Based on the uploaded materials, here is the best supported answer:\n\n{preview}\n\n"
            f"Question focus: {question}"
        )
