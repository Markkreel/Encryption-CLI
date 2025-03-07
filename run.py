from src.main import secure_file, restore_file

# Example usage
file_path = "example.txt"

# Create a test file
with open(file_path, "w") as f:
    f.write("This is a test file to encrypt and compress!")

# Secure the file
secure_file(file_path, "your_password")

# Restore the file
restore_file(file_path + ".flc", "your_password")