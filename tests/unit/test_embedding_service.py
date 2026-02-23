from src.services.embedding_service import EmbeddingService


def test_generate_embedding_has_consistent_dimension():
    service = EmbeddingService()
    vec = service.generate_embedding("test sentence")
    assert isinstance(vec, list)
    assert len(vec) == service.embedding_dim


def test_batch_embeddings_match_input_count():
    service = EmbeddingService()
    vectors = service.generate_embeddings(["a", "b", "c"])
    assert len(vectors) == 3
    assert all(len(v) == service.embedding_dim for v in vectors)


def test_cosine_similarity_range():
    service = EmbeddingService()
    a = service.generate_embedding("machine learning")
    b = service.generate_embedding("machine learning")
    sim = service.cosine_similarity(a, b)
    assert 0.0 <= sim <= 1.0
    assert sim > 0.95
