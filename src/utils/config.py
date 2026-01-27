"""
Configuration Management Module for SAFES
==========================================
Centralized configuration loader with support for YAML config files
and environment variables.

Features:
- Loads config.yaml with nested access via dot notation
- Environment variable loading from .env file
- Singleton pattern for single config instance
- Validation of required settings
- Type hints and clear error messages

Usage:
    from src.utils.config import config

    # Access nested values with dot notation
    chunk_size = config.get("document_processing.chunk_size")

    # Get entire sections
    llm_config = config.get_section("llm")

    # Access common properties directly
    api_key = config.openai_api_key
    is_debug = config.is_debug
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, TypeVar, Union

import yaml
from dotenv import load_dotenv


# Type variable for generic return types
T = TypeVar("T")


# -----------------------------------------------------------------------------
# Exceptions
# -----------------------------------------------------------------------------

class ConfigurationError(Exception):
    """Raised when there's a configuration-related error."""
    pass


class MissingConfigError(ConfigurationError):
    """Raised when a required configuration value is missing."""
    pass


class InvalidConfigError(ConfigurationError):
    """Raised when a configuration value is invalid."""
    pass


# -----------------------------------------------------------------------------
# Configuration Loader Class
# -----------------------------------------------------------------------------

class ConfigLoader:
    """
    Configuration loader with support for YAML files and environment variables.

    Implements singleton pattern to ensure configuration is loaded only once.
    Provides dot notation access to nested configuration values.

    Attributes:
        config_path: Path to the YAML configuration file
        _config: Internal dictionary holding all configuration values
        _env_loaded: Whether environment variables have been loaded

    Example:
        >>> config = ConfigLoader()
        >>> chunk_size = config.get("document_processing.chunk_size", default=500)
        >>> llm_settings = config.get_section("llm")
        >>> print(config.openai_api_key)
    """

    _instance: Optional["ConfigLoader"] = None
    _initialized: bool = False

    def __new__(cls, config_path: Optional[str] = None) -> "ConfigLoader":
        """
        Implement singleton pattern - return existing instance if available.

        Args:
            config_path: Optional path to config file (only used on first instantiation)

        Returns:
            The singleton ConfigLoader instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_path: Optional[str] = None) -> None:
        """
        Initialize the configuration loader.

        Loads the YAML configuration file and environment variables.
        Only performs initialization once due to singleton pattern.

        Args:
            config_path: Path to YAML config file. Defaults to "configs/config.yaml"

        Raises:
            ConfigurationError: If config file cannot be loaded
        """
        # Skip if already initialized (singleton)
        if ConfigLoader._initialized:
            return

        # Determine project root directory
        self._project_root = Path(__file__).parent.parent.parent

        # Set config path
        if config_path:
            self._config_path = Path(config_path)
        else:
            self._config_path = self._project_root / "configs" / "config.yaml"

        # Initialize internal state
        self._config: Dict[str, Any] = {}
        self._env_loaded: bool = False

        # Load configuration
        self._load_env()
        self._load_config()
        self._validate_required()

        ConfigLoader._initialized = True

    # -------------------------------------------------------------------------
    # Loading Methods
    # -------------------------------------------------------------------------

    def _load_env(self) -> None:
        """
        Load environment variables from .env file.

        Searches for .env file in configs/ directory and project root.
        Environment variables take precedence over config file values.
        """
        # Possible .env locations (in order of precedence)
        env_paths = [
            self._project_root / "configs" / ".env",
            self._project_root / ".env",
        ]

        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path)
                self._env_loaded = True
                break

    def _load_config(self) -> None:
        """
        Load configuration from YAML file.

        Raises:
            ConfigurationError: If config file doesn't exist or is invalid
        """
        if not self._config_path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {self._config_path}\n"
                f"Please ensure 'configs/config.yaml' exists."
            )

        try:
            with open(self._config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ConfigurationError(
                f"Invalid YAML in configuration file: {self._config_path}\n"
                f"Error: {e}"
            )
        except Exception as e:
            raise ConfigurationError(
                f"Failed to load configuration file: {self._config_path}\n"
                f"Error: {e}"
            )

    def _validate_required(self) -> None:
        """
        Validate that required configuration values are present.

        Checks for critical settings like API keys and raises clear
        errors if they're missing.

        Raises:
            MissingConfigError: If required configuration is missing
        """
        warnings = []

        # Check OpenAI API key (required for LLM features)
        if not self.openai_api_key:
            warnings.append(
                "OPENAI_API_KEY not set. LLM features will not work.\n"
                "Set it in configs/.env or as an environment variable."
            )

        # Log warnings but don't fail (allow app to start for testing)
        if warnings:
            # Import here to avoid circular dependency
            try:
                from src.utils.logger import logger
                for warning in warnings:
                    logger.warning(warning)
            except ImportError:
                for warning in warnings:
                    print(f"WARNING: {warning}")

    # -------------------------------------------------------------------------
    # Access Methods
    # -------------------------------------------------------------------------

    def get(
        self,
        key: str,
        default: Optional[T] = None,
        required: bool = False
    ) -> Union[Any, T]:
        """
        Get a configuration value using dot notation.

        Supports nested keys like "document_processing.chunk_size".
        Environment variables take precedence over config file values.

        Args:
            key: Configuration key in dot notation (e.g., "llm.model")
            default: Default value if key not found
            required: If True, raises error when key is missing

        Returns:
            Configuration value or default

        Raises:
            MissingConfigError: If required=True and key is not found

        Example:
            >>> config.get("document_processing.chunk_size", default=500)
            500
            >>> config.get("llm.temperature", default=0.7)
            0.3
        """
        # First, check environment variable (with key converted to uppercase)
        env_key = key.upper().replace(".", "_")
        env_value = os.getenv(env_key)
        if env_value is not None:
            return self._convert_type(env_value)

        # Navigate through nested config
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                if required:
                    raise MissingConfigError(
                        f"Required configuration key not found: '{key}'"
                    )
                return default

        return value

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get an entire configuration section as a dictionary.

        Args:
            section: Section name (top-level key in config.yaml)

        Returns:
            Dictionary containing all values in the section

        Raises:
            MissingConfigError: If section doesn't exist

        Example:
            >>> llm_config = config.get_section("llm")
            >>> print(llm_config["model"])
            "gpt-3.5-turbo"
        """
        if section not in self._config:
            raise MissingConfigError(
                f"Configuration section not found: '{section}'"
            )
        return self._config[section].copy()

    def get_all(self) -> Dict[str, Any]:
        """
        Get the entire configuration as a dictionary.

        Returns:
            Complete configuration dictionary

        Note:
            Returns a copy to prevent accidental modification.
        """
        return self._config.copy()

    def _convert_type(self, value: str) -> Any:
        """
        Convert string environment variable to appropriate Python type.

        Args:
            value: String value from environment variable

        Returns:
            Converted value (bool, int, float, or original string)
        """
        # Boolean conversion
        if value.lower() in ("true", "yes", "1", "on"):
            return True
        if value.lower() in ("false", "no", "0", "off"):
            return False

        # Integer conversion
        try:
            return int(value)
        except ValueError:
            pass

        # Float conversion
        try:
            return float(value)
        except ValueError:
            pass

        # Return as string
        return value

    # -------------------------------------------------------------------------
    # Configuration Reload
    # -------------------------------------------------------------------------

    def reload(self) -> None:
        """
        Reload configuration from file.

        Useful for picking up configuration changes without restarting
        the application.

        Example:
            >>> config.reload()  # Refresh config from file
        """
        self._load_env()
        self._load_config()

    # -------------------------------------------------------------------------
    # Common Properties
    # -------------------------------------------------------------------------

    @property
    def openai_api_key(self) -> Optional[str]:
        """
        Get OpenAI API key from environment variable.

        Returns:
            API key string or None if not set
        """
        return os.getenv("OPENAI_API_KEY")

    @property
    def environment(self) -> str:
        """
        Get current environment (development/staging/production).

        Returns:
            Environment string, defaults to "development"
        """
        return os.getenv("ENVIRONMENT", "development").lower()

    @property
    def is_debug(self) -> bool:
        """
        Check if application is in debug mode.

        Returns:
            True if debug mode is enabled
        """
        # Check environment variable first
        debug_env = os.getenv("DEBUG")
        if debug_env is not None:
            return debug_env.lower() in ("true", "1", "yes", "on")

        # Fall back to config file
        return self.get("app.debug", default=False)

    @property
    def log_level(self) -> str:
        """
        Get logging level.

        Returns:
            Log level string (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        return os.getenv("LOG_LEVEL", self.get("logging.level", default="INFO")).upper()

    @property
    def project_root(self) -> Path:
        """
        Get the project root directory path.

        Returns:
            Path to project root
        """
        return self._project_root

    # -------------------------------------------------------------------------
    # Path Properties
    # -------------------------------------------------------------------------

    @property
    def upload_dir(self) -> Path:
        """Get path to upload directory."""
        path = os.getenv("UPLOAD_DIR", self.get("document_processing.upload_dir", "data/uploads"))
        return self._project_root / path

    @property
    def processed_dir(self) -> Path:
        """Get path to processed documents directory."""
        path = os.getenv("PROCESSED_DIR", self.get("document_processing.processed_dir", "data/processed"))
        return self._project_root / path

    @property
    def vectordb_dir(self) -> Path:
        """Get path to vector database directory."""
        path = os.getenv("CHROMA_PERSIST_DIR", self.get("vector_database.persist_directory", "data/vectordb"))
        return self._project_root / path

    @property
    def log_dir(self) -> Path:
        """Get path to logs directory."""
        return self._project_root / "logs"

    # -------------------------------------------------------------------------
    # LLM Properties
    # -------------------------------------------------------------------------

    @property
    def llm_model(self) -> str:
        """Get the configured LLM model name."""
        return self.get("llm.model", default="gpt-3.5-turbo")

    @property
    def llm_temperature(self) -> float:
        """Get the LLM temperature setting."""
        return self.get("llm.temperature", default=0.3)

    @property
    def llm_max_tokens(self) -> int:
        """Get the maximum tokens for LLM response."""
        return self.get("llm.max_tokens", default=1500)

    # -------------------------------------------------------------------------
    # Document Processing Properties
    # -------------------------------------------------------------------------

    @property
    def chunk_size(self) -> int:
        """Get text chunk size in tokens."""
        return self.get("document_processing.chunk_size", default=500)

    @property
    def chunk_overlap(self) -> int:
        """Get chunk overlap size in tokens."""
        return self.get("document_processing.chunk_overlap", default=50)

    @property
    def allowed_extensions(self) -> List[str]:
        """Get list of allowed file extensions."""
        return self.get("document_processing.allowed_extensions", default=[".pdf", ".docx", ".txt", ".md"])

    @property
    def max_file_size_mb(self) -> int:
        """Get maximum allowed file size in megabytes."""
        return self.get("document_processing.max_file_size_mb", default=50)

    # -------------------------------------------------------------------------
    # Retrieval Properties
    # -------------------------------------------------------------------------

    @property
    def retrieval_top_k(self) -> int:
        """Get number of chunks to retrieve."""
        return self.get("retrieval.top_k", default=5)

    @property
    def similarity_threshold(self) -> float:
        """Get minimum similarity threshold for retrieval."""
        return self.get("retrieval.similarity_threshold", default=0.7)

    # -------------------------------------------------------------------------
    # API Properties
    # -------------------------------------------------------------------------

    @property
    def api_host(self) -> str:
        """Get API server host."""
        return os.getenv("API_HOST", self.get("api.host", default="0.0.0.0"))

    @property
    def api_port(self) -> int:
        """Get API server port."""
        return int(os.getenv("API_PORT", self.get("api.port", default=8000)))

    # -------------------------------------------------------------------------
    # Magic Methods
    # -------------------------------------------------------------------------

    def __repr__(self) -> str:
        """String representation of ConfigLoader."""
        return (
            f"ConfigLoader(config_path='{self._config_path}', "
            f"env='{self.environment}', debug={self.is_debug})"
        )

    def __contains__(self, key: str) -> bool:
        """Check if a configuration key exists."""
        try:
            self.get(key, required=True)
            return True
        except MissingConfigError:
            return False


# -----------------------------------------------------------------------------
# Global Configuration Instance
# -----------------------------------------------------------------------------

def get_config(config_path: Optional[str] = None) -> ConfigLoader:
    """
    Get the global configuration instance.

    Factory function that returns the singleton ConfigLoader instance.
    Use this or the global `config` variable to access configuration.

    Args:
        config_path: Optional path to config file (only used on first call)

    Returns:
        The singleton ConfigLoader instance

    Example:
        >>> from src.utils.config import get_config
        >>> config = get_config()
        >>> print(config.llm_model)
    """
    return ConfigLoader(config_path)


# Create global config instance for easy importing
# Usage: from src.utils.config import config
config = get_config()


# -----------------------------------------------------------------------------
# Module Exports
# -----------------------------------------------------------------------------

__all__ = [
    "ConfigLoader",
    "ConfigurationError",
    "MissingConfigError",
    "InvalidConfigError",
    "get_config",
    "config",
]
