"""Citation generation, formatting, and validation helpers."""

from __future__ import annotations

import re
from typing import Dict, List


class CitationManager:
    """Manage citation payloads and rendering formats."""

    def register_citations(self, retrieval_results: List[Dict]) -> List[Dict]:
        """Build normalized citations from retrieval outputs."""
        citations: List[Dict] = []
        for idx, item in enumerate(retrieval_results, start=1):
            meta = item.get("metadata", {})
            citations.append(
                {
                    "id": idx,
                    "document_id": item.get("document_id") or meta.get("document_id"),
                    "chunk_id": item.get("id") or meta.get("chunk_id"),
                    "page_number": meta.get("page_number"),
                    "section_title": meta.get("section_title"),
                    "score": round(float(item.get("score", 0.0)), 4),
                }
            )
        return citations

    def format_inline(self, citations: List[Dict]) -> str:
        """Return compact inline citation text."""
        parts = []
        for cite in citations:
            page = f"p.{cite['page_number']}" if cite.get("page_number") else "p.?"
            section = f", {cite['section_title']}" if cite.get("section_title") else ""
            parts.append(f"[{cite['id']}] {cite['document_id']} ({page}{section})")
        return "; ".join(parts)

    def format_footnote(self, citations: List[Dict]) -> str:
        """Return multi-line footnote citation text."""
        lines = []
        for cite in citations:
            page = f"page {cite['page_number']}" if cite.get("page_number") else "page unknown"
            section = f", section: {cite['section_title']}" if cite.get("section_title") else ""
            lines.append(f"[{cite['id']}] {cite['document_id']} ({page}{section})")
        return "\n".join(lines)

    def citation_markers(self, text: str) -> List[int]:
        """Extract [n] markers referenced in output text."""
        return [int(match) for match in re.findall(r"\[(\d+)\]", text)]

    def verify_citation_references(self, text: str, citations: List[Dict]) -> bool:
        """Check that all referenced citation markers are present."""
        if not citations:
            return False
        valid_ids = {int(c["id"]) for c in citations}
        markers = self.citation_markers(text)
        return bool(markers) and all(marker in valid_ids for marker in markers)

    def enrich_response(self, answer: str, citations: List[Dict], mode: str = "inline") -> str:
        """Append rendered citations to response text."""
        if not citations:
            return answer
        if mode == "footnote":
            return f"{answer}\n\nSources:\n{self.format_footnote(citations)}"
        return f"{answer}\n\nSources: {self.format_inline(citations)}"
