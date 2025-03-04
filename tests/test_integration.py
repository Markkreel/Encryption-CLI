"""Integration tests for the FileLock application.

These tests verify the combined functionality of compression and encryption.
"""

import os
import zlib
import pytest
from src.main import secure_file, restore_file


@pytest.fixture
def test_file(tmp_path):
    """Create a temporary test file."""
    file_path = tmp_path / "test.txt"
    content = b"Hello, this is a test file for FileLock integration testing!"
    with open(file_path, "wb") as f:
        f.write(content)
    return str(file_path)


def test_secure_and_restore_file(test_file):
    """Test the complete workflow of securing and restoring a file."""
    password = "test_password"
    original_content = open(test_file, "rb").read()

    # Secure the file (encrypt + compress)
    try:
        secure_file(test_file, password)
        secured_file = test_file + ".flc"
    except zlib.error as e:
        raise ValueError(f"Failed to compress data: {e}") from e

    # Verify the secured file exists and original is unchanged
    assert os.path.exists(secured_file)
    assert open(test_file, "rb").read() == original_content

    # Remove the original file to ensure restore creates a new one
    os.remove(test_file)
    assert not os.path.exists(test_file)

    # Restore the file (decompress + decrypt)
    try:
        restore_file(secured_file, password)
    except zlib.error as e:
        raise ValueError(f"Failed to decompress data: {e}") from e

    # Verify the restored content matches the original
    assert os.path.exists(test_file)
    restored_content = open(test_file, "rb").read()
    assert restored_content == original_content


def test_secure_file_with_invalid_compression_level(test_file):
    """Test securing a file with invalid compression level."""
    with pytest.raises(ValueError, match="Compression level must be between 1 and 9"):
        secure_file(test_file, "password", compression_level=0)

    with pytest.raises(ValueError, match="Compression level must be between 1 and 9"):
        secure_file(test_file, "password", compression_level=10)


def test_restore_file_with_wrong_extension(test_file):
    """Test restoring a file without .flc extension."""
    with pytest.raises(ValueError, match="File must have .flc extension"):
        restore_file(test_file, "password")


def test_restore_file_with_wrong_password(test_file):
    """Test restoring a file with incorrect password."""
    # First secure the file
    try:
        secure_file(test_file, "correct_password")
        secured_file = test_file + ".flc"
    except zlib.error as e:
        raise ValueError(f"Failed to compress data: {e}") from e

    # Then try to restore with wrong password
    try:
        with pytest.raises(ValueError):
            restore_file(secured_file, "wrong_password")
    except zlib.error as e:
        raise ValueError(f"Failed to decompress data: {e}") from e
