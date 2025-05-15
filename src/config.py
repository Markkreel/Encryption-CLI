"""Configuration settings for FileLock."""

from pathlib import Path

# Compression settings
COMPRESSION_LEVELS = {"none": 0, "fast": 3, "balanced": 6, "max": 9}
DEFAULT_COMPRESSION_LEVEL = "balanced"

# File settings
ALLOWED_EXTENSIONS = [
    ".txt",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".jpg",
    ".jpeg",
    ".png",
    ".zip",
    ".rar",
    ".7z",
]

# Encryption settings
KEY_LENGTH = 32  # 256-bit key
SALT_LENGTH = 16  # 128-bit salt
IV_LENGTH = 16  # 128-bit IV
HASH_ITERATIONS = 100000

# Output settings
ENCRYPTED_SUFFIX = ".encrypted"
COMPRESSED_SUFFIX = ".compressed"

# Buffer sizes
READ_BUFFER_SIZE = 64 * 1024  # 64KB chunks for file reading
WRITE_BUFFER_SIZE = 64 * 1024  # 64KB chunks for file writing

# Temporary file settings
TEMP_DIR = Path.home() / ".filelock" / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Error messages
ERROR_MESSAGES = {
    "invalid_password": "Invalid password provided",
    "file_not_found": "File not found: {}",
    "invalid_extension": "File type not supported: {}",
    "compression_error": "Error compressing file: {}",
    "encryption_error": "Error encrypting file: {}",
    "decryption_error": "Error decrypting file: {}",
    "permission_error": "Permission denied: {}",
}
