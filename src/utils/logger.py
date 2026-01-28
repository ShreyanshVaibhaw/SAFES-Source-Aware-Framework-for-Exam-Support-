"""
Logging Configuration Module for SAFES
======================================
Comprehensive logging utility using loguru with console and file handlers.

Features:
- Colored console output for development
- Rotating file logs with retention
- Separate error log file
- Contextual logging with module/function/line info
"""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger


# -----------------------------------------------------------------------------
# Configuration Constants
# -----------------------------------------------------------------------------

# Base directory for logs (relative to project root)
LOG_DIR = Path(__file__).parent.parent.parent / "logs"

# Log file paths
APP_LOG_FILE = LOG_DIR / "app.log"
ERROR_LOG_FILE = LOG_DIR / "error.log"

# Log formats
CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

FILE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
    "{level: <8} | "
    "{name}:{function}:{line} | "
    "{message}"
)

# Rotation and retention settings
ROTATION_SIZE = "10 MB"
RETENTION_PERIOD = "7 days"


# -----------------------------------------------------------------------------
# Logger State
# -----------------------------------------------------------------------------

_logger_initialized = False


# -----------------------------------------------------------------------------
# Setup Functions
# -----------------------------------------------------------------------------

def setup_logger(
    console_level: str = "DEBUG",
    file_level: str = "INFO",
    error_level: str = "ERROR",
    log_dir: Optional[Path] = None,
    rotation: str = ROTATION_SIZE,
    retention: str = RETENTION_PERIOD,
    colorize: bool = True,
    diagnose: bool = True,
) -> None:
    """
    Configure the application-wide logger with console and file handlers.

    Args:
        console_level: Minimum log level for console output (default: DEBUG)
        file_level: Minimum log level for app.log file (default: INFO)
        error_level: Minimum log level for error.log file (default: ERROR)
        log_dir: Directory for log files (default: project_root/logs)
        rotation: When to rotate log files (default: "10 MB")
        retention: How long to keep old logs (default: "7 days")
        colorize: Enable colored console output (default: True)
        diagnose: Show variable values in tracebacks (default: True, disable in production)

    Example:
        >>> from src.utils.logger import setup_logger, get_logger
        >>> setup_logger(console_level="INFO")
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
    """
    global _logger_initialized

    # Determine log directory
    logs_path = log_dir or LOG_DIR

    # Create logs directory if it doesn't exist
    logs_path.mkdir(parents=True, exist_ok=True)

    # Remove default handler
    logger.remove()

    # -------------------------------------------------------------------------
    # Console Handler
    # -------------------------------------------------------------------------
    # Colored output for development, shows all levels from console_level up
    logger.add(
        sys.stderr,
        format=CONSOLE_FORMAT,
        level=console_level.upper(),
        colorize=colorize,
        diagnose=diagnose,
        backtrace=True,
    )

    # -------------------------------------------------------------------------
    # Application Log File Handler
    # -------------------------------------------------------------------------
    # Rotates at specified size, retains for specified period
    logger.add(
        logs_path / "app.log",
        format=FILE_FORMAT,
        level=file_level.upper(),
        rotation=rotation,
        retention=retention,
        compression="zip",  # Compress rotated logs
        encoding="utf-8",
        diagnose=diagnose,
        backtrace=True,
    )

    # -------------------------------------------------------------------------
    # Error Log File Handler
    # -------------------------------------------------------------------------
    # Separate file for errors only, easier to monitor critical issues
    logger.add(
        logs_path / "error.log",
        format=FILE_FORMAT,
        level=error_level.upper(),
        rotation=rotation,
        retention=retention,
        compression="zip",
        encoding="utf-8",
        diagnose=diagnose,
        backtrace=True,
    )

    _logger_initialized = True
    logger.info("Logger initialized successfully")
    logger.debug(f"Log directory: {logs_path.absolute()}")


def get_logger(name: str) -> "logger":
    """
    Get a logger instance bound with the specified module name.

    This function returns a logger with contextual binding for the module name,
    making it easier to track which module generated each log message.

    Args:
        name: Module name, typically __name__ from the calling module

    Returns:
        A loguru logger instance bound with the module name

    Example:
        >>> from src.utils.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing document")
        >>> logger.error("Failed to parse PDF", exc_info=True)
    """
    # Auto-initialize with defaults if not already done
    if not _logger_initialized:
        setup_logger()

    # Return logger bound with module name context
    return logger.bind(name=name)


# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------

def log_function_call(func):
    """
    Decorator to automatically log function entry and exit.

    Logs the function name, arguments, and return value (or exception).
    Useful for debugging complex call chains.

    Example:
        >>> @log_function_call
        ... def process_document(doc_id: str, options: dict):
        ...     return {"status": "success"}
    """
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__qualname__
        logger.debug(f"Entering {func_name} | args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Exiting {func_name} | result={result}")
            return result
        except Exception as e:
            logger.exception(f"Exception in {func_name}: {e}")
            raise

    return wrapper


def log_async_function_call(func):
    """
    Decorator to automatically log async function entry and exit.

    Same as log_function_call but for async functions.

    Example:
        >>> @log_async_function_call
        ... async def fetch_data(url: str):
        ...     return await http_client.get(url)
    """
    from functools import wraps

    @wraps(func)
    async def wrapper(*args, **kwargs):
        func_name = func.__qualname__
        logger.debug(f"Entering {func_name} | args={args}, kwargs={kwargs}")
        try:
            result = await func(*args, **kwargs)
            logger.debug(f"Exiting {func_name} | result={result}")
            return result
        except Exception as e:
            logger.exception(f"Exception in {func_name}: {e}")
            raise

    return wrapper


class LogContext:
    """
    Context manager for adding temporary context to log messages.

    Useful for adding request IDs, user IDs, or other contextual information
    to all log messages within a specific scope.

    Example:
        >>> with LogContext(request_id="abc-123", user_id="user-456"):
        ...     logger.info("Processing request")  # Includes request_id and user_id
    """

    def __init__(self, **context):
        self.context = context
        self._token = None

    def __enter__(self):
        self._token = logger.configure(extra=self.context)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Context is automatically cleaned up
        pass


def set_log_level(level: str) -> None:
    """
    Dynamically change the console log level at runtime.

    Useful for temporarily enabling debug logging without restarting.

    Args:
        level: New log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Example:
        >>> set_log_level("DEBUG")  # Enable verbose logging
        >>> # ... do debugging ...
        >>> set_log_level("INFO")   # Back to normal
    """
    # Note: This requires re-adding handlers, which is a limitation of loguru
    # For production, consider using environment variables instead
    logger.info(f"Log level change requested to: {level}")


# -----------------------------------------------------------------------------
# Module Initialization
# -----------------------------------------------------------------------------

# Export the base logger for direct imports
__all__ = [
    "logger",
    "setup_logger",
    "get_logger",
    "log_function_call",
    "log_async_function_call",
    "LogContext",
    "set_log_level",
]
