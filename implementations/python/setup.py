#!/usr/bin/env python3
"""
Setup script for VerBeat Python package
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "VerBeat - A 3D Versioning System for Real-World Dev Flow"

# Read version from verbeat.version file
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'verbeat.version')
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    version_str = line.split('#')[0].strip()
                    try:
                        return int(version_str)
                    except ValueError:
                        pass
    return 1

setup(
    name="verbeat",
    version=f"{get_version()}.0.0",
    description="A 3D Versioning System for Real-World Dev Flow",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Avner Cohen",
    author_email="israbirding@gmail.com",
    url="https://github.com/verbeat/verbeat",
    packages=find_packages(),
    py_modules=["verbeat"],
    entry_points={
        "console_scripts": [
            "verbeat=verbeat:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control",
    ],
    python_requires=">=3.9",
    keywords="versioning, git, semantic, calendar, version management",
    project_urls={
        "Bug Reports": "https://github.com/verbeat/verbeat/issues",
        "Source": "https://github.com/verbeat/verbeat",
        "Documentation": "https://github.com/verbeat/verbeat#readme",
    },
    include_package_data=True,
    zip_safe=False,
) 