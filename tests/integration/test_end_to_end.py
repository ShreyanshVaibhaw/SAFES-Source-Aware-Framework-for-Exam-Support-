def test_full_user_journey(test_client, sample_text_file):
    with sample_text_file.open("rb") as fp:
        upload = test_client.post(
            "/documents/upload", files={"file": ("sample.txt", fp, "text/plain")}
        )
    assert upload.status_code == 200
    doc_id = upload.json()["document_id"]

    query = test_client.post("/query", json={"question": "Explain photosynthesis", "top_k": 5})
    assert query.status_code == 200

    guide = test_client.post(
        "/study/guide", json={"topics": ["photosynthesis"], "level": "understand"}
    )
    assert guide.status_code == 200

    practice = test_client.post(
        "/study/practice-test",
        json={"topics": ["photosynthesis"], "difficulty": "easy", "num_questions": 2},
    )
    assert practice.status_code == 200

    delete = test_client.delete(f"/documents/{doc_id}")
    assert delete.status_code == 200
