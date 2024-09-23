"""
Setup script for CodeMapper package.

This script provides the necessary configuration for packaging and distributing
the CodeMapper tool via PyPI.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codemapper",
    version="3.2.0",
    author="Shane Holloman",
    author_email="your.email@example.com",
    description="A tool to generate comprehensive Markdown artifacts of directory structures and file contents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shaneholloman/codemapper",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "chardet",
        "pathspec",
    ],
    entry_points={
        "console_scripts": [
            "codemapper=codemapper.codemapper:main",
        ],
    },
)
