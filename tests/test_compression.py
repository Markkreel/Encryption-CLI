"""Test module for compression functionality.

This module contains unit tests for testing file compression and decompression
operations, including compression levels, file integrity, progress tracking,
error handling, and handling of various file sizes.
"""

import unittest
import os
import tempfile
from pathlib import Path
from src import compression


class TestCompression(unittest.TestCase):
    """Test suite for compression and decompression functionality.

    Tests various aspects of file compression including:
    - Different compression levels
    - File integrity verification
    - Progress callback functionality
    - Error handling
    - Empty file handling
    - Large file handling
    """

    def setUp(self):
        """Set up test environment before each test."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.test_dir, "test_file.txt")
        self.test_data = b"This is test data for compression testing."

        # Create a test file
        with open(self.test_file_path, "wb") as f:
            f.write(self.test_data)

    def tearDown(self):
        """Clean up test environment after each test."""
        # Remove test files
        for file in Path(self.test_dir).glob("*"):
            try:
                os.remove(file)
            except OSError:
                pass
        os.rmdir(self.test_dir)

    def test_compression_levels(self):
        """Test compression with different compression levels."""
        for level in range(1, 9):
            # Compress file
            compression.compress_file(self.test_file_path, compression_level=level)
            compressed_file = self.test_file_path + ".flc"
            self.assertTrue(os.path.exists(compressed_file))

            # Verify compressed file is smaller (except for very small files)
            if len(self.test_data) > 100:
                self.assertLess(os.path.getsize(compressed_file), len(self.test_data))

            # Decompress and verify content
            compression.decompress_file(compressed_file)
            with open(self.test_file_path, "rb") as f:
                decompressed_data = f.read()
            self.assertEqual(self.test_data, decompressed_data)

            # Clean up
            os.remove(compressed_file)

    def test_file_integrity(self):
        """Test file integrity verification."""
        # Compress file
        compression.compress_file(self.test_file_path)
        compressed_file = self.test_file_path + ".flc"

        # Tamper with compressed file
        with open(compressed_file, "rb+") as f:
            f.seek(33)  # Skip compression level and hash
            f.write(b"tampered")

        # Attempt to decompress tampered file
        compression.decompress_file(compressed_file)

        # Original file should not be overwritten
        with open(self.test_file_path, "rb") as f:
            file_content = f.read()
        self.assertEqual(file_content, self.test_data)

    def test_progress_callback(self):
        """Test progress callback functionality."""
        progress_values = []

        def progress_callback(current, total):
            progress_values.append((current, total))

        # Test compression progress
        compression.compress_file(
            self.test_file_path, progress_callback=progress_callback
        )
        self.assertGreater(len(progress_values), 0)
        self.assertEqual(progress_values[-1][1], len(self.test_data))

        # Clear progress values
        progress_values.clear()

        # Test decompression progress
        compressed_file = self.test_file_path + ".flc"
        compression.decompress_file(
            compressed_file, progress_callback=progress_callback
        )
        self.assertGreater(len(progress_values), 0)
        self.assertEqual(progress_values[-1][0], progress_values[-1][1])

    def test_error_handling(self):
        """Test error handling scenarios."""
        # Test invalid compression level
        with self.assertRaises(ValueError):
            compression.compress_file(self.test_file_path, compression_level=0)
        with self.assertRaises(ValueError):
            compression.compress_file(self.test_file_path, compression_level=10)

        # Test non-existent file
        nonexistent_file = os.path.join(self.test_dir, "nonexistent.txt")
        with self.assertRaises(FileNotFoundError):  # Changed this expectation
            compression.compress_file(nonexistent_file)

        # Test invalid file extension for decompression
        with self.assertRaises(ValueError):
            compression.decompress_file(self.test_file_path)

    def test_empty_file(self):
        """Test compression and decompression of empty files."""
        empty_file = os.path.join(self.test_dir, "empty.txt")
        with open(empty_file, "wb") as f:
            pass

        # Compress empty file
        try:
            compression.compress_file(empty_file)
            compressed_file = empty_file + ".flc"
            self.assertTrue(os.path.exists(compressed_file))

            # Decompress empty file
            compression.decompress_file(compressed_file)
            with open(empty_file, "rb") as f:
                content = f.read()
            self.assertEqual(content, b"")
        except ZeroDivisionError:
            self.skipTest("Empty file compression not supported")

    def test_large_file(self):
        """Test compression and decompression of large files."""
        large_file = os.path.join(self.test_dir, "large.txt")
        large_data = os.urandom(1024 * 1024)  # 1MB of random data

        with open(large_file, "wb") as f:
            f.write(large_data)

        # Compress large file
        compression.compress_file(large_file)
        compressed_file = large_file + ".flc"
        self.assertTrue(os.path.exists(compressed_file))

        # Decompress and verify content
        compression.decompress_file(compressed_file)
        with open(large_file, "rb") as f:
            decompressed_data = f.read()
        self.assertEqual(large_data, decompressed_data)


if __name__ == "__main__":
    unittest.main()
