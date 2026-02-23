def test_documents_list_endpoint(test_client):
    response = test_client.get("/documents")
    assert response.status_code == 200
    assert "documents" in response.json()


def test_get_document_not_found(test_client):
    response = test_client.get("/documents/not_found")
    assert response.status_code == 404


def test_delete_document_not_found(test_client):
    response = test_client.delete("/documents/not_found")
    assert response.status_code == 404
