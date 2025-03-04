from setuptools import setup, find_packages

setup(
    name="FileLock",
    version="0.1",
    packages=["filelock"],
    package_dir={"filelock": "src"},
    install_requires=[
        "pycryptodome",  # For encryption/decryption functionality
        "pytest",  # For testing
        "pytest-cov",  # For coverage reporting
    ],
    entry_points={
        "console_scripts": [
            "filelock=filelock.cli:main",
        ],
    },
    author="Portfolio Project",
    description="A secure file locking and encryption tool",
    python_requires=">=3.8",
)
