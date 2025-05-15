# Encryption CLI Examples

This document provides examples of how to use the Encryption CLI tool for various operations including file encryption, decryption, and compression.

## File Encryption

### Basic Encryption

Encrypt a file using default compression (balanced):

```bash
python src/cli.py encrypt myfile.txt --password mysecretpassword
```

### Encryption with Different Compression Levels

#### Maximum Compression

Best for achieving smallest file size:

```bash
python src/cli.py encrypt largefile.txt --password mysecretpassword --compression max
```

#### Fast Compression

Optimal for quick operations with decent compression:

```bash
python src/cli.py encrypt quickfile.txt --password mysecretpassword --compression fast
```

#### No Compression

Use when compression is not needed:

```bash
python src/cli.py encrypt sensitivefile.txt --password mysecretpassword --compression none
```

## File Decryption

### Basic Decryption

Decrypt an encrypted file:

```bash
python src/cli.py decrypt myfile.txt.flk --password mysecretpassword
```

### Custom Output Location

Decrypt and save to a specific path:

```bash
python src/cli.py decrypt myfile.txt.flk --password mysecretpassword --output /custom/path/myfile.txt
```

## Direct Compression Operations

### Basic Compression

Compress a file with default settings (level 6):

```python
from src.compression import compress_file
compress_file("myfile.txt")
```

### High Compression Settings

Compress with highest compression level:

```python
from src.compression import compress_file
compress_file("largefile.txt", compression_level=9)
```

### Compression with Progress Tracking

Compress while monitoring progress:

```python
from src.compression import compress_file
compress_file("bigfile.txt", progress_callback=lambda current, total: print(f"Progress: {current}/{total} bytes"))
```

### Basic Decompression

Decompress a compressed file:

```python
from src.compression import decompress_file
decompress_file("myfile.txt.flc")
```

### Decompression with Progress Tracking

Decompress while monitoring progress:

```python
from src.compression import decompress_file
decompress_file("bigfile.txt.flc", progress_callback=lambda current, total: print(f"Progress: {current}/{total} bytes"))
```
