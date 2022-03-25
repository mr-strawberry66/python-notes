"""Nox configuration to Lint, Format and Test code."""
import os

import nox


def list_py_modules():
    """Get modules for linting / testing."""
    root_dir = os.path.dirname(os.path.abspath(__file__))

    return [
        item
        for item in os.listdir(root_dir)
        if os.path.isdir(item)
        and not item.startswith(".")
        and item not in ["venv", "__pycache__"]
        or item.endswith(".py")
    ]


@nox.session
def reformat(session):
    """Reformat using Black."""
    session.install("black")
    session.run("black", ".")


@nox.session
def lint(session):
    """Lint using Flake8 and PyLint."""
    args = list_py_modules()
    session.install(
        "flake8",
        "flake8-docstrings",
        "flake8-import-order",
        "pylint",
        "nox",
    )
    if os.path.isfile("requirements.txt"):
        session.install("-r", "requirements.txt")

    session.run("flake8", "--max-complexity=8")
    session.run("pylint", *args)


@nox.session
def test(session):
    """Run tests."""
    dirs = [item for item in list_py_modules() if os.path.isdir(item)]
    args = ["--cov=" + item for item in dirs]

    session.install("pytest", "pytest-cov")
    if os.path.isfile("requirements.txt"):
        session.install("-r", "requirements.txt")

    session.run(
        "pytest",
        *args,
        "--cov-report",
        "term-missing",
    )
