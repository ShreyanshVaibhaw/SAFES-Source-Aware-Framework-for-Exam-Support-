def test_health_endpoint(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_document_upload_and_query_flow(test_client, sample_text_file):
    with sample_text_file.open("rb") as fp:
        upload = test_client.post(
            "/documents/upload", files={"file": ("sample.txt", fp, "text/plain")}
        )
    assert upload.status_code == 200, upload.text
    document_id = upload.json()["document_id"]

    query = test_client.post(
        "/query",
        json={
            "question": "What does photosynthesis do?",
            "top_k": 3,
            "check_hallucination": True,
            "include_citations": True,
        },
    )
    assert query.status_code == 200, query.text
    payload = query.json()
    assert "answer" in payload
    assert payload["citations"] is not None

    chunks = test_client.get(f"/documents/{document_id}/chunks")
    assert chunks.status_code == 200
    assert chunks.json()["chunks"]

    delete_res = test_client.delete(f"/documents/{document_id}")
    assert delete_res.status_code == 200
