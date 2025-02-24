# FileLock

**FileLock** is a command-line tool designed to securely encrypt files using AES-256 encryption with a password-derived key. Built with Python, it’s a simple yet powerful utility for protecting sensitive data. This project is under active development.

![1740416788661](image/README/1740416788661.png)

## Purpose

In a world where data security is critical, FileLock provides a lightweight, open-source solution to encrypt files with a password of your choice. Whether it’s a personal document or a configuration file, FileLock ensures your data stays confidential using industry-standard cryptography.

## Current Features

- **Encryption:** Encrypt any file with AES-256 in CBC mode, using a secure key derived from your password via PBKDF2.
- **CLI Interface:** Easy-to-use command-line interface with clear arguments for file and password input.

## Installation

**FileLock** requires Python 3.9+ and one external library. Here’s how to set it up:

Clone the repository:

```bash
git clone https://github.com/yourusername/filelock.git
cd filelock
```

Install dependencies:

```bash
pip install pycryptodome
```

Run the tool:

- On **Unix-like systems (Linux/macOS)**: `./filelock.py`
- On **Windows** or others: `python filelock.py`

## Usage

FileLock currently supports encrypting files. Here’s how to use it:

### Encrypt a File

Encrypt a file with a password:

```bash
python filelock.py encrypt <file> --password "<your_password>"
```

**Notes**:

- The encrypted file **(**`<file>.flk`) contains the salt, initialization vector (IV), and encrypted data.
- Decryption is coming soon.

## Help

```bash
python filelock.py --help
```

## Design Decisions

- **AES-256 CBC**: Chosen for its strength and widespread use in secure applications. CBC mode adds randomness via the IV, making each encryption unique even with the same password.
- **PBKDF2 for Key Derivation**: Uses 100,000 iterations to turn your password into a secure 32-byte key, paired with a random 16-byte salt to prevent rainbow table attacks.
- **File Format**: The encrypted output (`<file>.flk`) bundles salt, IV, and encrypted data into one file for simplicity and portability.

## Contrubuting

This is a personal project for my portfolio, but feel free to fork it and experiment! Suggestions are welcome—open an issue if you spot something to improve.

**Last Updated:** 24-02-2025 ⸺ **Last Checked:** 25-02-2025
