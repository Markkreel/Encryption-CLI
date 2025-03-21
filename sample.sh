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