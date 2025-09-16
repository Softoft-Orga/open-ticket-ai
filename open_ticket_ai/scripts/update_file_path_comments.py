#!/usr/bin/env python3
"""Utility to update FILE_PATH comments in Python files.

This script walks through all Python files in a given directory tree
(excluding ``__init__.py`` files). For each file it removes any lines
starting with ``# FILE_PATH:`` and inserts a new comment as the very
first line with the relative path of the file to the project root.
"""
from __future__ import annotations

from pathlib import Path
import re

from open_ticket_ai.src.core.util.path_util import find_python_code_root_path

FILE_PATH_PATTERN = re.compile(r"^\s*#\s*FILE_PATH:.*$")
"""re.Pattern: Regular expression to match lines that are FILE_PATH comments.

The pattern matches any line that starts with optional whitespace, then a `#` character,
followed by the exact string `FILE_PATH:` and then any characters until the end of the line.
"""


def update_file(file_path: Path, project_root: Path) -> None:
    """Update the FILE_PATH comment of ``file_path``.

    Existing comments that match the ``FILE_PATH_PATTERN`` are removed and a
    single line ``# FILE_PATH: <relative>`` is inserted at the top of the file.

    Args:
        file_path: Absolute path to the Python file to update.
        project_root: Root directory of the project (used to calculate relative path).
    """
    lines = file_path.read_text().splitlines()
    cleaned = [line for line in lines if not FILE_PATH_PATTERN.match(line)]
    relative = file_path.relative_to(project_root)
    cleaned.insert(0, f"# FILE_PATH: {relative}")
    file_path.write_text("\n".join(cleaned) + "\n")


def process_directory(directory: Path) -> None:
    """Process all Python files under ``directory``.

    Walks through all Python files in the directory tree (excluding ``__init__.py`` files),
    updating each file's FILE_PATH comment relative to the project root.

    Args:
        directory: Root directory to start processing from.
    """
    project_root = find_python_code_root_path().parent
    for py_file in directory.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        update_file(py_file, project_root)


def main() -> None:
    """Main entry point for the script.

    Processes all Python files in the project's code root directory.
    """
    process_directory(find_python_code_root_path())


if __name__ == "__main__":
    main()
