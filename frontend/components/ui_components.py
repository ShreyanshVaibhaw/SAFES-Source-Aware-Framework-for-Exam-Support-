"""Reusable Streamlit UI components — Ollama-inspired radical minimalism."""

from __future__ import annotations

from typing import Dict, List

import streamlit as st

# =============================================================================
# DESIGN SYSTEM — Ollama-inspired
# Pure grayscale, zero shadows, zero gradients, pill-shaped interactives,
# SF Pro Rounded display, binary radius (12px containers / 9999px interactive)
# =============================================================================

CSS_STYLES = """
<style>
/* === Typography === */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap');

:root {
  --black: #000000;
  --near-black: #262626;
  --dark-text: #404040;
  --mid-gray: #525252;
  --stone: #737373;
  --silver: #a3a3a3;
  --border: #e5e5e5;
  --snow: #fafafa;
  --white: #ffffff;
  --darkest: #090909;
}

/* === Global font === */
html, body, [class*="css"], .stMarkdown, .stText, button, input, textarea, select,
h1, h2, h3, h4, h5, h6, p, span, div, label, .stApp * {
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif !important;
  -webkit-font-smoothing: antialiased;
}

code, pre, .stCode, [class*="language-"] {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
}

/* === Hide Streamlit chrome === */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

/* Hide sidebar collapse button text leak */
[data-testid="stSidebarCollapseButton"] span,
[data-testid="stSidebarCollapsedControl"] span {
  font-size: 0 !important;
  visibility: hidden !important;
}
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarCollapsedControl"] svg {
  visibility: visible !important;
}

/* === Page background === */
.stApp {
  background: var(--white) !important;
  color: var(--black);
}

[data-testid="stAppViewContainer"] {
  background: transparent;
}

.stMarkdown, .stText, p, span, label, div {
  color: var(--near-black);
}

/* === HERO === */
.safes-hero {
  display: block;
  width: 100%;
  box-sizing: border-box;
  text-align: center;
  padding: 48px 40px 40px 40px;
  margin-bottom: 32px;
  border-bottom: 1px solid var(--border);
}

.stMarkdown:has(.safes-hero), .stMarkdown > div:has(.safes-hero) {
  width: 100%;
}

.safes-hero-title {
  font-family: 'SF Pro Rounded', ui-rounded, 'SF Pro Display', system-ui, sans-serif !important;
  font-size: 48px !important;
  font-weight: 500 !important;
  color: var(--black) !important;
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1.0 !important;
  letter-spacing: -0.02em;
}

.safes-hero-subtitle {
  font-size: 18px;
  font-weight: 400;
  color: var(--stone);
  margin-top: 12px;
  line-height: 1.56;
}

.safes-hero-stats {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 28px;
}

.safes-hero-stat {
  text-align: center;
}

.safes-hero-stat-value {
  font-family: 'SF Pro Rounded', ui-rounded, system-ui, sans-serif !important;
  font-size: 30px;
  font-weight: 500;
  color: var(--black);
  display: block;
  line-height: 1;
}

.safes-hero-stat-label {
  font-size: 12px;
  font-weight: 400;
  color: var(--silver);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 6px;
}

/* === SECTION HEADERS === */
.safes-section {
  margin: 12px 0 20px 0;
}

.safes-section h3 {
  font-family: 'SF Pro Rounded', ui-rounded, system-ui, sans-serif !important;
  font-size: 24px !important;
  font-weight: 500 !important;
  color: var(--black) !important;
  margin: 0 0 4px 0 !important;
  letter-spacing: -0.01em;
}

.safes-section p {
  font-size: 14px;
  color: var(--stone);
  margin: 0;
}

/* === CARDS === */
.safes-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 12px;
  color: var(--near-black);
}

.safes-card-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--black);
  margin: 0 0 6px 0;
}

.safes-card-meta {
  font-size: 14px;
  color: var(--stone);
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* === ANSWER === */
.safes-answer {
  background: var(--white);
  border: 1px solid var(--border);
  border-left: 3px solid var(--black);
  border-radius: 12px;
  padding: 24px 28px;
  margin: 16px 0;
  font-size: 16px;
  line-height: 1.6;
  color: var(--near-black);
}

.safes-answer-label {
  display: inline-block;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--stone);
  margin-bottom: 12px;
}

/* === BADGES (pill-shaped) === */
.safes-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 500;
  background: var(--snow);
  color: var(--mid-gray);
  border: 1px solid var(--border);
}

/* === CONFIDENCE === */
.safes-confidence {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 20px;
  margin: 12px 0;
}

.safes-confidence-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.safes-confidence-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--stone);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.safes-confidence-value {
  font-family: 'SF Pro Rounded', ui-rounded, system-ui, sans-serif !important;
  font-size: 24px;
  font-weight: 500;
  color: var(--black);
}

.safes-confidence-bar {
  height: 6px;
  background: var(--snow);
  border-radius: 9999px;
  overflow: hidden;
}

.safes-confidence-fill {
  height: 100%;
  border-radius: 9999px;
  background: var(--near-black);
}

/* === CITATIONS === */
.safes-citation {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 18px;
  margin: 8px 0;
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.safes-citation-id {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  background: var(--black);
  color: var(--white);
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  font-size: 13px;
}

.safes-citation-body {
  flex: 1;
  min-width: 0;
}

.safes-citation-doc {
  font-weight: 500;
  font-size: 14px;
  color: var(--black);
  word-break: break-all;
}

.safes-citation-meta {
  font-size: 12px;
  color: var(--stone);
  margin-top: 4px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* === STREAMLIT TABS (pill-shaped) === */
.stTabs [data-baseweb="tab-list"] {
  gap: 4px;
  background: transparent;
  padding: 4px;
  border: none;
}

.stTabs [data-baseweb="tab"] {
  border-radius: 9999px !important;
  padding: 8px 20px !important;
  font-weight: 400 !important;
  font-size: 14px !important;
  color: var(--stone) !important;
  background: transparent !important;
  border: none !important;
}

.stTabs [data-baseweb="tab"]:hover {
  background: var(--snow) !important;
  color: var(--black) !important;
}

.stTabs [aria-selected="true"] {
  background: var(--border) !important;
  color: var(--near-black) !important;
}

/* === BUTTONS (pill-shaped) === */
.stButton > button {
  border-radius: 9999px !important;
  font-weight: 500 !important;
  font-size: 14px !important;
  padding: 10px 24px !important;
  border: 1px solid var(--border) !important;
  background: var(--border) !important;
  color: var(--near-black) !important;
  box-shadow: none !important;
}

.stButton > button:hover {
  background: #d4d4d4 !important;
  border-color: #d4d4d4 !important;
  transform: none !important;
  box-shadow: none !important;
}

/* CTA / Primary */
.stButton > button[kind="primary"] {
  background: var(--black) !important;
  color: var(--white) !important;
  border: 1px solid var(--black) !important;
}

.stButton > button[kind="primary"]:hover {
  background: var(--near-black) !important;
  border-color: var(--near-black) !important;
  color: var(--white) !important;
  box-shadow: none !important;
}

/* === INPUTS (pill-shaped) === */
.stTextInput input, .stTextArea textarea, .stNumberInput input,
[data-baseweb="input"] input {
  border-radius: 9999px !important;
  border: 1px solid var(--border) !important;
  background: var(--white) !important;
  color: var(--black) !important;
  padding: 10px 20px !important;
  box-shadow: none !important;
}

.stTextArea textarea {
  border-radius: 12px !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--black) !important;
  box-shadow: none !important;
}

.stTextInput input::placeholder, .stTextArea textarea::placeholder {
  color: var(--silver) !important;
}

/* Labels */
.stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label,
.stFileUploader label, .stRadio label, .stCheckbox label {
  color: var(--black) !important;
  font-weight: 500 !important;
  font-size: 14px !important;
}

/* Selectbox */
.stSelectbox > div > div {
  border-radius: 9999px !important;
  border: 1px solid var(--border) !important;
  background: var(--white) !important;
  box-shadow: none !important;
}

[data-baseweb="popover"] {
  background: var(--white) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  box-shadow: none !important;
}

[data-baseweb="popover"] li {
  background: var(--white) !important;
  color: var(--black) !important;
}

[data-baseweb="popover"] li:hover {
  background: var(--snow) !important;
}

/* === SIDEBAR === */
section[data-testid="stSidebar"] {
  background: var(--white) !important;
  border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] * {
  color: var(--near-black);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
  color: var(--black);
  font-weight: 500;
}

/* === FILE UPLOADER === */
[data-testid="stFileUploaderDropzone"] {
  background: var(--snow) !important;
  border: 1px dashed var(--border) !important;
  border-radius: 12px !important;
  padding: 18px 16px !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  gap: 10px !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
  border-color: var(--stone) !important;
}

[data-testid="stFileUploaderDropzone"] span {
  color: var(--near-black) !important;
}

[data-testid="stFileUploaderDropzone"] small {
  color: var(--silver) !important;
}

[data-testid="stFileUploaderDropzone"] svg {
  color: var(--stone) !important;
}

/* Browse button inside uploader */
[data-testid="stFileUploaderDropzone"] button {
  font-size: 0 !important;
  line-height: 0 !important;
  text-indent: -9999px !important;
  background: var(--border) !important;
  background-image: none !important;
  border: none !important;
  border-radius: 9999px !important;
  padding: 8px 18px !important;
  min-width: 120px !important;
  height: 36px !important;
  cursor: pointer !important;
  box-shadow: none !important;
  position: relative !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}

[data-testid="stFileUploaderDropzone"] button > * {
  font-size: 0 !important;
  visibility: hidden !important;
  width: 0 !important;
  height: 0 !important;
  position: absolute !important;
  left: -9999px !important;
}

[data-testid="stFileUploaderDropzone"] button::before {
  content: 'Browse';
  font-size: 14px !important;
  font-weight: 500 !important;
  color: var(--near-black) !important;
  text-indent: 0 !important;
  visibility: visible !important;
  position: static !important;
  display: inline-block !important;
  width: auto !important;
  height: auto !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
  background: #d4d4d4 !important;
}

/* Delete button */
[data-testid="stFileUploaderDeleteBtn"] button {
  background: transparent !important;
  color: var(--stone) !important;
}

[data-testid="stFileUploaderDeleteBtn"] button::before {
  content: '' !important;
}

/* === METRICS === */
[data-testid="stMetric"] {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 20px;
}

[data-testid="stMetricValue"] {
  font-family: 'SF Pro Rounded', ui-rounded, system-ui, sans-serif !important;
  font-size: 30px !important;
  font-weight: 500 !important;
  color: var(--black) !important;
  -webkit-text-fill-color: var(--black) !important;
  background: none !important;
  background-clip: unset !important;
  -webkit-background-clip: unset !important;
}

[data-testid="stMetricLabel"] {
  font-weight: 500 !important;
  color: var(--stone) !important;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 12px !important;
}

/* === EXPANDERS === */
.streamlit-expanderHeader,
[data-testid="stExpander"] summary {
  background: var(--white) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  font-weight: 500 !important;
  color: var(--black) !important;
  box-shadow: none !important;
}

.streamlit-expanderHeader:hover,
[data-testid="stExpander"] summary:hover {
  background: var(--snow) !important;
}

/* === SLIDERS === */
.stSlider [data-baseweb="slider"] [role="slider"] {
  background: var(--black) !important;
  border-color: var(--black) !important;
}

.stSlider [data-baseweb="slider"] > div > div {
  background: var(--black) !important;
}

/* === PROGRESS BAR === */
.stProgress > div > div > div > div {
  background: var(--near-black) !important;
}

/* === ALERTS === */
.stAlert {
  border-radius: 12px !important;
  box-shadow: none !important;
}

/* === FOOTER === */
.safes-footer {
  text-align: center;
  padding: 32px 0;
  color: var(--silver);
  font-size: 14px;
  border-top: 1px solid var(--border);
  margin-top: 48px;
}

.safes-footer strong {
  color: var(--black);
  font-weight: 500;
}

/* === GROUNDING ALERT === */
.safes-grounding {
  background: var(--snow);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 20px;
  margin: 12px 0;
}
</style>
"""


def init_styles() -> None:
    """Inject Ollama-inspired CSS styles."""
    st.markdown(CSS_STYLES, unsafe_allow_html=True)


def render_hero(doc_count: int = 0, query_count: int = 0, llm_model: str = "GLM-5") -> None:
    """Render minimal hero header."""
    st.markdown(
        f"""
        <div class="safes-hero">
          <div class="safes-hero-title">SAFES</div>
          <p class="safes-hero-subtitle">
            Source-Aware Framework for Exam Support.<br>
            Grounded answers from your own study materials.
          </p>
          <div class="safes-hero-stats">
            <div class="safes-hero-stat">
              <span class="safes-hero-stat-value">{doc_count}</span>
              <div class="safes-hero-stat-label">Documents</div>
            </div>
            <div class="safes-hero-stat">
              <span class="safes-hero-stat-value">{query_count}</span>
              <div class="safes-hero-stat-label">Queries</div>
            </div>
            <div class="safes-hero-stat">
              <span class="safes-hero-stat-value">{llm_model}</span>
              <div class="safes-hero-stat-label">Model</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str = "", icon: str = "") -> None:
    """Render a minimal section header."""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="safes-section">
          <h3>{title}</h3>
          {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_answer(answer_text: str) -> None:
    """Render the LLM answer."""
    safe_text = answer_text.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
    st.markdown(
        f"""
        <div class="safes-answer">
          <div class="safes-answer-label">Answer</div>
          <div>{safe_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_confidence_meter(confidence: float, bloom_level: str = "") -> None:
    """Render a grayscale confidence meter."""
    confidence = max(0.0, min(1.0, float(confidence)))
    pct = confidence * 100

    if confidence >= 0.75:
        label = "High"
    elif confidence >= 0.5:
        label = "Moderate"
    else:
        label = "Low"

    bloom_html = (
        f'<span class="safes-badge">{bloom_level.title()}</span>'
        if bloom_level else ""
    )

    st.markdown(
        f"""
        <div class="safes-confidence">
          <div class="safes-confidence-header">
            <div>
              <span class="safes-confidence-label">{label} confidence</span>
              {bloom_html}
            </div>
            <span class="safes-confidence-value">{pct:.0f}%</span>
          </div>
          <div class="safes-confidence-bar">
            <div class="safes-confidence-fill" style="width: {pct}%;"></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_citations(citations: List[Dict]) -> None:
    """Render citations as minimal cards."""
    if not citations:
        st.markdown(
            '<div class="safes-card" style="text-align: center; color: var(--stone);">'
            "No citations returned.</div>",
            unsafe_allow_html=True,
        )
        return

    render_section_header("Sources", f"{len(citations)} citation(s)")

    for cite in citations:
        cid = cite.get("id", "?")
        doc = cite.get("document_id", "unknown")
        page = cite.get("page_number") or "?"
        section = cite.get("section_title") or "General"
        score = cite.get("score", 0.0)
        st.markdown(
            f"""
            <div class="safes-citation">
              <div class="safes-citation-id">{cid}</div>
              <div class="safes-citation-body">
                <div class="safes-citation-doc">{doc}</div>
                <div class="safes-citation-meta">
                  <span>Page {page}</span>
                  <span>{section}</span>
                  <span>Score {score}</span>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_document_card(doc: Dict) -> None:
    """Render a document card."""
    status = doc.get("status", "unknown")
    st.markdown(
        f"""
        <div class="safes-card">
          <div class="safes-card-title">{doc.get('filename', 'Untitled')}</div>
          <div class="safes-card-meta">
            <span>{doc.get('chunks', 0)} chunks</span>
            <span class="safes-badge">{status}</span>
          </div>
          <div style="font-size: 12px; color: var(--silver); margin-top: 6px;">
            <code>{doc.get('document_id', '')}</code>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_practice_questions(questions: List[str]) -> None:
    """Render practice questions."""
    if not questions:
        return
    render_section_header("Practice Questions")
    for i, q in enumerate(questions, 1):
        st.markdown(
            f"""
            <div class="safes-card" style="border-left: 2px solid var(--black);">
              <div style="display: flex; gap: 14px; align-items: flex-start;">
                <div class="safes-citation-id">{i}</div>
                <div style="flex: 1; padding-top: 4px; font-size: 14px;">{q}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_grounding_alert(grounding: Dict) -> None:
    """Render hallucination grounding info."""
    method = grounding.get("verification_method", "heuristic")
    is_grounded = grounding.get("is_grounded", True)
    overlap = grounding.get("keyword_overlap", 0.0)
    unsupported = grounding.get("unsupported_claims", [])

    status = "Grounded" if is_grounded else "Low grounding"
    icon = "+" if is_grounded else "!"

    st.markdown(
        f"""
        <div class="safes-grounding">
          <div style="font-weight: 500; color: var(--black); margin-bottom: 4px;">
            [{icon}] {status}
          </div>
          <div style="font-size: 14px; color: var(--stone);">
            Verification: {method} &middot; Keyword overlap: {overlap:.0%}
            {f" &middot; {len(unsupported)} unsupported claim(s)" if unsupported else ""}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render minimal footer."""
    st.markdown(
        """
        <div class="safes-footer">
          <strong>SAFES</strong> &middot; Source-Aware Framework for Exam Support
        </div>
        """,
        unsafe_allow_html=True,
    )
