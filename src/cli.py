"""Command-line interface for FileLock."""

import argparse
from pathlib import Path
from typing import Optional

from .config import COMPRESSION_LEVELS, DEFAULT_COMPRESSION_LEVEL
from .logging import setup_logger
from .utils import validate_file_path, is_valid_extension
from .config import ALLOWED_EXTENSIONS

logger = setup_logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="FileLock - Secure file encryption and compression tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Encrypt command
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file")
    encrypt_parser.add_argument(
        "file_path", type=str, help="Path to the file to encrypt"
    )
    encrypt_parser.add_argument(
        "--password", type=str, required=True, help="Encryption password"
    )
    encrypt_parser.add_argument(
        "--compression",
        choices=list(COMPRESSION_LEVELS.keys()),
        default=DEFAULT_COMPRESSION_LEVEL,
        help="Compression level",
    )
    encrypt_parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: input file path + .encrypted)",
    )

    # Decrypt command
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file")
    decrypt_parser.add_argument(
        "file_path", type=str, help="Path to the encrypted file"
    )
    decrypt_parser.add_argument(
        "--password", type=str, required=True, help="Decryption password"
    )
    decrypt_parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: removes .encrypted extension)",
    )

    return parser


def validate_args(args: argparse.Namespace) -> bool:
    """Validate command-line arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        True if arguments are valid, False otherwise
    """
    try:
        file_path = validate_file_path(args.file_path)

        if not is_valid_extension(file_path, ALLOWED_EXTENSIONS):
            logger.error("Unsupported file type: %s", file_path.suffix)
            return False

        if args.command == "encrypt":
            if len(args.password) < 8:
                logger.error("Password must be at least 8 characters long")
                return False

        elif args.command == "decrypt":
            if not file_path.suffix.endswith(".encrypted"):
                logger.error("File does not appear to be encrypted")
                return False

        return True

    except (FileNotFoundError, ValueError) as e:
        logger.error(str(e))
        return False


def parse_args() -> Optional[argparse.Namespace]:
    """Parse and validate command-line arguments.

    Returns:
        Parsed arguments if valid, None otherwise
    """
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return None

    if validate_args(args):
        return args

    return None
