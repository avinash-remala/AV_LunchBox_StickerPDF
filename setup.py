#!/usr/bin/env python3
"""Setup configuration for av_lunchbox_stickerpdf package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "src" / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = [
        line.strip() 
        for line in requirements_path.read_text().split('\n')
        if line.strip() and not line.startswith('#')
    ]

setup(
    name="av-lunchbox-stickerpdf",
    version="2.0.0",
    author="AV Team",
    description="Generate lunch box order stickers and reports from Google Sheets and images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/av-lunchbox-stickerpdf",
    packages=find_packages(exclude=["tests", "docs"]),
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "av-lunchbox=av_lunchbox_stickerpdf.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
