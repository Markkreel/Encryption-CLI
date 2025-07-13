# Encryption CLI Examples

This document provides examples of how to use the Encryption CLI tool for various operations including file encryption, decryption, and compression.

## File Encryption

### Basic Encryption

Encrypt a file using default compression (balanced):

```bash
filelock encrypt myfile.txt --password mysecretpassword
```

### Encryption with Different Compression Levels

#### Maximum Compression

Best for achieving smallest file size:

```bash
filelock encrypt largefile.txt --password mysecretpassword --compression max
```

#### Fast Compression

Optimal for quick operations with decent compression:

```bash
filelock encrypt quickfile.txt --password mysecretpassword --compression fast
```

#### No Compression

Use when compression is not needed:

```bash
filelock encrypt sensitivefile.txt --password mysecretpassword --compression none
```

## File Decryption

### Basic Decryption

Decrypt an encrypted file:

```bash
filelock decrypt myfile.txt.flk --password mysecretpassword
```

### Custom Output Location

Decrypt and save to a specific path:

```bash
filelock decrypt myfile.txt.flk --password mysecretpassword --output /custom/path/myfile.txt
```
