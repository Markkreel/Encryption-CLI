from setuptools import setup, find_packages

setup(
    name="FileLock",
    version="0.1",
    packages=["filelock"],
    package_dir={"filelock": "src"},
    install_requires=[
        "pytest",  # For testing
    ],
    author="Portfolio Project",
    description="A secure file locking and encryption tool",
    python_requires=">=3.8",
)
