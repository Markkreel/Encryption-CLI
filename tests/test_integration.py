"""Integration tests for the FileLock application.

These tests verify the combined functionality of compression and encryption.
"""

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


def test_secure_file_with_invalid_compression_level(input_file):
    """Test securing a file with invalid compression level."""
    with pytest.raises(ValueError, match="Compression level must be between 1 and 9"):
        secure_file(input_file, "password", compression_level=0)

    with pytest.raises(ValueError, match="Compression level must be between 1 and 9"):
        secure_file(input_file, "password", compression_level=10)


def test_restore_file_with_wrong_extension(input_file):
    """Test restoring a file without .flc extension."""
    with pytest.raises(ValueError, match="File must have .flc extension"):
        restore_file(input_file, "password")


def test_restore_file_with_wrong_password(input_file):
    """Test restoring a file with incorrect password."""
    # First secure the file
    secure_file(input_file, "correct_password")
    secured_file = input_file + ".flc"

    # Then try to restore with wrong password
    with pytest.raises(ValueError):
        restore_file(secured_file, "wrong_password")
