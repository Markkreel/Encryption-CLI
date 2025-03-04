"""Integration module for FileLock compression and encryption functionality.

This module provides a unified interface for compressing and encrypting files,
as well as decrypting and decompressing them, while keeping the implementation
details of individual modules hidden.
"""

import os
from typing import Optional, Callable
from src.compression import compress_file, decompress_file
from src.filelock import encrypt_file, decrypt_file


def secure_file(
    file_path: str,
    password: str,
    compression_level: int = 6,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> None:
    """Encrypt and compress a file.

    This function first encrypts the file using AES-256 encryption and then
    compresses it using zlib compression.

    Args:
        file_path (str): Path to the file to process
        password (str): Password for encryption
        compression_level (int, optional): Compression level (1-9). Defaults to 6.
        progress_callback (Optional[Callable[[int, int], None]], optional):
            Callback for progress tracking. Takes current bytes and total bytes as arguments.
    """
    # First encrypt the file
    encrypt_file(file_path, password)
    encrypted_file = file_path + ".flk"

    # Then compress the encrypted file
    compress_file(encrypted_file, compression_level, progress_callback)

    os.remove(encrypted_file)


def restore_file(
    file_path: str,
    password: str,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> None:
    """Decompress and decrypt a file.

    This function first decompresses the file using zlib decompression and then
    decrypts it using AES-256 decryption.

    Args:
        file_path (str): Path to the compressed and encrypted file (.flc)
        password (str): Password for decryption
        progress_callback (Optional[Callable[[int, int], None]], optional):
            Callback for progress tracking. Takes current bytes and total bytes as arguments.
    """
    if not file_path.endswith(".flc"):
        raise ValueError("File must have .flc extension")

    # First decompress the file
    decompress_file(file_path, progress_callback)
    decompressed_file = file_path[:-4]  # Remove .flc extension

    # Then decrypt the file
    decrypt_file(decompressed_file, password)

    os.remove(decompressed_file)
