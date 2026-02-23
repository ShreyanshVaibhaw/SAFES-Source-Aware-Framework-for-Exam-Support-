"""Reusable Streamlit UI components."""

from __future__ import annotations

from typing import Dict, List

import streamlit as st

CSS_STYLES = """
<style>
.card {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 12px;
  margin-bottom: 10px;
  background: #f9fafb;
}
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 0.75rem;
  background: #ecfeff;
  color: #0f766e;
  border: 1px solid #99f6e4;
}
</style>
"""


def init_styles() -> None:
    st.markdown(CSS_STYLES, unsafe_allow_html=True)


def render_section_header(title: str, subtitle: str = "") -> None:
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)


def render_confidence_meter(confidence: float) -> None:
    confidence = max(0.0, min(1.0, float(confidence)))
    st.progress(confidence, text=f"Confidence: {confidence:.0%}")


def render_citations(citations: List[Dict]) -> None:
    if not citations:
        st.info("No citations returned.")
        return
    st.markdown("### Citations")
    for cite in citations:
        page = cite.get("page_number") or "?"
        section = cite.get("section_title") or "General"
        st.markdown(
            f"- [{cite.get('id')}] `{cite.get('document_id')}` | page `{page}` | "
            f"section `{section}` | score `{cite.get('score')}`"
        )


def render_document_card(doc: Dict) -> None:
    st.markdown(
        (
            "<div class='card'>"
            f"<strong>{doc.get('filename')}</strong><br/>"
            f"ID: <code>{doc.get('document_id')}</code><br/>"
            f"Chunks: {doc.get('chunks')} | Status: {doc.get('status')}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )
