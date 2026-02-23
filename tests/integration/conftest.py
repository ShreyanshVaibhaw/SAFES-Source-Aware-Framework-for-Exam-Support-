from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.fixture
def test_client():
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
