def test_study_guide_endpoint(test_client):
    response = test_client.post("/study/guide", json={"topics": ["RAG"], "level": "understand"})
    assert response.status_code == 200
    assert "guide" in response.json()


def test_practice_test_endpoint(test_client):
    response = test_client.post(
        "/study/practice-test",
        json={"topics": ["RAG"], "difficulty": "medium", "num_questions": 3},
    )
    assert response.status_code == 200
    assert len(response.json()["questions"]) == 3


def test_key_concepts_endpoint(test_client):
    response = test_client.get("/study/key-concepts")
    assert response.status_code == 200
    assert "concepts" in response.json()
