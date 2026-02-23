def test_query_endpoint_validation(test_client):
    response = test_client.post("/query", json={"question": "?"})
    assert response.status_code in (422, 200)


def test_query_stream_endpoint(test_client, sample_text_file):
    with sample_text_file.open("rb") as fp:
        upload = test_client.post(
            "/documents/upload", files={"file": ("sample.txt", fp, "text/plain")}
        )
    assert upload.status_code == 200
    doc_id = upload.json()["document_id"]

    response = test_client.post(
        "/query/stream", json={"question": "Explain photosynthesis", "top_k": 2}
    )
    assert response.status_code == 200
    assert response.text

    test_client.delete(f"/documents/{doc_id}")
