import os
from argparse import ArgumentParser
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA256


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 32-byte encryption key from the password and salt using PBKDF2."""
    return PBKDF2(
        password=password.encode(),
        salt=salt,
        dkLen=32,  # 32 bytes for AES-256
        count=100000,  # Number of iterations
        hmac_hash_module=SHA256
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
            with open(file_path, 'rb') as f:
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
        
        # Pad the data
        padded_data = pad(data, AES.block_size)
        
        # Create cipher and encrypt the data
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(padded_data)
        
        # Write the encrypted file
        encrypted_file_path = file_path + '.flk'
        try:
            with open(encrypted_file_path, 'wb') as f:
                f.write(salt + iv + encrypted_data)
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
    print("Decrypting...")


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
