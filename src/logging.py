"""Logging configuration for FileLock."""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

from .config import TEMP_DIR

# Create logs directory
LOGS_DIR = TEMP_DIR.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Log file settings
LOG_FILE = LOGS_DIR / "filelock.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5MB
BACKUP_COUNT = 3

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Set up a logger with file and console handlers.

    Args:
        name: Name of the logger
        level: Optional logging level (defaults to INFO if not specified)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Set default level if not specified
    if level is None:
        level = logging.INFO
    logger.setLevel(level)

    # Avoid adding handlers if they already exist
    if not logger.handlers:
        # Create formatters
        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

        # File handler (with rotation)
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


# Create default logger
default_logger = setup_logger("filelock")


def log_operation(
    logger: logging.Logger, operation: str, file_path: Path, **kwargs
) -> None:
    """Log a file operation with relevant details.

    Args:
        logger: Logger instance to use
        operation: Type of operation (e.g., 'encrypt', 'decrypt', 'compress')
        file_path: Path to the file being operated on
        **kwargs: Additional key-value pairs to log
    """
    log_data = {
        "operation": operation,
        "file": str(file_path),
        "size": file_path.stat().st_size if file_path.exists() else 0,
        **kwargs,
    }
    logger.info(f"File operation: {log_data}")


def log_error(
    logger: logging.Logger, error: Exception, operation: str, file_path: Path
) -> None:
    """Log an error that occurred during a file operation.

    Args:
        logger: Logger instance to use
        error: Exception that occurred
        operation: Type of operation during which the error occurred
        file_path: Path to the file being operated on
    """
    logger.error(
        f"Error during {operation} operation on {file_path}: {str(error)}",
        exc_info=True,
    )
