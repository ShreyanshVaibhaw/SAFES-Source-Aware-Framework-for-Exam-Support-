#!/usr/bin/env python3
"""
SAFES Setup Verification Script
================================
Verifies that all dependencies are installed correctly and configuration is valid.

Run: python scripts/verify_setup.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_status(name: str, status: bool, version: str = "") -> None:
    """Print status with checkmark or X."""
    icon = "[OK]" if status else "[FAIL]"
    version_str = f" (v{version})" if version else ""
    print(f"  {icon} {name}{version_str}")


def check_core_imports() -> bool:
    """Check that all core libraries can be imported."""
    print_header("CORE LIBRARY IMPORTS")
    all_ok = True

    libraries = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("streamlit", "Streamlit"),
        ("pydantic", "Pydantic"),
        ("yaml", "PyYAML"),
    ]

    for module, name in libraries:
        try:
            lib = __import__(module)
            version = getattr(lib, "__version__", "unknown")
            print_status(name, True, version)
        except ImportError as e:
            print_status(f"{name} - {e}", False)
            all_ok = False

    return all_ok


def check_document_processing() -> bool:
    """Check document processing libraries."""
    print_header("DOCUMENT PROCESSING")
    all_ok = True

    libraries = [
        ("pypdf", "PyPDF"),
        ("pdfplumber", "PDFPlumber"),
        ("docx", "python-docx"),
    ]

    for module, name in libraries:
        try:
            lib = __import__(module)
            version = getattr(lib, "__version__", "unknown")
            print_status(name, True, version)
        except ImportError as e:
            print_status(f"{name} - {e}", False)
            all_ok = False

    return all_ok


def check_vector_and_embeddings() -> bool:
    """Check vector database and embedding libraries."""
    print_header("VECTOR DATABASE & EMBEDDINGS")
    all_ok = True

    # ChromaDB
    try:
        import chromadb
        print_status("ChromaDB", True, chromadb.__version__)
    except ImportError as e:
        print_status(f"ChromaDB - {e}", False)
        all_ok = False

    # FAISS
    try:
        import faiss
        print_status("FAISS-CPU", True, "installed")
    except ImportError as e:
        print_status(f"FAISS-CPU - {e}", False)
        all_ok = False

    # Sentence Transformers
    try:
        import sentence_transformers
        print_status("Sentence-Transformers", True, sentence_transformers.__version__)
    except ImportError as e:
        print_status(f"Sentence-Transformers - {e}", False)
        all_ok = False

    return all_ok


def check_llm_libraries() -> bool:
    """Check LLM integration libraries."""
    print_header("LLM INTEGRATION")
    all_ok = True

    # OpenAI
    try:
        import openai
        print_status("OpenAI", True, openai.__version__)
    except ImportError as e:
        print_status(f"OpenAI - {e}", False)
        all_ok = False

    # LangChain Core (new package structure)
    try:
        import langchain_core
        print_status("LangChain-Core", True, langchain_core.__version__)
    except ImportError as e:
        print_status(f"LangChain-Core - {e}", False)
        all_ok = False

    # LangChain Community
    try:
        import langchain_community
        print_status("LangChain-Community", True, langchain_community.__version__)
    except ImportError as e:
        print_status(f"LangChain-Community - {e}", False)
        all_ok = False

    # LangChain OpenAI
    try:
        import langchain_openai
        from importlib.metadata import version
        lc_openai_version = version("langchain-openai")
        print_status("LangChain-OpenAI", True, lc_openai_version)
    except ImportError as e:
        print_status(f"LangChain-OpenAI - {e}", False)
        all_ok = False

    # Tiktoken
    try:
        import tiktoken
        print_status("Tiktoken", True, tiktoken.__version__)
    except ImportError as e:
        print_status(f"Tiktoken - {e}", False)
        all_ok = False

    return all_ok


def check_nlp_libraries() -> bool:
    """Check NLP libraries."""
    print_header("NLP LIBRARIES")
    all_ok = True

    # NLTK
    try:
        import nltk
        print_status("NLTK", True, nltk.__version__)
    except ImportError as e:
        print_status(f"NLTK - {e}", False)
        all_ok = False

    # spaCy
    try:
        import spacy
        print_status("spaCy", True, spacy.__version__)

        # Check if model is installed
        try:
            nlp = spacy.load("en_core_web_sm")
            print_status("spaCy Model (en_core_web_sm)", True, "loaded")
        except OSError:
            print_status("spaCy Model (en_core_web_sm) - not installed", False)
            print("    Run: python -m spacy download en_core_web_sm")
            all_ok = False
    except ImportError as e:
        print_status(f"spaCy - {e}", False)
        all_ok = False

    return all_ok


def check_utilities() -> bool:
    """Check utility libraries."""
    print_header("UTILITIES")
    all_ok = True

    libraries = [
        ("loguru", "Loguru"),
        ("tenacity", "Tenacity"),
        ("dotenv", "python-dotenv"),
        ("httpx", "HTTPX"),
    ]

    for module, name in libraries:
        try:
            lib = __import__(module)
            version = getattr(lib, "__version__", "installed")
            print_status(name, True, version)
        except ImportError as e:
            print_status(f"{name} - {e}", False)
            all_ok = False

    return all_ok


def check_configuration() -> bool:
    """Check configuration loading."""
    print_header("CONFIGURATION")
    all_ok = True

    # Check config file exists
    config_path = project_root / "configs" / "config.yaml"
    if config_path.exists():
        print_status("config.yaml exists", True)
    else:
        print_status("config.yaml missing", False)
        all_ok = False
        return all_ok

    # Try loading configuration
    try:
        from src.utils.config import config
        print_status("ConfigLoader initialized", True)

        # Test dot notation access
        chunk_size = config.get("document_processing.chunk_size")
        print_status(f"Config access works (chunk_size={chunk_size})", True)

        # Check environment
        print_status(f"Environment: {config.environment}", True)
        print_status(f"Debug mode: {config.is_debug}", True)

    except Exception as e:
        print_status(f"Config loading failed - {e}", False)
        all_ok = False

    return all_ok


def check_openai_api_key() -> bool:
    """Check if OpenAI API key is configured."""
    print_header("API KEY CHECK")

    import os
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        # Mask the key for security
        masked = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print_status(f"OPENAI_API_KEY is set ({masked})", True)
        return True
    else:
        print_status("OPENAI_API_KEY not set", False)
        print("    Set it in configs/.env or as environment variable")
        print("    LLM features will not work without it")
        return False  # Return False but don't fail the whole setup


def check_logger() -> bool:
    """Test the logger configuration."""
    print_header("LOGGER TEST")

    try:
        from src.utils.logger import setup_logger, get_logger

        # Setup logger with minimal output for test
        setup_logger(console_level="WARNING")
        logger = get_logger(__name__)

        print_status("Logger setup successful", True)
        print_status("Log directory: logs/", True)

        # Verify log directory exists
        log_dir = project_root / "logs"
        if log_dir.exists():
            print_status("Log directory exists", True)
        else:
            print_status("Log directory will be created on first log", True)

        return True
    except Exception as e:
        print_status(f"Logger setup failed - {e}", False)
        return False


def check_directories() -> bool:
    """Check that required directories exist."""
    print_header("DIRECTORY STRUCTURE")
    all_ok = True

    directories = [
        "src",
        "src/api",
        "src/core",
        "src/services",
        "src/models",
        "src/utils",
        "frontend",
        "configs",
        "data/uploads",
        "data/processed",
        "data/vectordb",
        "logs",
        "tests",
    ]

    for dir_name in directories:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print_status(dir_name, True)
        else:
            print_status(f"{dir_name} - missing", False)
            all_ok = False

    return all_ok


def main():
    """Run all verification checks."""
    print("\n" + "=" * 60)
    print(" SAFES - Setup Verification")
    print(" Source-Aware Framework for Exam Support")
    print("=" * 60)
    print(f"\nProject Root: {project_root}")
    print(f"Python Version: {sys.version.split()[0]}")

    results = []

    # Run all checks
    results.append(("Core Libraries", check_core_imports()))
    results.append(("Document Processing", check_document_processing()))
    results.append(("Vector & Embeddings", check_vector_and_embeddings()))
    results.append(("LLM Integration", check_llm_libraries()))
    results.append(("NLP Libraries", check_nlp_libraries()))
    results.append(("Utilities", check_utilities()))
    results.append(("Directories", check_directories()))
    results.append(("Configuration", check_configuration()))
    results.append(("Logger", check_logger()))

    # API key check (warning only, doesn't fail setup)
    check_openai_api_key()

    # Summary
    print_header("VERIFICATION SUMMARY")

    all_passed = True
    for name, passed in results:
        print_status(name, passed)
        if not passed:
            all_passed = False

    print("\n" + "-" * 60)
    if all_passed:
        print(" [SUCCESS] All checks passed! Setup is complete.")
        print(" You can now start developing the AI Study Assistant.")
        print("-" * 60 + "\n")
        return 0
    else:
        print(" [WARNING] Some checks failed. Review the output above.")
        print("-" * 60 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
