"""Bloom's taxonomy detection and response guidance."""

from __future__ import annotations

from enum import Enum
from typing import Dict, List


class BloomsLevel(str, Enum):
    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"


class BloomsTaxonomyService:
    """Detect cognitive level and generate level-aware helper content."""

    KEYWORDS: Dict[BloomsLevel, List[str]] = {
        BloomsLevel.REMEMBER: ["define", "list", "name", "what is", "state"],
        BloomsLevel.UNDERSTAND: ["explain", "summarize", "describe", "why"],
        BloomsLevel.APPLY: ["apply", "solve", "use", "demonstrate", "implement"],
        BloomsLevel.ANALYZE: ["compare", "analyze", "differentiate", "contrast", "examine"],
        BloomsLevel.EVALUATE: ["evaluate", "justify", "critique", "assess", "argue"],
        BloomsLevel.CREATE: ["create", "design", "compose", "propose", "develop"],
    }

    GUIDELINES: Dict[BloomsLevel, str] = {
        BloomsLevel.REMEMBER: "Provide concise factual recall points.",
        BloomsLevel.UNDERSTAND: "Explain concepts in clear language with short examples.",
        BloomsLevel.APPLY: "Show practical steps and worked usage.",
        BloomsLevel.ANALYZE: "Break down components and compare relationships.",
        BloomsLevel.EVALUATE: "Present criteria, trade-offs, and a justified judgement.",
        BloomsLevel.CREATE: "Synthesize ideas into a structured original output.",
    }

    def detect_level(self, query: str) -> BloomsLevel:
        """Infer Bloom level using keyword heuristic."""
        query_l = query.lower()
        scores = {level: 0 for level in BloomsLevel}
        for level, words in self.KEYWORDS.items():
            scores[level] = sum(1 for word in words if word in query_l)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else BloomsLevel.UNDERSTAND

    def get_response_guideline(self, level: BloomsLevel | str) -> str:
        """Return prompt guideline for one Bloom level."""
        normalized = self._normalize(level)
        return self.GUIDELINES[normalized]

    def generate_practice_questions(self, topic: str, level: BloomsLevel | str) -> List[str]:
        """Generate simple level-specific practice question stems."""
        normalized = self._normalize(level)
        templates = {
            BloomsLevel.REMEMBER: [f"Define {topic}.", f"List key facts about {topic}."],
            BloomsLevel.UNDERSTAND: [
                f"Explain {topic} in your own words.",
                f"Why is {topic} important?",
            ],
            BloomsLevel.APPLY: [f"Apply {topic} to a real exam-style scenario."],
            BloomsLevel.ANALYZE: [f"Compare two approaches related to {topic}."],
            BloomsLevel.EVALUATE: [f"Evaluate the strengths and limits of {topic}."],
            BloomsLevel.CREATE: [f"Design a new solution using {topic} principles."],
        }
        return templates[normalized]

    def list_levels(self) -> List[str]:
        return [level.value for level in BloomsLevel]

    def _normalize(self, level: BloomsLevel | str) -> BloomsLevel:
        if isinstance(level, BloomsLevel):
            return level
        return BloomsLevel(level.lower())
