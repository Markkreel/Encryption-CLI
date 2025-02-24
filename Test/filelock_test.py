import os
import sys
from argparse import ArgumentParser
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
import hashlib


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 32-byte encryption key from the password and salt using PBKDF2."""
    return PBKDF2(
        password=password.encode(),
        salt=salt,
        dkLen=32,  # 32 bytes for AES-256
        count=100000,  # Number of iterations
        hmac_hash_module=SHA256,
    )


def encrypt_file(file_path: str, password: str) -> None:
    """Encrypt a file using AES-256 in CBC mode with the provided password."""
    try:
        # Generate a random salt for key derivation
        salt = os.urandom(16)

        # Derive the encryption key from the password
        key = derive_key(password, salt)

        # Generate a random IV for encryption
        iv = os.urandom(16)

        # Read the file data
        try:
            with open(file_path, "rb") as f:
                data = f.read()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            return
        except PermissionError:
            print(f"Error: Permission denied accessing file '{file_path}'")
            return
        except IOError as e:
            print(f"Error reading file: {e}")
            return

        # Calculate hash of original data
        data_hash = hashlib.sha256(data).digest()

        # Pad the data
        padded_data = pad(data, AES.block_size)

        # Create cipher and encrypt the data
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(padded_data)

        # Write the encrypted file
        encrypted_file_path = file_path + ".flk"
        try:
            with open(encrypted_file_path, "wb") as f:
                # Format: [salt (16) | iv (16) | hash (32) | encrypted_data]
                f.write(salt + iv + data_hash + encrypted_data)
        except PermissionError:
            print(f"Error: Permission denied writing to '{encrypted_file_path}'")
            return
        except IOError as e:
            print(f"Error writing encrypted file: {e}")
            return

        print(f"File encrypted successfully: {encrypted_file_path}")
    except Exception as e:
        print(f"Error during encryption: {e}")


def decrypt_file(file_path: str, password: str) -> None:
    """Decrypt a file using the provided password."""
    try:
        # Read the encrypted file
        try:
            with open(file_path, "rb") as f:
                data = f.read()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            return
        except PermissionError:
            print(f"Error: Permission denied accessing file '{file_path}'")
            return
        except IOError as e:
            print(f"Error reading file: {e}")
            return

        # Extract components
        # Format: [salt (16) | iv (16) | hash (32) | encrypted_data]
        salt = data[:16]
        iv = data[16:32]
        hash_stored = data[32:64]
        encrypted_data = data[64:]

        # Derive the key from the password and salt
        key = derive_key(password, salt)

        # Create cipher and decrypt the data
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_data = cipher.decrypt(encrypted_data)
            original_data = unpad(decrypted_data, AES.block_size)
        except ValueError as e:
            print(f"Error: Invalid padding or corrupted data - {e}", file=sys.stderr)
            return
        except Exception as e:
            print(f"Error during decryption: {e}", file=sys.stderr)
            return

        # Verify integrity
        hash_computed = hashlib.sha256(original_data).digest()
        if hash_stored != hash_computed:
            print(
                "Error: Integrity check failed - file may have been tampered with",
                file=sys.stderr,
            )
            return

        # Write the decrypted file
        decrypted_file_path = file_path.replace(".flk", "")
        try:
            with open(decrypted_file_path, "wb") as f:
                f.write(original_data)
        except PermissionError:
            print(f"Error: Permission denied writing to '{decrypted_file_path}'")
            return
        except IOError as e:
            print(f"Error writing decrypted file: {e}")
            return

        print(f"File decrypted successfully: {decrypted_file_path}")
    except Exception as e:
        print(f"Error during decryption: {e}", file=sys.stderr)


def main():
    parser = ArgumentParser(
        description="FileLock: A secure file encryption and decryption tool using AES-256"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Encrypt command
    encrypt_parser = subparsers.add_parser(
        "encrypt", help="Encrypt a file using AES-256"
    )
    encrypt_parser.add_argument("file", help="Path to the file to encrypt")
    encrypt_parser.add_argument(
        "--password", required=True, help="Password for encryption"
    )

    # Decrypt command
    decrypt_parser = subparsers.add_parser(
        "decrypt", help="Decrypt a file using AES-256"
    )
    decrypt_parser.add_argument("file", help="Path to the file to decrypt")
    decrypt_parser.add_argument(
        "--password", required=True, help="Password for decryption"
    )

    args = parser.parse_args()

    if args.command == "encrypt":
        encrypt_file(args.file, args.password)
    elif args.command == "decrypt":
        decrypt_file(args.file, args.password)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
