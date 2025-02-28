import unittest
import os
import tempfile
import hashlib
from pathlib import Path
from filelock import derive_key, encrypt_file, decrypt_file


class TestFileLock(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.test_dir, "test_file.txt")
        self.test_data = b"This is test data for FileLock encryption."
        self.test_password = "testpassword123"

        # Create a test file
        with open(self.test_file_path, "wb") as f:
            f.write(self.test_data)

    def tearDown(self):
        """Clean up test environment after each test."""
        # Remove test files
        for file in Path(self.test_dir).glob("*"):
            try:
                os.remove(file)
            except OSError:
                pass
        os.rmdir(self.test_dir)

    def test_derive_key(self):
        """Test key derivation function."""
        salt = os.urandom(16)
        key1 = derive_key(self.test_password, salt)
        key2 = derive_key(self.test_password, salt)
        different_key = derive_key("differentpassword", salt)

        self.assertEqual(len(key1), 32)  # Check key length (256 bits)
        self.assertEqual(key1, key2)  # Same password and salt should produce same key
        self.assertNotEqual(
            key1, different_key
        )  # Different passwords should produce different keys

    def test_encryption_decryption_success(self):
        """Test successful encryption and decryption process."""
        # Encrypt the test file
        encrypt_file(self.test_file_path, self.test_password)
        encrypted_file = self.test_file_path + ".flk"
        self.assertTrue(os.path.exists(encrypted_file))

        # Decrypt the file
        decrypt_file(encrypted_file, self.test_password)
        decrypted_file = self.test_file_path

        # Verify the decrypted content matches original
        with open(decrypted_file, "rb") as f:
            decrypted_data = f.read()
        self.assertEqual(self.test_data, decrypted_data)

    def test_wrong_password_decryption(self):
        """Test decryption with wrong password."""
        # Encrypt with correct password
        encrypt_file(self.test_file_path, self.test_password)
        encrypted_file = self.test_file_path + ".flk"

        # Try to decrypt with wrong password
        wrong_password = "wrongpassword123"
        decrypt_file(encrypted_file, wrong_password)

        # Original file should not be overwritten
        self.assertTrue(os.path.exists(encrypted_file))

    def test_file_tampering(self):
        """Test detection of file tampering."""
        # Encrypt the file
        encrypt_file(self.test_file_path, self.test_password)
        encrypted_file = self.test_file_path + ".flk"

        # Tamper with the encrypted file
        with open(encrypted_file, "rb+") as f:
            f.seek(64)  # Skip salt, IV, and hash
            f.write(b"tampered")

        # Attempt to decrypt tampered file
        decrypt_file(encrypted_file, self.test_password)

        # Check if the original file was not overwritten
        self.assertFalse(os.path.exists(self.test_file_path))

    def test_nonexistent_file(self):
        """Test handling of non-existent files."""
        nonexistent_file = os.path.join(self.test_dir, "nonexistent.txt")
        encrypt_file(nonexistent_file, self.test_password)
        self.assertFalse(os.path.exists(nonexistent_file + ".flk"))

    def test_empty_file(self):
        """Test encryption and decryption of empty files."""
        empty_file = os.path.join(self.test_dir, "empty.txt")
        with open(empty_file, "wb") as f:
            pass

        # Encrypt and decrypt empty file
        encrypt_file(empty_file, self.test_password)
        encrypted_file = empty_file + ".flk"
        self.assertTrue(os.path.exists(encrypted_file))

        decrypt_file(encrypted_file, self.test_password)
        with open(empty_file, "rb") as f:
            content = f.read()
        self.assertEqual(content, b"")


if __name__ == "__main__":
    unittest.main()
