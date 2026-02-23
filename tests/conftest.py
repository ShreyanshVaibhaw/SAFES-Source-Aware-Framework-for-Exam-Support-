import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def test_env(tmp_path: Path):
    os.environ.setdefault("ENVIRONMENT", "test")
    os.environ.setdefault("LOG_LEVEL", "ERROR")
    os.environ.setdefault("SAFES_USE_SENTENCE_TRANSFORMERS", "0")
    yield
