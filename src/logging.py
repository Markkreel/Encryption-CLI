"""Enhanced logging configuration for FileLock with security and performance features."""

import hashlib
import json
import logging
import os
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional, Union

from .config import TEMP_DIR

# Create logs directory
DEFAULT_LOGS_DIR = TEMP_DIR.parent / "logs"
DEFAULT_LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Default log format
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class PrivacyMode(Enum):
    """Privacy modes for logging sensitive information."""
    FULL = "full"
    REDACTED = "redacted"
    HASHED = "hashed"


class ErrorSeverity(Enum):
    """Error severity levels for enhanced error tracking."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RotationType(Enum):
    """Log rotation strategies."""
    SIZE = "size"
    TIME = "time"
    BOTH = "both"


@dataclass
class LogConfig:
    """Configuration for logging behavior."""
    log_dir: Path = field(default_factory=lambda: DEFAULT_LOGS_DIR)
    log_file: str = "filelock.log"
    max_size: int = 5 * 1024 * 1024  # 5MB
    backup_count: int = 3
    format: str = DEFAULT_LOG_FORMAT
    date_format: str = DEFAULT_DATE_FORMAT
    console_output: bool = True
    file_output: bool = True
    privacy_mode: PrivacyMode = PrivacyMode.FULL
    rotation_type: RotationType = RotationType.SIZE
    rotation_interval: str = "midnight"  # For time-based rotation
    structured_logging: bool = False
    compress_rotated: bool = True
    log_level: str = "INFO"
    
    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "LogConfig":
        """Create LogConfig from dictionary."""
        # Convert string enums to enum types
        if "privacy_mode" in config and isinstance(config["privacy_mode"], str):
            config["privacy_mode"] = PrivacyMode(config["privacy_mode"])
        if "rotation_type" in config and isinstance(config["rotation_type"], str):
            config["rotation_type"] = RotationType(config["rotation_type"])
        
        return cls(**{k: v for k, v in config.items() if k in cls.__annotations__})
    
    @classmethod
    def from_env(cls) -> "LogConfig":
        """Create LogConfig from environment variables."""
        config = cls()
        
        # Override with environment variables if present
        if log_level := os.getenv("FILELOCK_LOG_LEVEL"):
            config.log_level = log_level.upper()
        if privacy_mode := os.getenv("FILELOCK_PRIVACY_MODE"):
            config.privacy_mode = PrivacyMode(privacy_mode.lower())
        if console_output := os.getenv("FILELOCK_CONSOLE_OUTPUT"):
            config.console_output = console_output.lower() == "true"
        
        return config


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def __init__(self, privacy_mode: PrivacyMode = PrivacyMode.FULL):
        super().__init__()
        self.privacy_mode = privacy_mode
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, "operation_data"):
            # Sanitize paths in operation data
            op_data = record.operation_data.copy()
            if "file" in op_data:
                op_data["file"] = sanitize_path(Path(op_data["file"]), self.privacy_mode)
            log_obj.update(op_data)
        
        # Add exception info if present
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_obj)


class CompressingRotatingFileHandler(RotatingFileHandler):
    """RotatingFileHandler that compresses rotated files."""
    
    def __init__(self, *args, compress: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.compress = compress
    
    def doRollover(self):
        """Override to add compression after rotation."""
        super().doRollover()
        
        if self.compress and self.backupCount > 0:
            # Compress the newly rotated file
            import gzip
            import shutil
            
            # Find the most recent backup
            for i in range(1, self.backupCount + 1):
                sfn = self.rotation_filename(f"{self.baseFilename}.{i}")
                if os.path.exists(sfn) and not sfn.endswith('.gz'):
                    # Compress the file
                    with open(sfn, 'rb') as f_in:
                        with gzip.open(f"{sfn}.gz", 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    os.remove(sfn)


def sanitize_path(file_path: Path, privacy_mode: PrivacyMode = PrivacyMode.FULL) -> str:
    """Sanitize file paths based on privacy settings."""
    if privacy_mode == PrivacyMode.FULL:
        return str(file_path)
    elif privacy_mode == PrivacyMode.REDACTED:
        # Show only filename, not full path
        return f".../{file_path.name}"
    elif privacy_mode == PrivacyMode.HASHED:
        # Hash the full path for consistency tracking
        path_hash = hashlib.sha256(str(file_path).encode()).hexdigest()[:8]
        return f"file_{path_hash}"
    return str(file_path)


def create_file_handler(config: LogConfig) -> logging.Handler:
    """Create appropriate file handler based on configuration."""
    log_path = config.log_dir / config.log_file
    
    if config.rotation_type == RotationType.SIZE:
        handler = CompressingRotatingFileHandler(
            log_path,
            maxBytes=config.max_size,
            backupCount=config.backup_count,
            compress=config.compress_rotated
        )
    elif config.rotation_type == RotationType.TIME:
        handler = TimedRotatingFileHandler(
            log_path,
            when=config.rotation_interval,
            interval=1,
            backupCount=config.backup_count
        )
    else:  # BOTH
        # Use size-based with daily checks
        handler = CompressingRotatingFileHandler(
            log_path,
            maxBytes=config.max_size,
            backupCount=config.backup_count,
            compress=config.compress_rotated
        )
    
    return handler


def setup_logger(
    name: str,
    config: Optional[LogConfig] = None,
    level: Optional[Union[int, str]] = None
) -> logging.Logger:
    """Set up a logger with file and console handlers.
    
    Args:
        name: Name of the logger
        config: Optional LogConfig instance (uses defaults if not provided)
        level: Optional logging level (uses config or INFO if not specified)
    
    Returns:
        Configured logger instance
    """
    if config is None:
        config = LogConfig.from_env()
    
    logger = logging.getLogger(name)
    
    # Set logging level
    if level is None:
        level = getattr(logging, config.log_level.upper(), logging.INFO)
    elif isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Avoid adding handlers if they already exist
    if not logger.handlers:
        # Create formatter
        if config.structured_logging:
            formatter = StructuredFormatter(privacy_mode=config.privacy_mode)
        else:
            formatter = logging.Formatter(config.format, datefmt=config.date_format)
        
        # File handler
        if config.file_output:
            file_handler = create_file_handler(config)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        # Console handler
        if config.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            # Console can have different level for less verbose output
            console_level = os.getenv("FILELOCK_CONSOLE_LOG_LEVEL")
            if console_level:
                console_handler.setLevel(getattr(logging, console_level.upper(), logging.INFO))
            logger.addHandler(console_handler)
    
    return logger


# Create default logger with environment-based config
default_config = LogConfig.from_env()
default_logger = setup_logger("filelock", default_config)


def log_operation(
    logger: logging.Logger,
    operation: str,
    file_path: Path,
    privacy_mode: Optional[PrivacyMode] = None,
    **kwargs
) -> None:
    """Log a file operation with relevant details.
    
    Args:
        logger: Logger instance to use
        operation: Type of operation (e.g., 'encrypt', 'decrypt', 'compress')
        file_path: Path to the file being operated on
        privacy_mode: Override privacy mode for this operation
        **kwargs: Additional key-value pairs to log
    """
    if privacy_mode is None:
        privacy_mode = default_config.privacy_mode
    
    log_data = {
        "operation": operation,
        "file": sanitize_path(file_path, privacy_mode),
        "size": file_path.stat().st_size if file_path.exists() else 0,
        **kwargs,
    }
    
    # Add operation data as extra field for structured logging
    logger.info(f"File operation: {operation}", extra={"operation_data": log_data})


def log_error(
    logger: logging.Logger,
    error: Exception,
    operation: str,
    file_path: Path,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    context: Optional[Dict[str, Any]] = None,
    privacy_mode: Optional[PrivacyMode] = None
) -> None:
    """Log an error with enhanced context and severity.
    
    Args:
        logger: Logger instance to use
        error: Exception that occurred
        operation: Type of operation during which the error occurred
        file_path: Path to the file being operated on
        severity: Error severity level
        context: Additional context information
        privacy_mode: Override privacy mode for this operation
    """
    if privacy_mode is None:
        privacy_mode = default_config.privacy_mode
    
    error_data = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "operation": operation,
        "file": sanitize_path(file_path, privacy_mode),
        "severity": severity.value,
        **(context or {})
    }
    
    # Log with appropriate level based on severity
    if severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
        logger.critical(
            f"Critical error during {operation}: {type(error).__name__}",
            exc_info=True,
            extra={"operation_data": error_data}
        )
    else:
        logger.error(
            f"Error during {operation}: {type(error).__name__}",
            exc_info=True,
            extra={"operation_data": error_data}
        )


@contextmanager
def log_performance(
    logger: logging.Logger,
    operation: str,
    file_path: Path,
    privacy_mode: Optional[PrivacyMode] = None
):
    """Context manager to log operation performance.
    
    Args:
        logger: Logger instance to use
        operation: Type of operation being performed
        file_path: Path to the file being operated on
        privacy_mode: Override privacy mode for this operation
    
    Yields:
        None
    
    Example:
        with log_performance(logger, "encrypt", file_path):
            # Perform encryption
            encrypt_file(file_path)
    """
    start_time = time.time()
    
    try:
        yield
        duration = time.time() - start_time
        log_operation(
            logger,
            operation,
            file_path,
            privacy_mode=privacy_mode,
            duration_seconds=round(duration, 3),
            status="success"
        )
    except Exception as e:
        duration = time.time() - start_time
        log_error(
            logger,
            e,
            operation,
            file_path,
            context={"duration_seconds": round(duration, 3)},
            privacy_mode=privacy_mode
        )
        raise


class OperationMetrics:
    """Track and log operation metrics."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.metrics = {
            "operations": {},
            "errors": {},
            "total_bytes_processed": 0,
            "total_duration": 0.0
        }
    
    def record_operation(self, operation: str, size: int, duration: float, success: bool):
        """Record metrics for an operation."""
        if operation not in self.metrics["operations"]:
            self.metrics["operations"][operation] = {"count": 0, "bytes": 0, "duration": 0.0}
        
        self.metrics["operations"][operation]["count"] += 1
        self.metrics["operations"][operation]["bytes"] += size
        self.metrics["operations"][operation]["duration"] += duration
        
        if not success:
            self.metrics["errors"][operation] = self.metrics["errors"].get(operation, 0) + 1
        
        self.metrics["total_bytes_processed"] += size
        self.metrics["total_duration"] += duration
    
    def log_summary(self):
        """Log a summary of collected metrics."""
        self.logger.info("Operation metrics summary", extra={"operation_data": self.metrics})


# Global metrics instance
metrics = OperationMetrics(default_logger)