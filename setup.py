"""Setup config for Notes CLI."""

from setuptools import setup

setup(
    name="notes",
    version="0.0.1",
    description="CLI for taking notes.",
    author="Sam Kenney",
    py_modules=["notes"],
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "notes = notes:cli",
        ],
    },
)
