"""Reusable Streamlit UI components — Ollama-inspired minimalism with themes."""

from __future__ import annotations

from typing import Dict, List

import streamlit as st

# =============================================================================
# THEMES — Minimalist palettes, same design language (pills, no shadows, clean)
# =============================================================================

THEMES: Dict[str, Dict[str, str]] = {
    "Minimal": {
        "bg": "#ffffff", "surface": "#fafafa", "text": "#000000", "text2": "#262626",
        "muted": "#737373", "faint": "#a3a3a3", "border": "#e5e5e5", "hover": "#d4d4d4",
        "active": "#e5e5e5", "accent": "#000000", "sidebar_bg": "#ffffff",
    },
    "Cappuccino": {
        "bg": "#FAF6F1", "surface": "#F5EDE4", "text": "#3E2C1C", "text2": "#5C4033",
        "muted": "#8B7355", "faint": "#B8A088", "border": "#E0D0BE", "hover": "#D4C4AE",
        "active": "#D4C4AE", "accent": "#6F4E37", "sidebar_bg": "#F5EDE4",
    },
    "Dark": {
        "bg": "#0F172A", "surface": "#1E293B", "text": "#F1F5F9", "text2": "#E2E8F0",
        "muted": "#94A3B8", "faint": "#64748B", "border": "#334155", "hover": "#2D3F55",
        "active": "#334155", "accent": "#E2E8F0", "sidebar_bg": "#0F172A",
    },
    "Midnight": {
        "bg": "#000000", "surface": "#0A0A0F", "text": "#FAFAFA", "text2": "#E4E4E7",
        "muted": "#A1A1AA", "faint": "#71717A", "border": "#27272A", "hover": "#1C1C20",
        "active": "#27272A", "accent": "#FAFAFA", "sidebar_bg": "#000000",
    },
    "Sage": {
        "bg": "#F7FAF8", "surface": "#EDF2EE", "text": "#1A2E1A", "text2": "#2D4A2D",
        "muted": "#5F7A5F", "faint": "#8FAA8F", "border": "#C8D8C8", "hover": "#B8CCB8",
        "active": "#C8D8C8", "accent": "#2D4A2D", "sidebar_bg": "#EDF2EE",
    },
    "Ocean": {
        "bg": "#F0F9FF", "surface": "#E8F4FD", "text": "#082F49", "text2": "#0C4A6E",
        "muted": "#0369A1", "faint": "#7DD3FC", "border": "#BAE6FD", "hover": "#A5D8F5",
        "active": "#BAE6FD", "accent": "#0C4A6E", "sidebar_bg": "#E8F4FD",
    },
    "Rose": {
        "bg": "#FFF5F5", "surface": "#FEE2E2", "text": "#450A0A", "text2": "#7F1D1D",
        "muted": "#B91C1C", "faint": "#FCA5A5", "border": "#FECACA", "hover": "#FDB5B5",
        "active": "#FECACA", "accent": "#7F1D1D", "sidebar_bg": "#FEE2E2",
    },
    "Lavender": {
        "bg": "#FAF5FF", "surface": "#F3E8FF", "text": "#2E1065", "text2": "#581C87",
        "muted": "#7C3AED", "faint": "#C4B5FD", "border": "#DDD6FE", "hover": "#D0C5F5",
        "active": "#DDD6FE", "accent": "#581C87", "sidebar_bg": "#F3E8FF",
    },
}


def _css(t: Dict[str, str]) -> str:
    """Build CSS from theme palette."""
    return f"""
<style>
:root {{
  --bg: {t['bg']}; --surface: {t['surface']}; --text: {t['text']}; --text2: {t['text2']};
  --muted: {t['muted']}; --faint: {t['faint']}; --border: {t['border']}; --hover: {t['hover']};
  --active: {t['active']}; --accent: {t['accent']}; --sidebar-bg: {t['sidebar_bg']};
}}

/* === Font === */
html, body, [class*="css"], .stMarkdown, .stText, button, input, textarea, select,
h1, h2, h3, h4, h5, h6, p, span, div, label, .stApp * {{
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif !important;
}}
code, pre, .stCode {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace !important; }}

/* === Chrome === */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header[data-testid="stHeader"] {{background: var(--bg) !important;}}

/* === Sidebar collapse button — VISIBLE === */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {{
  visibility: visible !important;
  color: var(--text) !important;
}}
[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"] button {{
  color: var(--text) !important;
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 9999px !important;
  width: 32px !important;
  height: 32px !important;
  box-shadow: none !important;
}}
[data-testid="stSidebarCollapseButton"] button:hover,
[data-testid="collapsedControl"] button:hover {{
  background: var(--hover) !important;
}}
[data-testid="stSidebarCollapseButton"] span,
[data-testid="collapsedControl"] span {{
  font-size: 0 !important; visibility: hidden !important;
}}
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="collapsedControl"] svg {{
  visibility: visible !important;
  color: var(--text) !important;
  fill: var(--text) !important;
}}

/* === Page === */
.stApp {{ background: var(--bg) !important; color: var(--text); }}
[data-testid="stAppViewContainer"] {{ background: transparent; }}
.stMarkdown, .stText, p, span, label, div {{ color: var(--text2); }}

/* === HERO === */
.safes-hero {{
  display: block; width: 100%; box-sizing: border-box;
  text-align: center; padding: 48px 40px 40px; margin-bottom: 32px;
  border-bottom: 1px solid var(--border);
}}
.stMarkdown:has(.safes-hero), .stMarkdown > div:has(.safes-hero) {{ width: 100%; }}
.safes-hero-title {{
  font-family: 'SF Pro Rounded', ui-rounded, system-ui, sans-serif !important;
  font-size: 48px !important; font-weight: 500 !important; color: var(--text) !important;
  margin: 0 !important; line-height: 1.0 !important; letter-spacing: -0.02em;
}}
.safes-hero-subtitle {{ font-size: 18px; color: var(--muted); margin-top: 12px; line-height: 1.56; }}
.safes-hero-stats {{ display: flex; justify-content: center; gap: 40px; margin-top: 28px; }}
.safes-hero-stat {{ text-align: center; }}
.safes-hero-stat-value {{
  font-family: 'SF Pro Rounded', ui-rounded, system-ui, sans-serif !important;
  font-size: 30px; font-weight: 500; color: var(--text); display: block; line-height: 1;
}}
.safes-hero-stat-label {{
  font-size: 12px; color: var(--faint); text-transform: uppercase; letter-spacing: 0.08em; margin-top: 6px;
}}

/* === Sections === */
.safes-section {{ margin: 12px 0 20px; }}
.safes-section h3 {{
  font-family: 'SF Pro Rounded', ui-rounded, system-ui, sans-serif !important;
  font-size: 24px !important; font-weight: 500 !important; color: var(--text) !important;
  margin: 0 0 4px !important;
}}
.safes-section p {{ font-size: 14px; color: var(--muted); margin: 0; }}

/* === Cards === */
.safes-card {{
  background: var(--bg); border: 1px solid var(--border); border-radius: 12px;
  padding: 20px 24px; margin-bottom: 12px; color: var(--text2);
}}
.safes-card-title {{ font-size: 16px; font-weight: 500; color: var(--text); margin: 0 0 6px; }}
.safes-card-meta {{ font-size: 14px; color: var(--muted); display: flex; gap: 12px; flex-wrap: wrap; }}

/* === Answer === */
.safes-answer {{
  background: var(--bg); border: 1px solid var(--border); border-left: 3px solid var(--accent);
  border-radius: 12px; padding: 24px 28px; margin: 16px 0; font-size: 16px; line-height: 1.6; color: var(--text2);
}}
.safes-answer-label {{
  display: inline-block; font-size: 12px; font-weight: 500; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--muted); margin-bottom: 12px;
}}

/* === Badges === */
.safes-badge {{
  display: inline-flex; align-items: center; gap: 4px; padding: 4px 12px;
  border-radius: 9999px; font-size: 12px; font-weight: 500;
  background: var(--surface); color: var(--muted); border: 1px solid var(--border);
}}

/* === Confidence === */
.safes-confidence {{
  background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; margin: 12px 0;
}}
.safes-confidence-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
.safes-confidence-label {{ font-size: 12px; font-weight: 500; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }}
.safes-confidence-value {{
  font-family: 'SF Pro Rounded', ui-rounded, system-ui, sans-serif !important;
  font-size: 24px; font-weight: 500; color: var(--text);
}}
.safes-confidence-bar {{ height: 6px; background: var(--surface); border-radius: 9999px; overflow: hidden; }}
.safes-confidence-fill {{ height: 100%; border-radius: 9999px; background: var(--accent); }}

/* === Citations === */
.safes-citation {{
  background: var(--bg); border: 1px solid var(--border); border-radius: 12px;
  padding: 14px 18px; margin: 8px 0; display: flex; align-items: flex-start; gap: 14px;
}}
.safes-citation-id {{
  flex-shrink: 0; width: 28px; height: 28px; background: var(--accent); color: var(--bg);
  border-radius: 9999px; display: flex; align-items: center; justify-content: center;
  font-weight: 500; font-size: 13px;
}}
.safes-citation-body {{ flex: 1; min-width: 0; }}
.safes-citation-doc {{ font-weight: 500; font-size: 14px; color: var(--text); word-break: break-all; }}
.safes-citation-meta {{ font-size: 12px; color: var(--muted); margin-top: 4px; display: flex; gap: 12px; flex-wrap: wrap; }}

/* === Buttons (pill) === */
.stButton > button {{
  border-radius: 9999px !important; font-weight: 500 !important; font-size: 14px !important;
  padding: 10px 24px !important; border: 1px solid var(--border) !important;
  background: var(--active) !important; color: var(--text2) !important; box-shadow: none !important;
}}
.stButton > button:hover {{
  background: var(--hover) !important; border-color: var(--hover) !important;
  transform: none !important; box-shadow: none !important;
}}
.stButton > button[kind="primary"] {{
  background: var(--accent) !important; color: var(--bg) !important;
  border: 1px solid var(--accent) !important;
}}
.stButton > button[kind="primary"]:hover {{
  opacity: 0.85; color: var(--bg) !important; box-shadow: none !important;
}}

/* === Inputs (pill) === */
.stTextInput input, .stNumberInput input, [data-baseweb="input"] input {{
  border-radius: 9999px !important; border: 1px solid var(--border) !important;
  background: var(--bg) !important; color: var(--text) !important; padding: 10px 20px !important; box-shadow: none !important;
}}
.stTextArea textarea {{
  border-radius: 12px !important; border: 1px solid var(--border) !important;
  background: var(--bg) !important; color: var(--text) !important; box-shadow: none !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{ border-color: var(--accent) !important; box-shadow: none !important; }}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {{ color: var(--faint) !important; }}
.stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label,
.stFileUploader label {{ color: var(--text) !important; font-weight: 500 !important; font-size: 14px !important; }}
.stSelectbox > div > div {{
  border-radius: 9999px !important; border: 1px solid var(--border) !important;
  background: var(--bg) !important; box-shadow: none !important;
}}
[data-baseweb="popover"] {{ background: var(--bg) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; box-shadow: none !important; }}
[data-baseweb="popover"] li {{ background: var(--bg) !important; color: var(--text) !important; }}
[data-baseweb="popover"] li:hover {{ background: var(--surface) !important; }}

/* === Sidebar === */
section[data-testid="stSidebar"] {{
  background: var(--sidebar-bg) !important; border-right: 1px solid var(--border); min-width: 0px !important;
}}
section[data-testid="stSidebar"][aria-expanded="false"] {{ min-width: 0 !important; width: 0 !important; }}
section[data-testid="stSidebar"] * {{ color: var(--text2); }}
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {{
  color: var(--text); font-weight: 500;
}}

/* Sidebar nav (radio as pills) */
section[data-testid="stSidebar"] .stRadio > div {{ display: flex !important; flex-direction: column !important; gap: 2px !important; }}
section[data-testid="stSidebar"] .stRadio > div > label {{
  border-radius: 9999px !important; padding: 8px 16px !important; font-size: 14px !important;
  font-weight: 400 !important; color: var(--muted) !important; cursor: pointer !important; margin: 0 !important;
  display: flex !important; align-items: center !important; gap: 8px !important;
}}
section[data-testid="stSidebar"] .stRadio > div > label:hover {{
  background: var(--surface) !important; color: var(--text) !important;
}}
section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
section[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {{
  background: var(--active) !important; color: var(--text) !important; font-weight: 500 !important;
}}
section[data-testid="stSidebar"] .stRadio > div > label > div:first-child {{ display: none !important; }}
section[data-testid="stSidebar"] .stRadio > label {{ display: none !important; }}

/* === File uploader === */
[data-testid="stFileUploaderDropzone"] {{
  background: var(--surface) !important; border: 1px dashed var(--border) !important;
  border-radius: 12px !important; padding: 18px 16px !important;
  display: flex !important; flex-direction: column !important; align-items: center !important; gap: 10px !important;
}}
[data-testid="stFileUploaderDropzone"]:hover {{ border-color: var(--muted) !important; }}
[data-testid="stFileUploaderDropzone"] span {{ color: var(--text2) !important; }}
[data-testid="stFileUploaderDropzone"] small {{ color: var(--faint) !important; }}
[data-testid="stFileUploaderDropzone"] svg {{ color: var(--muted) !important; }}
/* Hide ALL buttons inside the dropzone by default */
[data-testid="stFileUploaderDropzone"] button {{
  display: none !important;
}}
/* Show only the FIRST button (Browse) */
[data-testid="stFileUploaderDropzone"] button:first-of-type {{
  display: inline-flex !important;
  font-size: 0 !important; line-height: 0 !important; text-indent: -9999px !important;
  background: var(--active) !important; border: none !important; border-radius: 9999px !important;
  padding: 8px 18px !important; min-width: 120px !important; height: 36px !important;
  cursor: pointer !important; box-shadow: none !important;
  align-items: center !important; justify-content: center !important;
}}
[data-testid="stFileUploaderDropzone"] button:first-of-type > * {{
  font-size: 0 !important; visibility: hidden !important; width: 0 !important; height: 0 !important;
  position: absolute !important; left: -9999px !important;
}}
[data-testid="stFileUploaderDropzone"] button:first-of-type::before {{
  content: 'Browse'; font-size: 14px !important; font-weight: 500 !important; color: var(--text2) !important;
  text-indent: 0 !important; visibility: visible !important; position: static !important;
  display: inline-block !important; width: auto !important; height: auto !important;
}}
[data-testid="stFileUploaderDropzone"] button:first-of-type:hover {{ background: var(--hover) !important; }}
[data-testid="stFileUploaderDeleteBtn"] button {{ background: transparent !important; color: var(--muted) !important; }}
[data-testid="stFileUploaderDeleteBtn"] button::before {{ content: '' !important; }}

/* Hide the duplicate Browse button that appears outside the dropzone when a file is selected */
section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {{
  display: none !important;
}}
/* But keep the one inside the dropzone visible */
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {{
  display: inline-flex !important;
}}

/* === Metrics === */
[data-testid="stMetric"] {{ background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; }}
[data-testid="stMetricValue"] {{
  font-family: 'SF Pro Rounded', ui-rounded, system-ui, sans-serif !important;
  font-size: 30px !important; font-weight: 500 !important; color: var(--text) !important;
  -webkit-text-fill-color: var(--text) !important; background: none !important;
}}
[data-testid="stMetricLabel"] {{ font-weight: 500 !important; color: var(--muted) !important; text-transform: uppercase; letter-spacing: 0.05em; font-size: 12px !important; }}

/* === Expanders === */
.streamlit-expanderHeader, [data-testid="stExpander"] summary {{
  background: var(--bg) !important; border: 1px solid var(--border) !important;
  border-radius: 12px !important; font-weight: 500 !important; color: var(--text) !important; box-shadow: none !important;
}}
.streamlit-expanderHeader:hover, [data-testid="stExpander"] summary:hover {{ background: var(--surface) !important; }}

/* === Sliders === */
.stSlider [data-baseweb="slider"] [role="slider"] {{ background: var(--accent) !important; border-color: var(--accent) !important; }}
.stSlider [data-baseweb="slider"] > div > div {{ background: var(--accent) !important; }}

/* === Progress === */
.stProgress > div > div > div > div {{ background: var(--accent) !important; }}

/* === Alerts === */
.stAlert {{ border-radius: 12px !important; box-shadow: none !important; }}

/* === Grounding === */
.safes-grounding {{
  background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 14px 20px; margin: 12px 0;
}}

/* === Footer === */
.safes-footer {{
  text-align: center; padding: 32px 0; color: var(--faint); font-size: 14px;
  border-top: 1px solid var(--border); margin-top: 48px;
}}
.safes-footer strong {{ color: var(--text); font-weight: 500; }}

/* === Tabs (hidden — sidebar nav) === */
.stTabs [data-baseweb="tab-list"] {{ display: none !important; }}
</style>
"""


def init_styles(theme_name: str = "Minimal") -> None:
    """Inject themed CSS."""
    theme = THEMES.get(theme_name, THEMES["Minimal"])
    st.markdown(_css(theme), unsafe_allow_html=True)


def theme_selector() -> str:
    """Theme picker in sidebar."""
    if "safes_theme" not in st.session_state:
        st.session_state.safes_theme = "Minimal"
    theme = st.selectbox(
        "Theme",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.safes_theme),
        key="_theme_sel",
    )
    if theme != st.session_state.safes_theme:
        st.session_state.safes_theme = theme
        st.rerun()
    return theme


def render_hero(doc_count: int = 0, query_count: int = 0, llm_model: str = "GLM-5") -> None:
    st.markdown(
        f"""<div class="safes-hero">
          <div class="safes-hero-title">SAFES</div>
          <p class="safes-hero-subtitle">Source-Aware Framework for Exam Support.<br>
          Grounded answers from your own study materials.</p>
          <div class="safes-hero-stats">
            <div class="safes-hero-stat"><span class="safes-hero-stat-value">{doc_count}</span>
              <div class="safes-hero-stat-label">Documents</div></div>
            <div class="safes-hero-stat"><span class="safes-hero-stat-value">{query_count}</span>
              <div class="safes-hero-stat-label">Queries</div></div>
            <div class="safes-hero-stat"><span class="safes-hero-stat-value">{llm_model}</span>
              <div class="safes-hero-stat-label">Model</div></div>
          </div></div>""",
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str = "", icon: str = "") -> None:
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f'<div class="safes-section"><h3>{title}</h3>{sub}</div>', unsafe_allow_html=True)


def render_answer(answer_text: str) -> None:
    safe = answer_text.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
    st.markdown(
        f'<div class="safes-answer"><div class="safes-answer-label">Answer</div><div>{safe}</div></div>',
        unsafe_allow_html=True,
    )


def render_confidence_meter(confidence: float, bloom_level: str = "") -> None:
    confidence = max(0.0, min(1.0, float(confidence)))
    pct = confidence * 100
    label = "High" if confidence >= 0.75 else "Moderate" if confidence >= 0.5 else "Low"
    bloom = f'<span class="safes-badge">{bloom_level.title()}</span>' if bloom_level else ""
    st.markdown(
        f"""<div class="safes-confidence">
          <div class="safes-confidence-header">
            <div><span class="safes-confidence-label">{label} confidence</span> {bloom}</div>
            <span class="safes-confidence-value">{pct:.0f}%</span>
          </div>
          <div class="safes-confidence-bar">
            <div class="safes-confidence-fill" style="width: {pct}%;"></div>
          </div></div>""",
        unsafe_allow_html=True,
    )


def render_citations(citations: List[Dict]) -> None:
    if not citations:
        st.markdown('<div class="safes-card" style="text-align:center;color:var(--muted);">No citations.</div>', unsafe_allow_html=True)
        return
    render_section_header("Sources", f"{len(citations)} citation(s)")
    for c in citations:
        st.markdown(
            f"""<div class="safes-citation">
              <div class="safes-citation-id">{c.get('id','?')}</div>
              <div class="safes-citation-body">
                <div class="safes-citation-doc">{c.get('document_id','?')}</div>
                <div class="safes-citation-meta">
                  <span>Page {c.get('page_number','?')}</span>
                  <span>{c.get('section_title','General')}</span>
                  <span>Score {c.get('score',0)}</span>
                </div></div></div>""",
            unsafe_allow_html=True,
        )


def render_document_card(doc: Dict) -> None:
    st.markdown(
        f"""<div class="safes-card">
          <div class="safes-card-title">{doc.get('filename','Untitled')}</div>
          <div class="safes-card-meta"><span>{doc.get('chunks',0)} chunks</span>
            <span class="safes-badge">{doc.get('status','?')}</span></div>
          <div style="font-size:12px;color:var(--faint);margin-top:6px;"><code>{doc.get('document_id','')}</code></div>
        </div>""",
        unsafe_allow_html=True,
    )


def render_practice_questions(questions: List[str]) -> None:
    if not questions:
        return
    render_section_header("Practice Questions")
    for i, q in enumerate(questions, 1):
        st.markdown(
            f"""<div class="safes-card" style="border-left:2px solid var(--accent);">
              <div style="display:flex;gap:14px;align-items:flex-start;">
                <div class="safes-citation-id">{i}</div>
                <div style="flex:1;padding-top:4px;font-size:14px;">{q}</div>
              </div></div>""",
            unsafe_allow_html=True,
        )


def render_grounding_alert(grounding: Dict) -> None:
    method = grounding.get("verification_method", "heuristic")
    is_g = grounding.get("is_grounded", True)
    overlap = grounding.get("keyword_overlap", 0.0)
    unsup = grounding.get("unsupported_claims", [])
    status = "Grounded" if is_g else "Low grounding"
    icon = "+" if is_g else "!"
    st.markdown(
        f"""<div class="safes-grounding">
          <div style="font-weight:500;color:var(--text);margin-bottom:4px;">[{icon}] {status}</div>
          <div style="font-size:14px;color:var(--muted);">
            Verification: {method} &middot; Overlap: {overlap:.0%}
            {f" &middot; {len(unsup)} unsupported" if unsup else ""}
          </div></div>""",
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        '<div class="safes-footer"><strong>SAFES</strong> &middot; Source-Aware Framework for Exam Support</div>',
        unsafe_allow_html=True,
    )
