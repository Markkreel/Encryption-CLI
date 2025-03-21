"""Utility functions for FileLock operations."""

import os
from pathlib import Path
from typing import Union, Optional


def validate_file_path(file_path: Union[str, Path]) -> Path:
    """Validate and return a Path object for the given file path.

    Args:
        file_path: The path to validate as string or Path object

    Returns:
        Path object of the validated file path

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the path is invalid
    """
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
        return path
    except Exception as e:
        raise ValueError(f"Invalid file path: {e}")


def ensure_output_path(
    output_path: Union[str, Path], suffix: Optional[str] = None
) -> Path:
    """Ensure the output path exists and is writable.

    Args:
        output_path: The desired output path
        suffix: Optional suffix to append to the filename

    Returns:
        Path object of the validated output path

    Raises:
        PermissionError: If the path is not writable
        ValueError: If the path is invalid
    """
    try:
        path = Path(output_path)
        if suffix:
            path = path.with_suffix(suffix)

        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Check if path is writable
        if path.exists() and not os.access(path.parent, os.W_OK):
            raise PermissionError(f"Output path is not writable: {path}")

        return path
    except Exception as e:
        raise ValueError(f"Invalid output path: {e}")


def get_file_size(file_path: Union[str, Path]) -> int:
    """Get the size of a file in bytes.

    Args:
        file_path: Path to the file

    Returns:
        Size of the file in bytes
    """
    path = Path(file_path)
    return path.stat().st_size


def is_valid_extension(
    file_path: Union[str, Path], allowed_extensions: list[str]
) -> bool:
    """Check if the file has an allowed extension.

    Args:
        file_path: Path to the file
        allowed_extensions: List of allowed extensions (e.g., [".txt", ".pdf"])

    Returns:
        True if extension is allowed, False otherwise
    """
    return Path(file_path).suffix.lower() in [ext.lower() for ext in allowed_extensions]
