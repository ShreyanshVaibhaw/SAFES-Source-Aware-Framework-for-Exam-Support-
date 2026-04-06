from src.services.nlp_service import NLPService


def test_tokenize_returns_words():
    nlp = NLPService()
    tokens = nlp.tokenize("Hello world, this is a test!")
    assert "Hello" in tokens or "hello" in tokens
    assert len(tokens) >= 4


def test_lemmatize_returns_lowercase():
    nlp = NLPService()
    lemmas = nlp.lemmatize("Running dogs are playing")
    assert all(l == l.lower() for l in lemmas)
    assert len(lemmas) >= 2


def test_extract_keywords_filters_stopwords():
    nlp = NLPService()
    keywords = nlp.extract_keywords(
        "The quick brown fox jumps over the lazy dog. The fox is very quick.", top_k=5
    )
    assert "the" not in keywords
    assert len(keywords) > 0


def test_sentence_split():
    nlp = NLPService()
    sentences = nlp.sentence_split("First sentence. Second sentence! Third one?")
    assert len(sentences) >= 2


def test_remove_stopwords():
    nlp = NLPService()
    filtered = nlp.remove_stopwords(["the", "cat", "is", "on", "mat"])
    assert "the" not in filtered
    assert "cat" in filtered
    assert "mat" in filtered


def test_extract_entities_returns_list():
    nlp = NLPService()
    entities = nlp.extract_entities("Albert Einstein worked at Princeton University.")
    # May be empty if spaCy is not loaded, but should always return a list
    assert isinstance(entities, list)
