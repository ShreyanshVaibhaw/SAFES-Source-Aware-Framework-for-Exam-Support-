from src.core.blooms_taxonomy import BloomsLevel, BloomsTaxonomyService


def test_detect_level():
    service = BloomsTaxonomyService()
    level = service.detect_level("Compare TCP and UDP for latency")
    assert level in BloomsLevel


def test_generate_practice_questions():
    service = BloomsTaxonomyService()
    questions = service.generate_practice_questions("Binary Trees", "analyze")
    assert questions
