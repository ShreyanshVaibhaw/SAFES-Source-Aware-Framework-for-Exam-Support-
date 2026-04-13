"""SAFES - Streamlit frontend with Ollama-inspired minimalist design."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

import requests
import streamlit as st

# Ensure project root is on sys.path so both `frontend.` and `src.` imports work
_project_root = str(Path(__file__).parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from frontend.components.ui_components import (
    init_styles,
    render_answer,
    render_citations,
    render_confidence_meter,
    render_document_card,
    render_footer,
    render_grounding_alert,
    render_hero,
    render_practice_questions,
    render_section_header,
)

API_URL = os.getenv("API_URL", "http://localhost:8000")


def api_get(path: str):
    try:
        return requests.get(f"{API_URL}{path}", timeout=60)
    except requests.exceptions.RequestException:
        return None


def api_post(path: str, payload=None, files=None, data=None):
    try:
        return requests.post(
            f"{API_URL}{path}", json=payload, files=files, data=data, timeout=120
        )
    except requests.exceptions.RequestException:
        return None


def api_delete(path: str):
    try:
        return requests.delete(f"{API_URL}{path}", timeout=60)
    except requests.exceptions.RequestException:
        return None


def _ok(res) -> bool:
    """Safe check for response object."""
    return res is not None and res.ok


# =============================================================================
# SIDEBAR - DOCUMENT MANAGEMENT
# =============================================================================


def sidebar_documents() -> None:
    with st.sidebar:
        st.markdown("### Documents")
        st.caption("Upload your study materials below")

        uploaded = st.file_uploader(
            "Choose a file",
            type=["pdf", "docx", "txt", "md"],
            accept_multiple_files=False,
            label_visibility="collapsed",
        )
        if uploaded and st.button("Upload", type="primary", use_container_width=True):
            with st.spinner(f"Processing {uploaded.name}..."):
                files = {
                    "file": (
                        uploaded.name,
                        uploaded.getvalue(),
                        uploaded.type or "application/octet-stream",
                    )
                }
                res = api_post("/documents/upload", files=files)
                if _ok(res):
                    st.success(f"{uploaded.name} indexed!")
                    st.rerun()
                else:
                    st.error(res.text if res is not None else "API unreachable")

        # List existing documents
        docs_res = api_get("/documents")
        if _ok(docs_res):
            docs = docs_res.json().get("documents", [])
            st.markdown("---")
            st.markdown(f"### Library ({len(docs)})")

            if not docs:
                st.info("No documents yet. Upload one above to get started.")
            else:
                for doc in docs:
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(
                                f"""
                                <div style="font-size: 0.85rem; font-weight: 600; color: #1E1B4B;
                                            white-space: nowrap; overflow: hidden;
                                            text-overflow: ellipsis;">
                                  {doc['filename']}
                                </div>
                                <div style="font-size: 0.7rem; color: #6B7280;">
                                  {doc.get('chunks', 0)} chunks
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        with col2:
                            if st.button("x", key=f"del-{doc['document_id']}", help="Delete"):
                                delete_res = api_delete(f"/documents/{doc['document_id']}")
                                if _ok(delete_res):
                                    st.rerun()
        else:
            st.warning("⚠️ API not reachable. Start the backend server.")


# =============================================================================
# QUERY TAB
# =============================================================================


def query_tab() -> None:
    render_section_header(
        "Ask a Question",
        "Get grounded answers with citations from your uploaded materials",
    )

    question = st.text_area(
        "Your question",
        placeholder="e.g., Explain the difference between TCP and UDP for my networks exam",
        height=100,
        label_visibility="collapsed",
    )

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        bloom = st.selectbox(
            "Bloom Level",
            ["auto", "remember", "understand", "apply", "analyze", "evaluate", "create"],
            index=0,
            help="Cognitive level — auto-detects from question keywords",
        )
    with col2:
        top_k = st.slider("Top-K", 1, 10, 5, help="Number of source chunks to retrieve")
    with col3:
        st.markdown('<div style="height: 28px;"></div>', unsafe_allow_html=True)
        check_hall = st.toggle("Verify", value=True, help="Run hallucination check")

    if st.button("Get Answer", type="primary", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question first.")
            return

        with st.spinner("Searching and generating answer..."):
            payload = {
                "question": question,
                "bloom_level": None if bloom == "auto" else bloom,
                "top_k": top_k,
                "include_citations": True,
                "check_hallucination": check_hall,
            }
            res = api_post("/query", payload=payload)

        if not _ok(res):
            st.error(f"{res.text if res is not None else 'API unreachable'}")
            return

        data = res.json()

        # Render answer
        render_answer(data["answer"])

        # Confidence + bloom level
        render_confidence_meter(data.get("confidence", 0.0), data.get("bloom_level", ""))

        # Grounding alert
        if check_hall and data.get("grounding"):
            render_grounding_alert(data["grounding"])

        # Citations
        render_citations(data.get("citations", []))

        # Practice questions
        if data.get("practice_questions"):
            render_practice_questions(data["practice_questions"])


# =============================================================================
# STUDY GUIDE TAB
# =============================================================================


def study_guide_tab() -> None:
    render_section_header(
        "Study Guide Generator",
        "Generate exam-ready notes from your indexed materials",
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        topics_raw = st.text_input(
            "Topics (comma-separated)",
            value="",
            placeholder="e.g., photosynthesis, cell division, DNA replication",
        )
    with col2:
        level = st.selectbox(
            "Level",
            ["remember", "understand", "apply", "analyze", "evaluate", "create"],
            index=1,
        )

    if st.button("Generate Guide", type="primary", use_container_width=True):
        topics = [t.strip() for t in topics_raw.split(",") if t.strip()]
        if not topics:
            st.warning("Enter at least one topic.")
            return
        with st.spinner("Building your study guide..."):
            res = api_post("/study/guide", payload={"topics": topics, "level": level})
        if _ok(res):
            guide = res.json().get("guide", "")
            st.markdown(
                f'<div class="safes-card">{guide.replace(chr(10), "<br/>")}</div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "Download",
                guide,
                file_name="study_guide.md",
                mime="text/markdown",
                use_container_width=True,
            )
        else:
            st.error(res.text if res is not None else "API unreachable")


# =============================================================================
# COMPARE TOPICS TAB
# =============================================================================


def compare_tab() -> None:
    render_section_header(
        "Compare Topics",
        "Side-by-side comparison of two concepts from your materials",
    )

    col1, col2 = st.columns(2)
    with col1:
        topic_a = st.text_input("Topic A", placeholder="e.g., TCP")
    with col2:
        topic_b = st.text_input("Topic B", placeholder="e.g., UDP")

    if st.button("Compare", type="primary", use_container_width=True):
        if not topic_a or not topic_b:
            st.warning("Please enter both topics.")
            return
        with st.spinner(f"Comparing {topic_a} vs {topic_b}..."):
            res = api_post("/study/compare", payload={"topic_a": topic_a, "topic_b": topic_b})
        if _ok(res):
            data = res.json()
            comparison = data.get("comparison", "")
            st.markdown(
                f'<div class="safes-answer">'
                f'<div class="safes-answer-label">{topic_a} vs {topic_b}</div>'
                f'{comparison.replace(chr(10), "<br/>")}'
                f"</div>",
                unsafe_allow_html=True,
            )
            col1, col2 = st.columns(2)
            col1.metric(f"Sources for {topic_a}", data.get("sources_a", 0))
            col2.metric(f"Sources for {topic_b}", data.get("sources_b", 0))
        else:
            st.error(res.text if res is not None else "API unreachable")


# =============================================================================
# PRACTICE TEST TAB
# =============================================================================


def practice_test_tab() -> None:
    render_section_header(
        "Practice Test",
        "Generate exam questions to test your knowledge",
    )

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        topics_raw = st.text_input(
            "Topics",
            placeholder="e.g., process scheduling, memory management",
        )
    with col2:
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], index=1)
    with col3:
        num_questions = st.slider("Count", 1, 20, 5)

    if st.button("Generate Test", type="primary", use_container_width=True):
        topics: List[str] = [t.strip() for t in topics_raw.split(",") if t.strip()]
        if not topics:
            st.warning("Enter at least one topic.")
            return
        with st.spinner("Generating practice questions..."):
            res = api_post(
                "/study/practice-test",
                payload={
                    "topics": topics,
                    "difficulty": difficulty,
                    "num_questions": num_questions,
                },
            )
        if _ok(res):
            payload = res.json()
            for i, question in enumerate(payload.get("questions", []), 1):
                st.markdown(
                    f"""
                    <div class="safes-card" style="border-left: 3px solid var(--safes-violet);">
                      <div style="display: flex; gap: 12px; align-items: flex-start;">
                        <div class="safes-citation-id"
                             style="background: linear-gradient(135deg, #7C3AED, #DB2777);">{i}</div>
                        <div style="flex: 1;">
                          <div style="font-weight: 600; color: #1E1B4B; margin-bottom: 6px;">
                            {question.get('question', '')}
                          </div>
                          <div style="font-size: 0.8rem; color: #6B7280;">
                            💡 {question.get('hint', '')}
                          </div>
                        </div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.error(res.text if res is not None else "API unreachable")


# =============================================================================
# ANALYTICS TAB
# =============================================================================


def analytics_tab() -> None:
    render_section_header(
        "Analytics & History",
        "Query history, performance stats, and system health",
    )

    # Query stats
    stats_res = api_get("/query/stats")
    if _ok(stats_res):
        stats = stats_res.json()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Queries", stats.get("total_queries", 0))
        col2.metric("Avg Confidence", f"{stats.get('avg_confidence', 0):.0%}")
        col3.metric("Avg Response", f"{stats.get('avg_response_time_ms', 0):.0f}ms")

        bloom_data = stats.get("queries_by_bloom_level", {})
        if bloom_data:
            st.markdown("**Queries by Bloom Level:**")
            cols = st.columns(len(bloom_data))
            for i, (level, count) in enumerate(bloom_data.items()):
                cols[i].markdown(
                    f"""
                    <div class="safes-card" style="text-align: center; padding: 12px;">
                      <div style="font-family: 'SF Pro Rounded', ui-rounded, system-ui, sans-serif;
                                  font-size: 24px; font-weight: 500;
                                  color: #000000;">{count}</div>
                      <div style="font-size: 12px; color: #a3a3a3;
                                  text-transform: uppercase; letter-spacing: 0.05em;">
                        {level}
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("---")
    render_section_header("Recent Queries", "Last 10 questions you asked")

    history_res = api_get("/query/history?limit=10")
    if _ok(history_res):
        history = history_res.json().get("history", [])
        if history:
            for item in history:
                conf = item.get("confidence", 0)
                with st.expander(f"{item.get('question', '')[:90]}"):
                    st.markdown(
                        f'<div class="safes-answer" style="margin: 0;">'
                        f'{item.get("answer", "")[:500]}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f"""
                        <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px;">
                          <span class="safes-badge">
                            {item.get('bloom_level', 'understand')}
                          </span>
                          <span class="safes-badge">
                            {conf:.0%} confidence
                          </span>
                          <span class="safes-badge">
                            {item.get('citations_count', 0)} citations
                          </span>
                          <span class="safes-badge">
                            {item.get('response_time_ms', 0):.0f}ms
                          </span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            st.markdown(
                '<div class="safes-card" style="text-align: center; color: var(--stone);">'
                "No queries recorded yet.</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    render_section_header("System Health", "Vector store stats and document library")

    health = api_get("/health")
    docs = api_get("/documents")
    if _ok(health):
        h = health.json()
        vs = h.get("vector_store", {})
        col1, col2 = st.columns(2)
        col1.metric("API Status", h.get("status", "unknown").upper())
        col2.metric("Indexed Records", vs.get("records", 0))

    if _ok(docs):
        docs_list = docs.json().get("documents", [])
        if docs_list:
            st.markdown("**Document Library:**")
            for doc in docs_list:
                render_document_card(doc)


# =============================================================================
# MAIN
# =============================================================================


def get_doc_count() -> int:
    try:
        res = api_get("/documents")
        return len(res.json().get("documents", [])) if _ok(res) else 0
    except Exception:
        return 0


def get_query_count() -> int:
    try:
        res = api_get("/query/stats")
        return res.json().get("total_queries", 0) if _ok(res) else 0
    except Exception:
        return 0


def main() -> None:
    st.set_page_config(
        page_title="SAFES — AI Study Assistant",
        page_icon="S",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_styles()

    # Sidebar branding
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; padding: 12px 0 20px 0;">
              <div style="font-family: 'SF Pro Rounded', ui-rounded, system-ui, sans-serif;
                          font-size: 28px; font-weight: 500; color: #000000;
                          letter-spacing: -0.02em;">
                SAFES
              </div>
              <div style="font-size: 12px; color: #a3a3a3; text-transform: uppercase;
                          letter-spacing: 0.1em; font-weight: 400; margin-top: 2px;">
                Study Assistant
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

    sidebar_documents()

    # Hero
    render_hero(
        doc_count=get_doc_count(),
        query_count=get_query_count(),
        llm_model="GLM-5",
    )

    # Tabs — no emoji, clean text
    tabs = st.tabs(["Query", "Study Guide", "Compare", "Practice Test", "Analytics"])
    with tabs[0]:
        query_tab()
    with tabs[1]:
        study_guide_tab()
    with tabs[2]:
        compare_tab()
    with tabs[3]:
        practice_test_tab()
    with tabs[4]:
        analytics_tab()

    render_footer()


if __name__ == "__main__":
    main()
