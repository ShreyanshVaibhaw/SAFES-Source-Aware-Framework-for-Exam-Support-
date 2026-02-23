"""Helper script to run backend + frontend for manual testing."""

from __future__ import annotations

import subprocess


def main() -> None:
    api = subprocess.Popen(["uvicorn", "src.api.main:app", "--reload", "--port", "8000"])
    ui = subprocess.Popen(["streamlit", "run", "frontend/app.py"])
    print("API: http://localhost:8000")
    print("Frontend: http://localhost:8501")
    input("Press Enter to stop services...")
    ui.terminate()
    api.terminate()


if __name__ == "__main__":
    main()
