"""Provides compression and decompression functionality for files using zlib."""

import zlib
import hashlib
from typing import Optional, Callable
from pathlib import Path


def compress_file(
    file_path: str,
    compression_level: int = 6,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> None:
    """Compress a file using zlib with the specified compression level.

    Args:
        file_path (str): Path to the file to compress
        compression_level (int, optional): Compression level (1-9). Defaults to 6.
        progress_callback (Optional[Callable[[int, int], None]], optional): Callback for
            Takes current bytes processed and total bytes as arguments.
    """
    if not 1 <= compression_level <= 9:
        raise ValueError("Compression level must be between 1 and 9")

    # Read the file data
    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File '{file_path}' not found") from exc
    except PermissionError as exc:
        raise PermissionError(
            f"Permission denied accessing file '{file_path}'"
        ) from exc
    except IOError as exc:
        raise IOError(f"Error reading file: {exc}") from exc

    # Calculate hash of original data
    data_hash = hashlib.sha256(data).digest()

    # Initialize compressor
    compressor = zlib.compressobj(level=compression_level)
    compressed_data = compressor.compress(data)
    compressed_data += compressor.flush()

    total_size = len(data)
    processed_size = 0

    # Write the compressed file
    compressed_file_path = file_path + ".flc"
    try:
        with open(compressed_file_path, "wb") as f:
            # Format: [compression_level (1) | hash (32) | compressed_data]
            f.write(bytes([compression_level]) + data_hash + compressed_data)
            processed_size = len(compressed_data)
            if progress_callback:
                progress_callback(processed_size, total_size)

    except PermissionError as exc:
        raise PermissionError(
            f"Permission denied writing to '{compressed_file_path}'"
        ) from exc
    except IOError as e:
        raise IOError(f"Error writing compressed file: {e}") from e

    print(f"File compressed successfully: {compressed_file_path}")
    compression_ratio = (1 - len(compressed_data) / total_size) * 100
    print(f"Compression ratio: {compression_ratio:.1f}%")


def decompress_file(
    file_path: str, progress_callback: Optional[Callable[[int, int], None]] = None
) -> None:
    """Decompress a .flc file and verify its integrity.

    Args:
        file_path (str): Path to the compressed file
        progress_callback (Optional[Callable[[int, int], None]], optional): Callback for
            progress tracking.
            Takes current bytes processed and total bytes as arguments.
    """
    if not file_path.endswith(".flc"):
        raise ValueError("File must have .flc extension")

    # Read the compressed file
    try:
        with open(file_path, "rb") as f:
            # Read compression level and hash
            f.read(1)  # Skip compression level byte as it's not needed
            original_hash = f.read(32)
            compressed_data = f.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File '{file_path}' not found") from exc
    except PermissionError as exc:
        raise PermissionError(
            f"Permission denied accessing file '{file_path}'"
        ) from exc
    except IOError as exc:
        raise IOError(f"Error reading compressed file: {exc}") from exc

    # Decompress the data
    try:
        decompressor = zlib.decompressobj()
        decompressed_data = decompressor.decompress(compressed_data)
        decompressed_data += decompressor.flush()
    except zlib.error as e:
        raise ValueError(f"Failed to decompress data: {e}") from e

    # Verify integrity
    computed_hash = hashlib.sha256(decompressed_data).digest()
    if computed_hash != original_hash:
        raise ValueError("File integrity check failed. The file may be corrupted.")

    # Write the decompressed file
    output_file_path = str(Path(file_path).with_suffix(""))
    try:
        with open(output_file_path, "wb") as f:
            f.write(decompressed_data)
            if progress_callback:
                progress_callback(len(decompressed_data), len(decompressed_data))
    except PermissionError as exc:
        raise PermissionError(
            f"Permission denied writing to '{output_file_path}'"
        ) from exc
    except IOError as e:
        raise IOError(f"Error writing decompressed file: {e}") from e

    print(f"File decompressed successfully: {output_file_path}")
