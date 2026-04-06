"""NLP utilities wrapping spaCy and NLTK with graceful fallback."""

from __future__ import annotations

import re
from typing import Dict, List, Optional

from src.utils.logger import get_logger

# Lazy-load heavy NLP libraries
_spacy_nlp = None
_nltk_ready = False


def _load_spacy():
    global _spacy_nlp
    if _spacy_nlp is not None:
        return _spacy_nlp
    try:
        import spacy
        _spacy_nlp = spacy.load("en_core_web_sm")
    except Exception:
        _spacy_nlp = None
    return _spacy_nlp


def _load_nltk():
    global _nltk_ready
    if _nltk_ready:
        return True
    try:
        import nltk
        nltk.data.find("tokenizers/punkt_tab")
        _nltk_ready = True
    except Exception:
        try:
            import nltk
            nltk.download("punkt_tab", quiet=True)
            nltk.download("stopwords", quiet=True)
            _nltk_ready = True
        except Exception:
            _nltk_ready = False
    return _nltk_ready


STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "to", "of", "for", "in",
    "on", "and", "or", "with", "that", "this", "it", "be", "as", "at", "by",
    "from", "not", "but", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "can", "shall", "so", "if",
    "then", "than", "when", "where", "which", "who", "whom", "what", "how",
    "all", "each", "every", "both", "few", "more", "most", "other", "some",
    "such", "no", "nor", "only", "own", "same", "too", "very", "just",
    "about", "above", "after", "again", "also", "any", "because", "been",
    "before", "being", "between", "during", "further", "here", "into",
    "its", "my", "our", "out", "over", "these", "those", "through", "under",
    "until", "up", "while", "your",
}


class NLPService:
    """NLP utilities with graceful degradation when libraries are unavailable."""

    def __init__(self) -> None:
        self.logger = get_logger(__name__)
        self._spacy = _load_spacy()
        self._nltk_ok = _load_nltk()

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        if self._nltk_ok:
            try:
                from nltk.tokenize import word_tokenize
                return word_tokenize(text)
            except Exception:
                pass
        return re.findall(r"[a-zA-Z0-9]+(?:'[a-zA-Z]+)?", text)

    def lemmatize(self, text: str) -> List[str]:
        """Lemmatize text, returning list of lemma strings."""
        if self._spacy is not None:
            try:
                doc = self._spacy(text[:100000])
                return [token.lemma_.lower() for token in doc if not token.is_punct]
            except Exception:
                pass
        return [w.lower() for w in self.tokenize(text)]

    def extract_keywords(self, text: str, top_k: int = 20) -> List[str]:
        """Extract significant keywords from text by frequency."""
        tokens = self.lemmatize(text)
        filtered = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]
        freq: Dict[str, int] = {}
        for t in filtered:
            freq[t] = freq.get(t, 0) + 1
        ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in ranked[:top_k]]

    def sentence_split(self, text: str) -> List[str]:
        """Split text into sentences."""
        if self._spacy is not None:
            try:
                doc = self._spacy(text[:100000])
                return [sent.text.strip() for sent in doc.sents if sent.text.strip()]
            except Exception:
                pass
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

    def extract_entities(self, text: str) -> List[Dict]:
        """Extract named entities from text."""
        if self._spacy is not None:
            try:
                doc = self._spacy(text[:100000])
                return [
                    {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char}
                    for ent in doc.ents
                ]
            except Exception:
                pass
        return []

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stopwords from a token list."""
        return [t for t in tokens if t.lower() not in STOP_WORDS]
