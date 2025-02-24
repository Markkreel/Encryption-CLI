import os
from argparse import ArgumentParser


def encrypt_file(file_path: str, password: str) -> None:
    """Encrypt a file using the provided password."""
    print("Encrypting...")


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
