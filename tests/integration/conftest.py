import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.api.main import create_app


@pytest.fixture
def test_client(tmp_path: Path):
    # Each test gets its own vector store directory
    os.environ["CHROMA_PERSIST_DIR"] = str(tmp_path / "vectordb")
    app = create_app()
    with TestClient(app) as client:
        yield client


@pytest.fixture
def sample_text_file(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text(
        "Photosynthesis converts light energy into chemical energy in plants.",
        encoding="utf-8",
    )
    return file_path
