"""
Setup script for FileLock package.
Handles package configuration, dependencies and metadata for distribution.
"""

from setuptools import setup, find_packages

setup(
    name="FileLock",
    version="0.1",
    packages=find_packages(),
    package_dir={"": "src"},
    install_requires=[
        "pytest",  # For testing
    ],
    entry_points={
        'console_scripts': [
            'filelock=main:main',
        ],
    },
    author="Portfolio Project",
    description="A secure file locking and encryption tool",
    python_requires=">=3.8",
)
