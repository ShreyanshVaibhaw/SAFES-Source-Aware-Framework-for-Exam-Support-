"""Streamlit frontend for SAFES."""

from __future__ import annotations

from typing import List

import requests
import streamlit as st

from frontend.components.ui_components import (
    init_styles,
    render_citations,
    render_confidence_meter,
    render_document_card,
    render_section_header,
)

API_URL = st.secrets.get("API_URL", "http://localhost:8000")


def api_get(path: str):
    return requests.get(f"{API_URL}{path}", timeout=60)


def api_post(path: str, payload=None, files=None, data=None):
    return requests.post(f"{API_URL}{path}", json=payload, files=files, data=data, timeout=120)


def api_delete(path: str):
    return requests.delete(f"{API_URL}{path}", timeout=60)


def sidebar_documents() -> None:
    st.sidebar.header("Documents")
    uploaded = st.sidebar.file_uploader(
        "Upload PDF/DOCX/TXT/MD", type=["pdf", "docx", "txt", "md"], accept_multiple_files=False
    )
    if uploaded and st.sidebar.button("Upload"):
        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type or "application/octet-stream")}
        res = api_post("/documents/upload", files=files)
        if res.ok:
            st.sidebar.success("Document uploaded and indexed.")
        else:
            st.sidebar.error(res.text)

    docs_res = api_get("/documents")
    if docs_res.ok:
        docs = docs_res.json().get("documents", [])
        st.sidebar.caption(f"{len(docs)} document(s) indexed")
        for doc in docs:
            if st.sidebar.button(f"Delete {doc['filename']}", key=f"delete-{doc['document_id']}"):
                delete_res = api_delete(f"/documents/{doc['document_id']}")
                if delete_res.ok:
                    st.sidebar.success(f"Deleted {doc['filename']}")
                    st.rerun()
                else:
                    st.sidebar.error(delete_res.text)


def query_tab() -> None:
    render_section_header("Ask a Question", "Grounded answers from uploaded materials.")
    question = st.text_area("Question", placeholder="Explain photosynthesis for exam revision")
    bloom = st.selectbox(
        "Bloom level",
        ["auto", "remember", "understand", "apply", "analyze", "evaluate", "create"],
        index=1,
    )
    top_k = st.slider("Top-K chunks", min_value=1, max_value=10, value=5)
    include_citations = st.checkbox("Include citations", value=True)
    check_hall = st.checkbox("Hallucination check", value=True)

    if st.button("Get Answer"):
        payload = {
            "question": question,
            "bloom_level": None if bloom == "auto" else bloom,
            "top_k": top_k,
            "include_citations": include_citations,
            "check_hallucination": check_hall,
        }
        res = api_post("/query", payload=payload)
        if not res.ok:
            st.error(res.text)
            return
        data = res.json()
        st.markdown("### Answer")
        st.write(data["answer"])
        render_confidence_meter(data.get("confidence", 0.0))
        st.caption(f"Bloom level: {data.get('bloom_level')}")
        render_citations(data.get("citations", []))
        if data.get("practice_questions"):
            st.markdown("### Practice Questions")
            for item in data["practice_questions"]:
                st.markdown(f"- {item}")


def study_guide_tab() -> None:
    render_section_header("Study Guide")
    topics_raw = st.text_input("Topics (comma-separated)", value="core concepts")
    level = st.selectbox("Level", ["remember", "understand", "apply", "analyze", "evaluate", "create"], index=1)
    if st.button("Generate Guide"):
        topics = [t.strip() for t in topics_raw.split(",") if t.strip()]
        res = api_post("/study/guide", payload={"topics": topics, "level": level})
        if res.ok:
            guide = res.json().get("guide", "")
            st.markdown(guide)
            st.download_button("Download Guide", guide, file_name="study_guide.md")
        else:
            st.error(res.text)


def compare_tab() -> None:
    render_section_header("Compare Topics", "Compare two topics from your uploaded materials.")
    col1, col2 = st.columns(2)
    topic_a = col1.text_input("Topic A", placeholder="e.g., TCP")
    topic_b = col2.text_input("Topic B", placeholder="e.g., UDP")
    if st.button("Compare"):
        if not topic_a or not topic_b:
            st.warning("Please enter both topics.")
            return
        res = api_post("/study/compare", payload={"topic_a": topic_a, "topic_b": topic_b})
        if res.ok:
            data = res.json()
            st.markdown(data.get("comparison", ""))
            st.caption(f"Sources used: {data.get('sources_a', 0)} for {topic_a}, {data.get('sources_b', 0)} for {topic_b}")
        else:
            st.error(res.text)


def practice_test_tab() -> None:
    render_section_header("Practice Test")
    topics_raw = st.text_input("Topics", value="revision")
    difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], index=1)
    num_questions = st.slider("Number of questions", 1, 20, 5)
    if st.button("Generate Practice Test"):
        topics: List[str] = [t.strip() for t in topics_raw.split(",") if t.strip()]
        res = api_post(
            "/study/practice-test",
            payload={"topics": topics, "difficulty": difficulty, "num_questions": num_questions},
        )
        if res.ok:
            payload = res.json()
            for question in payload.get("questions", []):
                st.markdown(f"**{question['question']}**")
                st.caption(f"Hint: {question['hint']}")
        else:
            st.error(res.text)


def analytics_tab() -> None:
    render_section_header("Analytics")

    # Query history stats
    stats_res = api_get("/query/stats")
    if stats_res.ok:
        stats = stats_res.json()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Queries", stats.get("total_queries", 0))
        col2.metric("Avg Confidence", f"{stats.get('avg_confidence', 0):.0%}")
        col3.metric("Avg Response Time", f"{stats.get('avg_response_time_ms', 0):.0f}ms")

        bloom_data = stats.get("queries_by_bloom_level", {})
        if bloom_data:
            st.markdown("**Queries by Bloom Level:**")
            for level, count in bloom_data.items():
                st.caption(f"  {level}: {count}")

    # Query history table
    st.markdown("---")
    render_section_header("Query History")
    history_res = api_get("/query/history?limit=10")
    if history_res.ok:
        history = history_res.json().get("history", [])
        if history:
            for item in history:
                with st.expander(f"{item.get('question', '')[:80]}..."):
                    st.write(item.get("answer", "")[:300])
                    st.caption(
                        f"Bloom: {item.get('bloom_level')} | "
                        f"Confidence: {item.get('confidence', 0):.0%} | "
                        f"Citations: {item.get('citations_count', 0)} | "
                        f"Time: {item.get('response_time_ms', 0):.0f}ms"
                    )
        else:
            st.info("No queries recorded yet.")

    # System health
    st.markdown("---")
    render_section_header("System Health")
    health = api_get("/health")
    docs = api_get("/documents")
    if health.ok:
        st.json(health.json())
    if docs.ok:
        for doc in docs.json().get("documents", []):
            render_document_card(doc)


def main() -> None:
    st.set_page_config(page_title="AI Study Assistant", layout="wide")
    init_styles()
    sidebar_documents()

    tabs = st.tabs(["Query", "Study Guide", "Compare Topics", "Practice Test", "Analytics"])
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


if __name__ == "__main__":
    main()
