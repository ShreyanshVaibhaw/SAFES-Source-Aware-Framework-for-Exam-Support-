def test_compare_topics_endpoint(test_client):
    response = test_client.post(
        "/study/compare",
        json={"topic_a": "TCP", "topic_b": "UDP"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["topic_a"] == "TCP"
    assert data["topic_b"] == "UDP"
    assert "comparison" in data


def test_compare_topics_with_uploaded_doc(test_client, sample_text_file):
    # Upload document first
    with sample_text_file.open("rb") as fp:
        upload = test_client.post(
            "/documents/upload", files={"file": ("sample.txt", fp, "text/plain")}
        )
    assert upload.status_code == 200

    response = test_client.post(
        "/study/compare",
        json={"topic_a": "photosynthesis", "topic_b": "energy"},
    )
    assert response.status_code == 200
    assert "comparison" in response.json()
