# FileLock

![1741196416000](image/README/1741196416000.png)

A Python utility for securely encrypting files with AES-256 encryption and zlib compression, with integrity verification and progress tracking.

## DEVELOPMENT NOTE!

The program is currently stable but doesn't have a complete CLI integration for encryption/decryption and compression features. To test the program, you can skip the usage section and directly use `run.py`. Modify the `FILE_PATH` variable in `run.py` to encrypt/decrypt your desired file. You can also adjust the compression level in `main.py` by modifying `compression_level` variable.

You still have the option to run the encryption/decryption features separately from the compression feature by running `filelock.py` in your CLI.

## Specifications

- AES-256 CBC mode encryption
- Zlib compression with configurable levels (1-9)
- SHA-256 hash verification for tamper detection

## Installation

```bash
# Requires Python 3.9+
pip install -r requirements.txt
```

## Usage

### Secure a File (Encrypt + Compress)

```python
from src.main import secure_file

secure_file(
    "sensitive.docx",
    "your_strong_password",
    compression_level=7  # Optimal balance of speed/size
)
# Creates: sensitive.docx.flc
```

### Restore a File (Decrypt + Decompress)

```python
from src.main import restore_file

restore_file(
    "sensitive.docx.flc",
    "your_strong_password"
)
# Restores: sensitive.docx
```

## Technical Details

### File Structure (.flc)

```
[1 byte: compression level] +
[32 bytes: SHA-256 hash] +
[zlib compressed data] +
[AES-256 encrypted payload]
```

### Integrity Verification

1. Generates SHA-256 hash of original data
2. Stores hash in file header
3. Verifies hash during restoration

## Testing

Run test suite:

```bash
pytest tests/ -v
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Submit pull request

## License

MIT License - See [LICENSE](LICENSE) for details

**Last Updated:** 10-03-2025 ⸺ **Last Checked:** 10-03-2025
