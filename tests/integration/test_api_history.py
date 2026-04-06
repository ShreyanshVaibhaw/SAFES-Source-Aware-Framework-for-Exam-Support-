def test_query_history_endpoint(test_client, sample_text_file):
    # Upload a document first
    with sample_text_file.open("rb") as fp:
        upload = test_client.post(
            "/documents/upload", files={"file": ("sample.txt", fp, "text/plain")}
        )
    assert upload.status_code == 200

    # Make a query (should be recorded in history)
    test_client.post("/query", json={"question": "What is photosynthesis?", "top_k": 3})

    # Check history
    history_res = test_client.get("/query/history")
    assert history_res.status_code == 200
    data = history_res.json()
    assert data["total"] >= 1
    assert len(data["history"]) >= 1


def test_query_stats_endpoint(test_client):
    stats_res = test_client.get("/query/stats")
    assert stats_res.status_code == 200
    data = stats_res.json()
    assert "total_queries" in data
    assert "avg_confidence" in data
