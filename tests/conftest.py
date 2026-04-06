import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def test_env(tmp_path: Path):
    os.environ.setdefault("ENVIRONMENT", "test")
    os.environ.setdefault("LOG_LEVEL", "ERROR")
    os.environ.setdefault("SAFES_USE_SENTENCE_TRANSFORMERS", "0")
    # Use temp directory for vector store persistence during tests
    os.environ["CHROMA_PERSIST_DIR"] = str(tmp_path / "vectordb")
    yield
    # Clean up env var after test
    os.environ.pop("CHROMA_PERSIST_DIR", None)
