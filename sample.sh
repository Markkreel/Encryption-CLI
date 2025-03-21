#!/bin/bash

# Example commands for using FileLock CLI

# Basic file encryption with default compression (balanced)
echo "Example 1: Encrypt a file with password"
echo "python src/cli.py encrypt myfile.txt --password mysecretpassword"

# Encrypt with different compression levels
echo "\nExample 2: Encrypt with maximum compression"
echo "python src/cli.py encrypt largefile.txt --password mysecretpassword --compression max"

echo "\nExample 3: Encrypt with fast compression"
echo "python src/cli.py encrypt quickfile.txt --password mysecretpassword --compression fast"

echo "\nExample 4: Encrypt without compression"
echo "python src/cli.py encrypt sensitivefile.txt --password mysecretpassword --compression none"

# Basic file decryption
echo "\nExample 5: Decrypt a file"
echo "python src/cli.py decrypt myfile.txt.flk --password mysecretpassword"

# Decrypt with custom output path
echo "\nExample 6: Decrypt to custom output location"
echo "python src/cli.py decrypt myfile.txt.flk --password mysecretpassword --output /custom/path/myfile.txt"

# Direct compression examples using compression.py
echo "\n# Direct Compression Examples"

# Basic compression with default level (6)
echo "\nExample 7: Basic compression"
echo "python -c 'from src.compression import compress_file; compress_file(\"myfile.txt\")'" 

# Compression with maximum level
echo "\nExample 8: Maximum compression (level 9)"
echo "python -c 'from src.compression import compress_file; compress_file(\"largefile.txt\", compression_level=9)'" 

# Compression with progress tracking
echo "\nExample 9: Compression with progress tracking"
echo "python -c 'from src.compression import compress_file; compress_file(\"bigfile.txt\", progress_callback=lambda current, total: print(f\"Progress: {current}/{total} bytes\"))'" 

# Basic decompression
echo "\nExample 10: Basic decompression"
echo "python -c 'from src.compression import decompress_file; decompress_file(\"myfile.txt.flc\")'" 

# Decompression with progress tracking
echo "\nExample 11: Decompression with progress tracking"
echo "python -c 'from src.compression import decompress_file; decompress_file(\"bigfile.txt.flc\", progress_callback=lambda current, total: print(f\"Progress: {current}/{total} bytes\"))'"