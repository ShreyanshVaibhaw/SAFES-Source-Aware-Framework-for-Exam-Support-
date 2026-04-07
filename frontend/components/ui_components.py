"""Reusable Streamlit UI components for SAFES with multi-theme support."""

from __future__ import annotations

from typing import Dict, List

import streamlit as st

# =============================================================================
# THEMES
# Five committed aesthetics — pick one via theme_selector()
# =============================================================================

THEMES: Dict[str, Dict[str, str]] = {
    "Light": {
        "primary": "#4F46E5",
        "primary_2": "#7C3AED",
        "primary_3": "#DB2777",
        "deep": "#1E1B4B",
        "mint": "#10B981",
        "amber": "#F59E0B",
        "rose": "#F43F5E",
        "bg_1": "#FAFAFE",
        "bg_2": "#F3F4F8",
        "surface": "#FFFFFF",
        "surface_2": "#FAFBFF",
        "border": "#E5E7EB",
        "border_2": "#E0E7FF",
        "text": "#1F2937",
        "muted": "#6B7280",
        "answer_bg": "#FFFFFF",
        "answer_grad": "#FAFBFF",
        "card_bg": "#FFFFFF",
        "sidebar_bg_1": "#FFFFFF",
        "sidebar_bg_2": "#FAFBFF",
        "tab_bg": "#FFFFFF",
        "code_bg": "#F3F4F6",
    },
    "Dark": {
        "primary": "#818CF8",
        "primary_2": "#A78BFA",
        "primary_3": "#F472B6",
        "deep": "#E0E7FF",
        "mint": "#34D399",
        "amber": "#FBBF24",
        "rose": "#FB7185",
        "bg_1": "#0F172A",
        "bg_2": "#1E293B",
        "surface": "#1E293B",
        "surface_2": "#243049",
        "border": "#334155",
        "border_2": "#3730A3",
        "text": "#F1F5F9",
        "muted": "#94A3B8",
        "answer_bg": "#1E293B",
        "answer_grad": "#243049",
        "card_bg": "#1E293B",
        "sidebar_bg_1": "#0F172A",
        "sidebar_bg_2": "#1E293B",
        "tab_bg": "#1E293B",
        "code_bg": "#0F172A",
    },
    "Midnight": {
        "primary": "#22D3EE",
        "primary_2": "#A78BFA",
        "primary_3": "#F472B6",
        "deep": "#E0F2FE",
        "mint": "#4ADE80",
        "amber": "#FACC15",
        "rose": "#FB7185",
        "bg_1": "#000000",
        "bg_2": "#0A0A0F",
        "surface": "#0F0F1A",
        "surface_2": "#161628",
        "border": "#27272A",
        "border_2": "#312E81",
        "text": "#FAFAFA",
        "muted": "#A1A1AA",
        "answer_bg": "#0F0F1A",
        "answer_grad": "#161628",
        "card_bg": "#0F0F1A",
        "sidebar_bg_1": "#000000",
        "sidebar_bg_2": "#0A0A0F",
        "tab_bg": "#0F0F1A",
        "code_bg": "#000000",
    },
    "Sunset": {
        "primary": "#F97316",
        "primary_2": "#EF4444",
        "primary_3": "#EC4899",
        "deep": "#7C2D12",
        "mint": "#65A30D",
        "amber": "#EAB308",
        "rose": "#E11D48",
        "bg_1": "#FFF7ED",
        "bg_2": "#FFEDD5",
        "surface": "#FFFFFF",
        "surface_2": "#FFFBF5",
        "border": "#FED7AA",
        "border_2": "#FDBA74",
        "text": "#431407",
        "muted": "#9A3412",
        "answer_bg": "#FFFFFF",
        "answer_grad": "#FFFBF5",
        "card_bg": "#FFFFFF",
        "sidebar_bg_1": "#FFFFFF",
        "sidebar_bg_2": "#FFF7ED",
        "tab_bg": "#FFFFFF",
        "code_bg": "#FFF7ED",
    },
    "Ocean": {
        "primary": "#0891B2",
        "primary_2": "#0EA5E9",
        "primary_3": "#06B6D4",
        "deep": "#083344",
        "mint": "#10B981",
        "amber": "#F59E0B",
        "rose": "#F43F5E",
        "bg_1": "#F0F9FF",
        "bg_2": "#E0F2FE",
        "surface": "#FFFFFF",
        "surface_2": "#F7FCFF",
        "border": "#BAE6FD",
        "border_2": "#7DD3FC",
        "text": "#082F49",
        "muted": "#0369A1",
        "answer_bg": "#FFFFFF",
        "answer_grad": "#F7FCFF",
        "card_bg": "#FFFFFF",
        "sidebar_bg_1": "#FFFFFF",
        "sidebar_bg_2": "#F0F9FF",
        "tab_bg": "#FFFFFF",
        "code_bg": "#F0F9FF",
    },
}


def _build_css(theme: Dict[str, str]) -> str:
    """Build the full CSS stylesheet from a theme palette."""
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {{
  --safes-primary: {theme['primary']};
  --safes-primary-2: {theme['primary_2']};
  --safes-primary-3: {theme['primary_3']};
  --safes-deep: {theme['deep']};
  --safes-mint: {theme['mint']};
  --safes-amber: {theme['amber']};
  --safes-rose: {theme['rose']};
  --safes-bg-1: {theme['bg_1']};
  --safes-bg-2: {theme['bg_2']};
  --safes-surface: {theme['surface']};
  --safes-surface-2: {theme['surface_2']};
  --safes-border: {theme['border']};
  --safes-border-2: {theme['border_2']};
  --safes-text: {theme['text']};
  --safes-muted: {theme['muted']};
  --safes-answer-bg: {theme['answer_bg']};
  --safes-answer-grad: {theme['answer_grad']};
  --safes-card-bg: {theme['card_bg']};
  --safes-sidebar-bg-1: {theme['sidebar_bg_1']};
  --safes-sidebar-bg-2: {theme['sidebar_bg_2']};
  --safes-tab-bg: {theme['tab_bg']};
  --safes-code-bg: {theme['code_bg']};
  --safes-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 4px 12px rgba(0, 0, 0, 0.04);
  --safes-shadow-lg: 0 4px 6px rgba(0, 0, 0, 0.08), 0 12px 24px rgba(0, 0, 0, 0.08);
}}

/* === Global font === */
html, body, [class*="css"], .stMarkdown, .stText, button, input, textarea, select,
h1, h2, h3, h4, h5, h6, p, span, div, .stApp * {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}}

code, pre, .stCode, [class*="language-"] {{
  font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
  background: var(--safes-code-bg) !important;
  color: var(--safes-text) !important;
}}

/* === Hide Streamlit chrome === */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header[data-testid="stHeader"] {{background: transparent;}}

/* === Page background === */
.stApp {{
  background: linear-gradient(180deg, var(--safes-bg-1) 0%, var(--safes-bg-2) 100%) !important;
  color: var(--safes-text);
}}

[data-testid="stAppViewContainer"] {{
  background: transparent;
}}

/* Default text color */
.stMarkdown, .stText, p, span, label, div {{
  color: var(--safes-text);
}}

/* === HERO HEADER === */
.safes-hero {{
  position: relative;
  display: block;
  width: 100%;
  box-sizing: border-box;
  background: linear-gradient(135deg, var(--safes-primary) 0%, var(--safes-primary-2) 50%, var(--safes-primary-3) 100%);
  border-radius: 20px;
  padding: 32px 40px;
  margin-bottom: 24px;
  color: white;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}}

.stMarkdown:has(.safes-hero), .stMarkdown > div:has(.safes-hero) {{
  width: 100%;
}}

.safes-hero::before {{
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 60%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, transparent 70%);
  pointer-events: none;
}}

.safes-hero-content {{
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}}

.safes-hero-title {{
  font-size: 2.75rem !important;
  font-weight: 800 !important;
  letter-spacing: -0.02em !important;
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1.1 !important;
  color: white !important;
  text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}}

.safes-hero-title-row {{
  display: flex;
  align-items: center;
  gap: 14px;
  margin: 4px 0 8px 0;
}}

.safes-hero-mark {{
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
}}

.safes-hero-subtitle {{
  font-size: 1rem;
  font-weight: 500;
  opacity: 0.95;
  margin-top: 6px;
  max-width: 540px;
  color: white !important;
}}

.safes-hero-badge {{
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
  color: white;
}}

.safes-hero-stats {{
  display: flex;
  gap: 28px;
  flex-wrap: wrap;
}}

.safes-hero-stat {{
  text-align: center;
}}

.safes-hero-stat-value {{
  font-size: 1.6rem;
  font-weight: 800;
  display: block;
  line-height: 1;
  color: white !important;
}}

.safes-hero-stat-label {{
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  opacity: 0.85;
  margin-top: 4px;
  color: white;
}}

/* === SECTION HEADERS === */
.safes-section {{
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 8px 0 16px 0;
}}

.safes-section-icon {{
  width: 36px;
  height: 36px;
  background: var(--safes-surface-2);
  border: 1px solid var(--safes-border-2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}}

.safes-section-text h3 {{
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--safes-deep);
  letter-spacing: -0.01em;
}}

.safes-section-text p {{
  margin: 2px 0 0 0;
  font-size: 0.85rem;
  color: var(--safes-muted);
}}

/* === CARDS === */
.safes-card {{
  background: var(--safes-card-bg);
  border: 1px solid var(--safes-border);
  border-radius: 14px;
  padding: 18px 20px;
  margin-bottom: 12px;
  box-shadow: var(--safes-shadow);
  transition: all 0.2s ease;
  color: var(--safes-text);
}}

.safes-card:hover {{
  transform: translateY(-2px);
  box-shadow: var(--safes-shadow-lg);
  border-color: var(--safes-primary);
}}

.safes-card-title {{
  font-size: 1rem;
  font-weight: 700;
  color: var(--safes-deep);
  margin: 0 0 6px 0;
}}

.safes-card-meta {{
  font-size: 0.8rem;
  color: var(--safes-muted);
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}}

/* === ANSWER CARD === */
.safes-answer {{
  background: linear-gradient(135deg, var(--safes-answer-bg) 0%, var(--safes-answer-grad) 100%);
  border: 1px solid var(--safes-border-2);
  border-left: 4px solid var(--safes-primary);
  border-radius: 14px;
  padding: 24px 28px;
  margin: 16px 0;
  box-shadow: var(--safes-shadow-lg);
  font-size: 1rem;
  line-height: 1.7;
  color: var(--safes-text);
}}

.safes-answer-label {{
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--safes-primary);
  margin-bottom: 12px;
}}

/* === BADGES === */
.safes-badge {{
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  border: 1px solid;
}}

.safes-badge-indigo {{
  background: rgba(79, 70, 229, 0.12);
  color: var(--safes-primary);
  border-color: rgba(79, 70, 229, 0.3);
}}

.safes-badge-mint {{
  background: rgba(16, 185, 129, 0.12);
  color: var(--safes-mint);
  border-color: rgba(16, 185, 129, 0.3);
}}

.safes-badge-amber {{
  background: rgba(245, 158, 11, 0.12);
  color: var(--safes-amber);
  border-color: rgba(245, 158, 11, 0.3);
}}

.safes-badge-rose {{
  background: rgba(244, 63, 94, 0.12);
  color: var(--safes-rose);
  border-color: rgba(244, 63, 94, 0.3);
}}

.safes-badge-violet {{
  background: rgba(124, 58, 237, 0.12);
  color: var(--safes-primary-2);
  border-color: rgba(124, 58, 237, 0.3);
}}

/* === CONFIDENCE METER === */
.safes-confidence {{
  background: var(--safes-card-bg);
  border: 1px solid var(--safes-border);
  border-radius: 12px;
  padding: 14px 18px;
  margin: 12px 0;
}}

.safes-confidence-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}}

.safes-confidence-label {{
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--safes-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

.safes-confidence-value {{
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: -0.01em;
}}

.safes-confidence-bar {{
  height: 8px;
  background: var(--safes-border);
  border-radius: 999px;
  overflow: hidden;
  position: relative;
}}

.safes-confidence-fill {{
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* === CITATIONS === */
.safes-citation {{
  background: var(--safes-surface-2);
  border: 1px solid var(--safes-border);
  border-radius: 10px;
  padding: 12px 16px;
  margin: 8px 0;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  transition: all 0.2s ease;
}}

.safes-citation:hover {{
  border-color: var(--safes-primary);
}}

.safes-citation-id {{
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, var(--safes-primary), var(--safes-primary-2));
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
}}

.safes-citation-body {{
  flex: 1;
  min-width: 0;
}}

.safes-citation-doc {{
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--safes-deep);
  word-break: break-all;
}}

.safes-citation-meta {{
  font-size: 0.75rem;
  color: var(--safes-muted);
  margin-top: 2px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}}

/* === STREAMLIT TABS === */
.stTabs [data-baseweb="tab-list"] {{
  gap: 6px;
  background: var(--safes-tab-bg);
  padding: 6px;
  border-radius: 14px;
  border: 1px solid var(--safes-border);
  box-shadow: var(--safes-shadow);
}}

.stTabs [data-baseweb="tab"] {{
  border-radius: 10px !important;
  padding: 10px 18px !important;
  font-weight: 600 !important;
  color: var(--safes-muted) !important;
  background: transparent !important;
  transition: all 0.2s ease;
  border: none !important;
}}

.stTabs [data-baseweb="tab"]:hover {{
  background: var(--safes-surface-2) !important;
  color: var(--safes-primary) !important;
}}

.stTabs [aria-selected="true"] {{
  background: linear-gradient(135deg, var(--safes-primary), var(--safes-primary-2)) !important;
  color: white !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}}

/* === STREAMLIT BUTTONS === */
/* Default secondary button */
.stButton > button {{
  border-radius: 10px !important;
  font-weight: 600 !important;
  padding: 10px 22px !important;
  transition: all 0.2s ease !important;
  border: 1px solid var(--safes-border) !important;
  background: var(--safes-surface) !important;
  color: var(--safes-text) !important;
  font-family: 'Inter', sans-serif !important;
}}

.stButton > button:hover {{
  transform: translateY(-1px);
  box-shadow: var(--safes-shadow-lg) !important;
  border-color: var(--safes-primary) !important;
  color: var(--safes-primary) !important;
}}

/* Primary button (gradient) */
.stButton > button[kind="primary"] {{
  background: linear-gradient(135deg, var(--safes-primary), var(--safes-primary-2)) !important;
  color: white !important;
  border: none !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}}

.stButton > button[kind="primary"]:hover {{
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
  transform: translateY(-2px);
  color: white !important;
}}

/* === STREAMLIT INPUTS === */
.stTextInput input, .stTextArea textarea, .stSelectbox > div > div,
.stNumberInput input, [data-baseweb="input"] input {{
  border-radius: 10px !important;
  border: 1px solid var(--safes-border) !important;
  background: var(--safes-surface) !important;
  color: var(--safes-text) !important;
  font-family: 'Inter', sans-serif !important;
  transition: all 0.2s ease;
}}

.stTextInput input:focus, .stTextArea textarea:focus {{
  border-color: var(--safes-primary) !important;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
}}

/* Input labels */
.stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label,
.stFileUploader label, .stRadio label, .stCheckbox label {{
  color: var(--safes-text) !important;
  font-weight: 600 !important;
  font-size: 0.85rem !important;
}}

/* === SIDEBAR === */
section[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, var(--safes-sidebar-bg-1) 0%, var(--safes-sidebar-bg-2) 100%) !important;
  border-right: 1px solid var(--safes-border);
}}

section[data-testid="stSidebar"] * {{
  color: var(--safes-text);
}}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{
  color: var(--safes-deep);
  font-weight: 700;
  letter-spacing: -0.01em;
}}

/* === FILE UPLOADER (NUCLEAR FIX) === */
section[data-testid="stFileUploader"] {{
  background: transparent !important;
}}

section[data-testid="stFileUploader"] > div {{
  background: transparent !important;
  border: none !important;
}}

[data-testid="stFileUploaderDropzone"] {{
  background: var(--safes-surface-2) !important;
  border: 2px dashed var(--safes-border-2) !important;
  border-radius: 12px !important;
  padding: 18px 16px !important;
  transition: all 0.2s ease;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  gap: 10px !important;
  text-align: center !important;
}}

[data-testid="stFileUploaderDropzone"]:hover {{
  border-color: var(--safes-primary) !important;
  background: var(--safes-surface) !important;
}}

/* Instructions block (text + icon) */
[data-testid="stFileUploaderDropzoneInstructions"] {{
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  gap: 6px !important;
  width: 100% !important;
  background: transparent !important;
}}

[data-testid="stFileUploaderDropzoneInstructions"] svg {{
  width: 28px !important;
  height: 28px !important;
  color: var(--safes-primary) !important;
  fill: var(--safes-primary) !important;
}}

[data-testid="stFileUploaderDropzoneInstructions"] span {{
  color: var(--safes-text) !important;
  font-size: 0.85rem !important;
  font-weight: 600 !important;
}}

[data-testid="stFileUploaderDropzoneInstructions"] small {{
  color: var(--safes-muted) !important;
  font-size: 0.7rem !important;
}}

/* === The INTERNAL Browse button - hide original text, use ::before === */
[data-testid="stFileUploaderDropzone"] button {{
  /* Hide whatever text Streamlit puts here */
  font-size: 0 !important;
  line-height: 0 !important;
  text-indent: -9999px !important;
  /* Then style the button itself */
  background: var(--safes-primary) !important;
  background-image: none !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 8px 18px !important;
  min-width: 130px !important;
  height: 36px !important;
  cursor: pointer !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1) !important;
  text-shadow: none !important;
  transition: all 0.2s ease !important;
  position: relative !important;
  overflow: hidden !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}}

/* Hide ALL children of the button (including any nested spans/p elements) */
[data-testid="stFileUploaderDropzone"] button > * {{
  font-size: 0 !important;
  visibility: hidden !important;
  width: 0 !important;
  height: 0 !important;
  overflow: hidden !important;
  position: absolute !important;
  left: -9999px !important;
}}

/* Inject our own clean text via pseudo-element */
[data-testid="stFileUploaderDropzone"] button::before {{
  content: '📁 Browse';
  font-size: 0.85rem !important;
  line-height: 1 !important;
  font-weight: 600 !important;
  color: white !important;
  text-indent: 0 !important;
  font-family: 'Inter', -apple-system, sans-serif !important;
  visibility: visible !important;
  position: static !important;
  display: inline-block !important;
  width: auto !important;
  height: auto !important;
}}

[data-testid="stFileUploaderDropzone"] button:hover {{
  background: var(--safes-primary-2) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}}

/* Uploaded file display */
[data-testid="stFileUploaderFile"] {{
  background: var(--safes-surface) !important;
  border: 1px solid var(--safes-border) !important;
  border-radius: 8px !important;
  padding: 8px !important;
}}

[data-testid="stFileUploaderFileName"] {{
  color: var(--safes-text) !important;
}}

[data-testid="stFileUploaderDeleteBtn"] button {{
  background: transparent !important;
  color: var(--safes-rose) !important;
}}

[data-testid="stFileUploaderDeleteBtn"] button::before {{
  content: '' !important;
}}

/* === METRICS === */
[data-testid="stMetric"] {{
  background: var(--safes-card-bg);
  border: 1px solid var(--safes-border);
  border-radius: 14px;
  padding: 16px 20px;
  box-shadow: var(--safes-shadow);
  transition: all 0.2s ease;
}}

[data-testid="stMetric"]:hover {{
  transform: translateY(-2px);
  box-shadow: var(--safes-shadow-lg);
  border-color: var(--safes-primary);
}}

[data-testid="stMetricValue"] {{
  font-size: 2rem !important;
  font-weight: 800 !important;
  background: linear-gradient(135deg, var(--safes-primary), var(--safes-primary-2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}

[data-testid="stMetricLabel"] {{
  font-weight: 600 !important;
  color: var(--safes-muted) !important;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.75rem !important;
}}

/* === EXPANDERS === */
.streamlit-expanderHeader,
[data-testid="stExpander"] summary {{
  background: var(--safes-card-bg) !important;
  border: 1px solid var(--safes-border) !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  color: var(--safes-text) !important;
  transition: all 0.2s ease;
}}

.streamlit-expanderHeader:hover,
[data-testid="stExpander"] summary:hover {{
  border-color: var(--safes-primary) !important;
  background: var(--safes-surface-2) !important;
}}

[data-testid="stExpander"] {{
  background: transparent;
  border: none;
}}

/* === SLIDERS === */
.stSlider [data-baseweb="slider"] [role="slider"] {{
  background: var(--safes-primary) !important;
  border-color: var(--safes-primary) !important;
}}

.stSlider [data-baseweb="slider"] > div > div {{
  background: var(--safes-primary) !important;
}}

/* === ALERTS === */
.stAlert {{
  border-radius: 12px !important;
  border-width: 1px !important;
}}

[data-testid="stAlertContentInfo"] {{
  background: var(--safes-surface-2) !important;
  color: var(--safes-text) !important;
}}

[data-testid="stAlertContentSuccess"] {{
  background: rgba(16, 185, 129, 0.12) !important;
  color: var(--safes-mint) !important;
}}

[data-testid="stAlertContentWarning"] {{
  background: rgba(245, 158, 11, 0.12) !important;
  color: var(--safes-amber) !important;
}}

[data-testid="stAlertContentError"] {{
  background: rgba(244, 63, 94, 0.12) !important;
  color: var(--safes-rose) !important;
}}

/* === PROGRESS BAR === */
.stProgress > div > div > div > div {{
  background: linear-gradient(90deg, var(--safes-primary), var(--safes-primary-2)) !important;
}}

/* === ANIMATIONS === */
@keyframes fadeInUp {{
  from {{ opacity: 0; transform: translateY(12px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

.safes-card, .safes-answer, .safes-citation, .safes-confidence {{
  animation: fadeInUp 0.4s ease-out;
}}

/* === FOOTER === */
.safes-footer {{
  text-align: center;
  padding: 24px 0;
  color: var(--safes-muted);
  font-size: 0.8rem;
  border-top: 1px solid var(--safes-border);
  margin-top: 40px;
}}

.safes-footer-highlight {{
  color: var(--safes-primary);
  font-weight: 700;
}}

/* === THEME PICKER (in sidebar) === */
.safes-theme-picker {{
  background: var(--safes-surface-2);
  border: 1px solid var(--safes-border);
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 12px;
}}

/* === SELECTBOX dropdown popover === */
[data-baseweb="popover"] {{
  background: var(--safes-surface) !important;
  color: var(--safes-text) !important;
}}

[data-baseweb="popover"] li {{
  background: var(--safes-surface) !important;
  color: var(--safes-text) !important;
}}

[data-baseweb="popover"] li:hover {{
  background: var(--safes-surface-2) !important;
}}
</style>
"""


def init_styles(theme_name: str = "Light") -> None:
    """Inject themed CSS styles."""
    theme = THEMES.get(theme_name, THEMES["Light"])
    st.markdown(_build_css(theme), unsafe_allow_html=True)


def theme_selector() -> str:
    """Render a theme selector in the sidebar and return the chosen theme."""
    if "safes_theme" not in st.session_state:
        st.session_state.safes_theme = "Light"

    theme = st.sidebar.selectbox(
        "🎨 Theme",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.safes_theme),
        key="theme_selector_widget",
    )
    if theme != st.session_state.safes_theme:
        st.session_state.safes_theme = theme
        st.rerun()
    return theme


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
    """Render a confidence meter with color coding."""
    confidence = max(0.0, min(1.0, float(confidence)))
    pct = confidence * 100

    if confidence >= 0.75:
        color = "#10B981"
        label = "High Confidence"
    elif confidence >= 0.5:
        color = "#F59E0B"
        label = "Moderate Confidence"
    else:
        color = "#F43F5E"
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
            '<div class="safes-card" style="text-align: center;">'
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
            <div class="safes-card" style="border-left: 3px solid var(--safes-primary-2);">
              <div style="display: flex; gap: 12px; align-items: flex-start;">
                <div class="safes-citation-id">{i}</div>
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
        bg = "rgba(16, 185, 129, 0.12)"
        border = "var(--safes-mint)"
        icon, title = "✅", "Answer Grounded"
    else:
        bg = "rgba(245, 158, 11, 0.12)"
        border = "var(--safes-amber)"
        icon, title = "⚠️", "Low Grounding"

    st.markdown(
        f"""
        <div style="background: {bg}; border-left: 4px solid {border}; border-radius: 10px;
                    padding: 14px 18px; margin: 12px 0; color: var(--safes-text);">
          <div style="font-weight: 700; color: {border}; margin-bottom: 4px;">{icon} {title}</div>
          <div style="font-size: 0.85rem; color: var(--safes-muted);">
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
