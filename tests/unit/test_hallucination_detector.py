from src.core.hallucination_detector import HallucinationDetector


def test_grounded_answer_scores_higher():
    detector = HallucinationDetector()
    chunks = [{"content": "Newton formulated three laws of motion."}]
    grounded = detector.detect("Newton formulated three laws of motion.", chunks, True)
    ungrounded = detector.detect("Newton made a fourth law in quantum space.", chunks, False)
    assert grounded["confidence"] > ungrounded["confidence"]
