"""
Run script for main.py
"""

from src.main import secure_file, restore_file

# Example usage
FILE_PATH = r"C:/External/Portfolio/FileLock/localtest/test.txt.flk.flc"

# Create a test file
with open(FILE_PATH, "w", encoding="UTF-8") as f:
    f.write("This is a test file to encrypt and compress!")

# Secure the file
secure_file(FILE_PATH, "your_password")

# Restore the file
restore_file(FILE_PATH + ".flc", "your_password")
