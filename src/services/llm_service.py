"""Multi-provider LLM wrapper with safe local fallback.

Supports: OpenAI, Anthropic Claude, Google Gemini, Ollama (local), and any
OpenAI-compatible API endpoint.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

from src.core.prompts import build_system_prompt, build_user_prompt
from src.utils.config import ConfigLoader
from src.utils.config import config as global_config
from src.utils.logger import get_logger

# Lazy imports for optional providers
try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # type: ignore

try:
    import anthropic as anthropic_lib
except Exception:
    anthropic_lib = None  # type: ignore

try:
    import google.generativeai as genai
except Exception:
    genai = None  # type: ignore


class LLMService:
    """Generate grounded responses through multiple LLM providers.

    Provider detection order:
    1. LLM_PROVIDER env var / config llm.provider
    2. Auto-detect from available API keys
    3. Fallback to context-only mode (no LLM needed)
    """

    def __init__(self, config: Optional[ConfigLoader] = None) -> None:
        self.config = config or global_config
        self.logger = get_logger(__name__)

        self.provider = os.getenv(
            "LLM_PROVIDER", self.config.get("llm.provider", "openai")
        ).lower()
        self.model = os.getenv("LLM_MODEL", self.config.llm_model)
        self.temperature = float(self.config.llm_temperature)
        self.max_tokens = int(self.config.llm_max_tokens)

        # Provider-specific API keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "")

        # Initialize the active client
        self._client = None
        self._active_provider = None
        self._init_provider()

    def _init_provider(self) -> None:
        """Initialize the best available LLM provider."""
        # Try configured provider first, then auto-detect
        providers_to_try = [self.provider]
        if self.provider not in ["openai", "anthropic", "gemini", "ollama"]:
            providers_to_try = ["openai", "anthropic", "gemini", "ollama"]
        else:
            # Add fallbacks
            for p in ["openai", "anthropic", "gemini", "ollama"]:
                if p not in providers_to_try:
                    providers_to_try.append(p)

        for provider in providers_to_try:
            if self._try_init(provider):
                return

        self.logger.warning(
            "No LLM provider available. Running in fallback mode (context-only answers). "
            "Set one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, or run Ollama locally."
        )

    def _try_init(self, provider: str) -> bool:
        """Try to initialize a specific provider. Returns True on success."""
        if provider == "openai" and self.openai_api_key and OpenAI is not None:
            try:
                kwargs = {"api_key": self.openai_api_key}
                if self.openai_base_url:
                    kwargs["base_url"] = self.openai_base_url
                self._client = OpenAI(**kwargs)
                self._active_provider = "openai"
                self.logger.info(f"LLM provider: OpenAI ({self.model})")
                return True
            except Exception as exc:
                self.logger.warning(f"Failed to init OpenAI: {exc}")

        if provider == "anthropic" and self.anthropic_api_key and anthropic_lib is not None:
            try:
                self._client = anthropic_lib.Anthropic(api_key=self.anthropic_api_key)
                self._active_provider = "anthropic"
                if not self.model.startswith("claude"):
                    self.model = "claude-sonnet-4-20250514"
                self.logger.info(f"LLM provider: Anthropic ({self.model})")
                return True
            except Exception as exc:
                self.logger.warning(f"Failed to init Anthropic: {exc}")

        if provider == "gemini" and self.gemini_api_key and genai is not None:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self._client = genai.GenerativeModel(
                    self.model if "gemini" in self.model else "gemini-2.0-flash"
                )
                self._active_provider = "gemini"
                if "gemini" not in self.model:
                    self.model = "gemini-2.0-flash"
                self.logger.info(f"LLM provider: Gemini ({self.model})")
                return True
            except Exception as exc:
                self.logger.warning(f"Failed to init Gemini: {exc}")

        if provider == "ollama" and OpenAI is not None:
            try:
                self._client = OpenAI(
                    base_url=f"{self.ollama_base_url}/v1",
                    api_key="ollama",
                )
                # Quick connectivity check
                self._client.models.list()
                self._active_provider = "ollama"
                if self.model in ("gpt-3.5-turbo", "gpt-4"):
                    self.model = "llama3.2"
                self.logger.info(f"LLM provider: Ollama ({self.model})")
                return True
            except Exception:
                pass  # Ollama not running, skip silently

        return False

    def generate_answer(self, question: str, context: str, bloom_level: str = "understand") -> str:
        """Return grounded answer text using the active provider."""
        if self._client is None:
            return self._fallback_answer(question=question, context=context)

        system_prompt = build_system_prompt(bloom_level)
        user_prompt = build_user_prompt(question, context)

        try:
            if self._active_provider == "anthropic":
                return self._anthropic_generate(system_prompt, user_prompt)
            elif self._active_provider == "gemini":
                return self._gemini_generate(system_prompt, user_prompt)
            else:
                # OpenAI and Ollama both use OpenAI-compatible API
                return self._openai_generate(system_prompt, user_prompt)
        except Exception as exc:
            self.logger.warning(f"LLM call failed ({self._active_provider}); using fallback: {exc}")
            return self._fallback_answer(question=question, context=context)

    def _openai_generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate via OpenAI-compatible API (OpenAI, Ollama, etc.)."""
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

    def _anthropic_generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate via Anthropic Claude API."""
        message = self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return (message.content[0].text or "").strip()

    def _gemini_generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate via Google Gemini API."""
        combined = f"{system_prompt}\n\n{user_prompt}"
        response = self._client.generate_content(combined)
        return (response.text or "").strip()

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

    def generate_comparison(
        self, topic_a: str, topic_b: str, context_a: str, context_b: str
    ) -> str:
        """Generate a structured comparison of two topics."""
        if self._client is None:
            return self._fallback_comparison(topic_a, topic_b, context_a, context_b)

        prompt = (
            f"Compare and contrast these two topics based on the provided context.\n\n"
            f"Topic A: {topic_a}\nContext for A:\n{context_a}\n\n"
            f"Topic B: {topic_b}\nContext for B:\n{context_b}\n\n"
            "Provide:\n"
            "1. Key similarities\n"
            "2. Key differences\n"
            "3. When to use each\n"
            "4. Exam tips for distinguishing them\n"
            "Use only the provided context. Be concise and exam-focused."
        )
        system = "You are an exam-focused study assistant. Compare topics using only provided context."

        try:
            if self._active_provider == "anthropic":
                return self._anthropic_generate(system, prompt)
            elif self._active_provider == "gemini":
                return self._gemini_generate(system, prompt)
            else:
                return self._openai_generate(system, prompt)
        except Exception as exc:
            self.logger.warning(f"Comparison LLM call failed: {exc}")
            return self._fallback_comparison(topic_a, topic_b, context_a, context_b)

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

    def _fallback_comparison(
        self, topic_a: str, topic_b: str, context_a: str, context_b: str
    ) -> str:
        """Heuristic comparison when no LLM is available."""
        tokens_a = set(context_a.lower().split()) if context_a else set()
        tokens_b = set(context_b.lower().split()) if context_b else set()
        common = tokens_a & tokens_b - {"the", "a", "an", "is", "are", "and", "or", "of", "to", "in"}
        unique_a = tokens_a - tokens_b - {"the", "a", "an", "is", "are", "and", "or", "of", "to", "in"}
        unique_b = tokens_b - tokens_a - {"the", "a", "an", "is", "are", "and", "or", "of", "to", "in"}

        lines = [
            f"# Comparison: {topic_a} vs {topic_b}",
            "",
            "## Similarities",
            f"Shared terms: {', '.join(list(common)[:10]) or 'None found'}",
            "",
            "## Differences",
            f"Unique to {topic_a}: {', '.join(list(unique_a)[:10]) or 'None found'}",
            f"Unique to {topic_b}: {', '.join(list(unique_b)[:10]) or 'None found'}",
            "",
            f"## Context for {topic_a}",
            (context_a[:300] if context_a else "No context available."),
            "",
            f"## Context for {topic_b}",
            (context_b[:300] if context_b else "No context available."),
        ]
        return "\n".join(lines)
