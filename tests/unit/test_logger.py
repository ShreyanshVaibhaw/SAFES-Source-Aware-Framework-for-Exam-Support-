from pathlib import Path

from src.utils.logger import get_logger, log_function_call, setup_logger


def test_setup_logger_creates_log_dir(tmp_path: Path):
    setup_logger(log_dir=tmp_path)
    logger = get_logger(__name__)
    logger.info("test log line")
    assert (tmp_path / "app.log").exists()
    assert (tmp_path / "error.log").exists()


def test_log_function_decorator():
    @log_function_call
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5
