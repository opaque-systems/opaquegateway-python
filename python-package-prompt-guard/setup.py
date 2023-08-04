from pathlib import Path

from setuptools import setup

README_FILE_PATH = Path("README.md")


# Note the package should always be installed via `pip install` rather than
# directly calling setup.py. When installed that way, the values of
# pyproject.toml are passed in here
setup(
    packages=["promptguard"],
    package_dir={"": "src"},
    long_description=README_FILE_PATH.read_text(),
)
