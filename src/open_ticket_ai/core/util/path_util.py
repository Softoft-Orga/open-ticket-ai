"""Utility functions for path operations."""

from pathlib import Path


def find_python_code_root_path(project_name: str = "src") -> Path:
    """Find the project root path by searching for a parent directory with the given name.

    Args:
        project_name: Name of the project root directory (default: "src")

    Returns:
        Path to the project root directory

    Raises:
        FileNotFoundError: If the project root is not found
    """
    start_path = Path(__file__).resolve()
    for parent in [start_path, *start_path.parents]:
        if parent.name == project_name:
            return parent
    raise FileNotFoundError(f"Project folder '{project_name}' not found in parents of {start_path}")
