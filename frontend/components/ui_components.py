"""Reusable Streamlit UI components for SAFES."""

from __future__ import annotations

from typing import Dict, List

import streamlit as st

# =============================================================================
# DESIGN TOKENS
# Academic-modern aesthetic: deep indigo + warm violet, soft surfaces,
# generous whitespace, rounded corners, subtle shadows
# =============================================================================

CSS_STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --safes-indigo: #4F46E5;
  --safes-violet: #7C3AED;
  --safes-deep: #1E1B4B;
  --safes-mint: #10B981;
  --safes-amber: #F59E0B;
  --safes-rose: #F43F5E;
  --safes-bg: #FAFAFE;
  --safes-surface: #FFFFFF;
  --safes-border: #E5E7EB;
  --safes-text: #1F2937;
  --safes-muted: #6B7280;
  --safes-shadow: 0 1px 3px rgba(79, 70, 229, 0.05), 0 4px 12px rgba(79, 70, 229, 0.04);
  --safes-shadow-lg: 0 4px 6px rgba(79, 70, 229, 0.08), 0 12px 24px rgba(79, 70, 229, 0.08);
}

/* === Global font override === */
html, body, [class*="css"], .stMarkdown, .stText, button, input, textarea, select,
h1, h2, h3, h4, h5, h6, p, span, div, .stApp * {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

code, pre, .stCode {
  font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
}

/* === Hide Streamlit chrome === */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

/* === Page background === */
.stApp {
  background: linear-gradient(180deg, #FAFAFE 0%, #F3F4F8 100%);
}

/* === HERO HEADER === */
.safes-hero {
  position: relative;
  display: block;
  width: 100%;
  box-sizing: border-box;
  background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #DB2777 100%);
  border-radius: 20px;
  padding: 32px 40px;
  margin-bottom: 24px;
  color: white;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(79, 70, 229, 0.25);
}

/* Ensure Streamlit's markdown wrapper doesn't shrink our hero */
.stMarkdown:has(.safes-hero) {
  width: 100%;
}
.stMarkdown > div:has(.safes-hero) {
  width: 100%;
}

.safes-hero::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 60%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
  pointer-events: none;
}

.safes-hero-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.safes-hero-title {
  font-size: 2.75rem !important;
  font-weight: 800 !important;
  letter-spacing: -0.02em !important;
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1.1 !important;
  text-shadow: 0 2px 8px rgba(0,0,0,0.2);
  color: white !important;
}

.safes-hero-title-row {
  display: flex;
  align-items: center;
  gap: 14px;
  margin: 4px 0 8px 0;
}

.safes-hero-mark {
  width: 52px;
  height: 52px;
  background: rgba(255,255,255,0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  flex-shrink: 0;
}

.safes-hero-subtitle {
  font-size: 1rem;
  font-weight: 500;
  opacity: 0.92;
  margin-top: 6px;
  max-width: 540px;
}

.safes-hero-badge {
  display: inline-block;
  padding: 4px 10px;
  background: rgba(255,255,255,0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.safes-hero-stats {
  display: flex;
  gap: 28px;
  flex-wrap: wrap;
}

.safes-hero-stat {
  text-align: center;
}

.safes-hero-stat-value {
  font-size: 1.6rem;
  font-weight: 800;
  display: block;
  line-height: 1;
}

.safes-hero-stat-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  opacity: 0.8;
  margin-top: 4px;
}

/* === SECTION HEADERS === */
.safes-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 8px 0 16px 0;
}

.safes-section-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%);
  border: 1px solid #DDD6FE;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.safes-section-text h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--safes-deep);
  letter-spacing: -0.01em;
}

.safes-section-text p {
  margin: 2px 0 0 0;
  font-size: 0.85rem;
  color: var(--safes-muted);
}

/* === CARDS === */
.safes-card {
  background: var(--safes-surface);
  border: 1px solid var(--safes-border);
  border-radius: 14px;
  padding: 18px 20px;
  margin-bottom: 12px;
  box-shadow: var(--safes-shadow);
  transition: all 0.2s ease;
}

.safes-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--safes-shadow-lg);
  border-color: #C7D2FE;
}

.safes-card-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--safes-deep);
  margin: 0 0 6px 0;
}

.safes-card-meta {
  font-size: 0.8rem;
  color: var(--safes-muted);
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* === ANSWER CARD === */
.safes-answer {
  background: linear-gradient(135deg, #FFFFFF 0%, #FAFBFF 100%);
  border: 1px solid #E0E7FF;
  border-left: 4px solid var(--safes-indigo);
  border-radius: 14px;
  padding: 24px 28px;
  margin: 16px 0;
  box-shadow: var(--safes-shadow-lg);
  font-size: 1rem;
  line-height: 1.7;
  color: var(--safes-text);
}

.safes-answer-label {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--safes-indigo);
  margin-bottom: 12px;
}

/* === BADGES === */
.safes-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  border: 1px solid;
}

.safes-badge-indigo {
  background: #EEF2FF;
  color: #4338CA;
  border-color: #C7D2FE;
}

.safes-badge-mint {
  background: #ECFDF5;
  color: #047857;
  border-color: #A7F3D0;
}

.safes-badge-amber {
  background: #FFFBEB;
  color: #B45309;
  border-color: #FCD34D;
}

.safes-badge-rose {
  background: #FFF1F2;
  color: #BE123C;
  border-color: #FECDD3;
}

.safes-badge-violet {
  background: #F5F3FF;
  color: #6D28D9;
  border-color: #DDD6FE;
}

/* === CONFIDENCE METER === */
.safes-confidence {
  background: var(--safes-surface);
  border: 1px solid var(--safes-border);
  border-radius: 12px;
  padding: 14px 18px;
  margin: 12px 0;
}

.safes-confidence-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.safes-confidence-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--safes-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.safes-confidence-value {
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: -0.01em;
}

.safes-confidence-bar {
  height: 8px;
  background: #F3F4F6;
  border-radius: 999px;
  overflow: hidden;
  position: relative;
}

.safes-confidence-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* === CITATIONS === */
.safes-citation {
  background: #FAFBFF;
  border: 1px solid #E0E7FF;
  border-radius: 10px;
  padding: 12px 16px;
  margin: 8px 0;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  transition: all 0.2s ease;
}

.safes-citation:hover {
  border-color: var(--safes-indigo);
  background: #F5F7FF;
}

.safes-citation-id {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, var(--safes-indigo), var(--safes-violet));
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
}

.safes-citation-body {
  flex: 1;
  min-width: 0;
}

.safes-citation-doc {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--safes-deep);
  word-break: break-all;
}

.safes-citation-meta {
  font-size: 0.75rem;
  color: var(--safes-muted);
  margin-top: 2px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* === STREAMLIT WIDGET OVERRIDES === */

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  gap: 6px;
  background: var(--safes-surface);
  padding: 6px;
  border-radius: 14px;
  border: 1px solid var(--safes-border);
  box-shadow: var(--safes-shadow);
}

.stTabs [data-baseweb="tab"] {
  border-radius: 10px !important;
  padding: 10px 18px !important;
  font-weight: 600 !important;
  color: var(--safes-muted) !important;
  background: transparent !important;
  transition: all 0.2s ease;
  border: none !important;
}

.stTabs [data-baseweb="tab"]:hover {
  background: #F5F7FF !important;
  color: var(--safes-indigo) !important;
}

.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--safes-indigo), var(--safes-violet)) !important;
  color: white !important;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

/* Buttons */
.stButton > button {
  border-radius: 10px !important;
  font-weight: 600 !important;
  padding: 10px 22px !important;
  transition: all 0.2s ease !important;
  border: 1px solid var(--safes-border) !important;
  background: var(--safes-surface) !important;
  color: var(--safes-deep) !important;
}

.stButton > button:hover {
  transform: translateY(-1px);
  box-shadow: var(--safes-shadow-lg) !important;
  border-color: var(--safes-indigo) !important;
  color: var(--safes-indigo) !important;
}

.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, var(--safes-indigo), var(--safes-violet)) !important;
  color: white !important;
  border: none !important;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
}

.stButton > button[kind="primary"]:hover {
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
  transform: translateY(-2px);
}

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
  border-radius: 10px !important;
  border: 1px solid var(--safes-border) !important;
  font-family: 'Inter', sans-serif !important;
  transition: all 0.2s ease;
}

.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--safes-indigo) !important;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #FFFFFF 0%, #FAFBFF 100%);
  border-right: 1px solid var(--safes-border);
}

section[data-testid="stSidebar"] h2 {
  color: var(--safes-deep);
  font-weight: 700;
  letter-spacing: -0.01em;
}

/* File uploader */
[data-testid="stFileUploaderDropzone"] {
  background: linear-gradient(135deg, #FAFBFF 0%, #F5F3FF 100%) !important;
  border: 2px dashed #C7D2FE !important;
  border-radius: 12px !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
  border-color: var(--safes-indigo) !important;
  background: linear-gradient(135deg, #EEF2FF 0%, #EDE9FE 100%) !important;
}

/* Metrics */
[data-testid="stMetric"] {
  background: var(--safes-surface);
  border: 1px solid var(--safes-border);
  border-radius: 14px;
  padding: 16px 20px;
  box-shadow: var(--safes-shadow);
  transition: all 0.2s ease;
}

[data-testid="stMetric"]:hover {
  transform: translateY(-2px);
  box-shadow: var(--safes-shadow-lg);
  border-color: #C7D2FE;
}

[data-testid="stMetricValue"] {
  font-size: 2rem !important;
  font-weight: 800 !important;
  background: linear-gradient(135deg, var(--safes-indigo), var(--safes-violet));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

[data-testid="stMetricLabel"] {
  font-weight: 600 !important;
  color: var(--safes-muted) !important;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.75rem !important;
}

/* Expanders */
.streamlit-expanderHeader {
  background: var(--safes-surface) !important;
  border: 1px solid var(--safes-border) !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  transition: all 0.2s ease;
}

.streamlit-expanderHeader:hover {
  border-color: var(--safes-indigo) !important;
  background: #FAFBFF !important;
}

/* Sliders */
.stSlider [data-baseweb="slider"] [role="slider"] {
  background: var(--safes-indigo) !important;
  border-color: var(--safes-indigo) !important;
}

/* Alerts */
.stAlert {
  border-radius: 12px !important;
  border-width: 1px !important;
}

/* Progress bar (default Streamlit one) */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--safes-indigo), var(--safes-violet)) !important;
}

/* Animations */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.safes-card, .safes-answer, .safes-citation {
  animation: fadeInUp 0.4s ease-out;
}

/* Footer */
.safes-footer {
  text-align: center;
  padding: 24px 0;
  color: var(--safes-muted);
  font-size: 0.8rem;
  border-top: 1px solid var(--safes-border);
  margin-top: 40px;
}

.safes-footer-highlight {
  color: var(--safes-indigo);
  font-weight: 600;
}
</style>
"""


def init_styles() -> None:
    """Inject global CSS styles."""
    st.markdown(CSS_STYLES, unsafe_allow_html=True)


def render_hero(doc_count: int = 0, query_count: int = 0, llm_model: str = "GLM-5") -> None:
    """Render the main hero header with project name and live stats."""
    st.markdown(
        f"""
        <div class="safes-hero">
          <div class="safes-hero-content">
            <div>
              <span class="safes-hero-badge">Source-Aware Framework for Exam Support</span>
              <div class="safes-hero-title-row">
                <div class="safes-hero-mark">📚</div>
                <div class="safes-hero-title">SAFES</div>
              </div>
              <p class="safes-hero-subtitle">
                Exam-focused AI study assistant grounded in your own materials.
                Citations, hallucination control, and Bloom-level adaptive answers.
              </p>
            </div>
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
                <div class="safes-hero-stat-label">LLM</div>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str = "", icon: str = "") -> None:
    """Render a section header with optional icon and subtitle."""
    icon_html = f'<div class="safes-section-icon">{icon}</div>' if icon else ""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="safes-section">
          {icon_html}
          <div class="safes-section-text">
            <h3>{title}</h3>
            {subtitle_html}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_answer(answer_text: str) -> None:
    """Render the LLM answer in a styled card."""
    # Escape any HTML in the answer text but preserve newlines
    safe_text = answer_text.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
    st.markdown(
        f"""
        <div class="safes-answer">
          <div class="safes-answer-label">Grounded Answer</div>
          <div>{safe_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_confidence_meter(confidence: float, bloom_level: str = "") -> None:
    """Render a beautiful confidence meter with color coding."""
    confidence = max(0.0, min(1.0, float(confidence)))
    pct = confidence * 100

    if confidence >= 0.75:
        color = "#10B981"  # mint
        label = "High Confidence"
    elif confidence >= 0.5:
        color = "#F59E0B"  # amber
        label = "Moderate Confidence"
    else:
        color = "#F43F5E"  # rose
        label = "Low Confidence"

    bloom_badge = (
        f'<span class="safes-badge safes-badge-violet">Bloom: {bloom_level.title()}</span>'
        if bloom_level
        else ""
    )

    st.markdown(
        f"""
        <div class="safes-confidence">
          <div class="safes-confidence-header">
            <div>
              <span class="safes-confidence-label">{label}</span>
              {bloom_badge}
            </div>
            <span class="safes-confidence-value" style="color: {color};">{pct:.0f}%</span>
          </div>
          <div class="safes-confidence-bar">
            <div class="safes-confidence-fill" style="width: {pct}%; background: linear-gradient(90deg, {color}, {color}aa);"></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_citations(citations: List[Dict]) -> None:
    """Render citations as styled cards."""
    if not citations:
        st.markdown(
            '<div class="safes-card" style="color: #6B7280; text-align: center;">'
            "No citations returned for this answer.</div>",
            unsafe_allow_html=True,
        )
        return

    render_section_header("Sources", f"{len(citations)} citation(s) backing this answer", icon="📚")

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
                  <span>📄 Page {page}</span>
                  <span>📑 {section}</span>
                  <span>⚡ Score {score}</span>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_document_card(doc: Dict) -> None:
    """Render a document card with hover effect."""
    status = doc.get("status", "unknown")
    status_class = "safes-badge-mint" if status == "completed" else "safes-badge-amber"
    st.markdown(
        f"""
        <div class="safes-card">
          <div class="safes-card-title">📄 {doc.get('filename', 'Untitled')}</div>
          <div class="safes-card-meta">
            <span><strong>{doc.get('chunks', 0)}</strong> chunks</span>
            <span class="safes-badge {status_class}">{status}</span>
          </div>
          <div class="safes-card-meta" style="margin-top: 6px;">
            <code style="font-size: 0.7rem;">{doc.get('document_id', '')}</code>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_practice_questions(questions: List[str]) -> None:
    """Render generated practice questions in styled cards."""
    if not questions:
        return
    render_section_header(
        "Practice Questions",
        "Try these to reinforce your learning",
        icon="🎯",
    )
    for i, q in enumerate(questions, 1):
        st.markdown(
            f"""
            <div class="safes-card" style="border-left: 3px solid var(--safes-violet);">
              <div style="display: flex; gap: 12px; align-items: flex-start;">
                <div class="safes-citation-id" style="background: linear-gradient(135deg, #7C3AED, #DB2777);">{i}</div>
                <div style="flex: 1; padding-top: 4px;">{q}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_grounding_alert(grounding: Dict) -> None:
    """Render hallucination grounding info as an alert."""
    method = grounding.get("verification_method", "heuristic")
    is_grounded = grounding.get("is_grounded", True)
    overlap = grounding.get("keyword_overlap", 0.0)
    unsupported = grounding.get("unsupported_claims", [])

    if is_grounded:
        bg, border, icon, title = "#ECFDF5", "#10B981", "✅", "Answer Grounded"
    else:
        bg, border, icon, title = "#FFFBEB", "#F59E0B", "⚠️", "Low Grounding"

    st.markdown(
        f"""
        <div style="background: {bg}; border-left: 4px solid {border}; border-radius: 10px;
                    padding: 14px 18px; margin: 12px 0;">
          <div style="font-weight: 700; color: {border}; margin-bottom: 4px;">{icon} {title}</div>
          <div style="font-size: 0.85rem; color: #4B5563;">
            Verification: <strong>{method}</strong> · Keyword overlap: <strong>{overlap:.0%}</strong>
            {f" · {len(unsupported)} unsupported claim(s)" if unsupported else ""}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render the page footer."""
    st.markdown(
        """
        <div class="safes-footer">
          <span class="safes-footer-highlight">SAFES</span> · Source-Aware Framework for Exam Support ·
          Built with FastAPI, Streamlit & RAG
        </div>
        """,
        unsafe_allow_html=True,
    )
