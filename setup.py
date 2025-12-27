"""Setup configuration for Olivetti."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="olivetti",
    version="0.1.0",
    description="Personal, highly intelligent AI writing assistant for professional novelists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Olivetti Team",
    author_email="",
    url="https://github.com/superhappyfuntimellc/Olivetti",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.25.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "olivetti=olivetti.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Text Processing",
        "Topic :: Artistic Software",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
