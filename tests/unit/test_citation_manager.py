from src.core.citation_manager import CitationManager


def test_citation_registration_and_formatting():
    manager = CitationManager()
    cites = manager.register_citations(
        [
            {
                "id": "chunk1",
                "document_id": "doc1",
                "metadata": {"page_number": 2, "section_title": "Intro"},
                "score": 0.9,
            }
        ]
    )
    assert len(cites) == 1
    text = manager.enrich_response("Answer [1]", cites, mode="footnote")
    assert "Sources:" in text
    assert manager.verify_citation_references(text, cites)
