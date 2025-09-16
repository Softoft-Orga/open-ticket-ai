"""Generates a directory tree structure while respecting `.gitignore` rules.

This module provides functionality to traverse a directory hierarchy, exclude files
and directories specified in a `.gitignore` file, and generate a visual tree
representation of the structure using the `rich` library.
"""
from io import StringIO
from pathlib import Path

from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from pathspec.util import normalize_file
from rich import print
from rich.console import Console
from rich.tree import Tree

from open_ticket_ai.src.core.util.path_util import find_python_code_root_path


def load_gitignore(base_path: Path) -> PathSpec:
    """Loads and parses a .gitignore file into a PathSpec object.

    Args:
        base_path (Path): The directory path containing the .gitignore file.

    Returns:
        PathSpec: A PathSpec object representing the ignore patterns. Returns an empty
        PathSpec if no .gitignore file exists.
    """
    gitignore = base_path / ".gitignore"
    if not gitignore.exists():
        return PathSpec.from_lines(GitWildMatchPattern, [])
    lines = gitignore.read_text().splitlines()
    return PathSpec.from_lines(GitWildMatchPattern, lines)


def build_tree(base_path: Path, spec: PathSpec, tree: Tree, relative_path=""):
    """Recursively builds a directory tree structure while respecting gitignore rules.

    Walks through the directory structure starting at `base_path`, adding nodes to the
    provided `tree` object. Files/directories matching .gitignore patterns are excluded.

    Args:
        base_path (Path): The root directory to start building the tree from.
        spec (PathSpec): PathSpec object containing gitignore patterns.
        tree (Tree): Rich Tree object to populate with directory structure.
        relative_path (str): Internal path accumulator for recursion (default: "").
    """
    for path in sorted(base_path.iterdir()):
        rel_path = normalize_file((Path(relative_path) / path.name).as_posix())
        if spec.match_file(rel_path):
            continue
        if path.is_dir():
            branch = tree.add(f"{path.name}")
            build_tree(path, spec, branch, rel_path)
        else:
            tree.add(path.name)


def get_tree_str(tree: Tree) -> str:
    """Renders a Rich Tree object to a string representation.

    Args:
        tree (Tree): Rich Tree object to render.

    Returns:
        str: String representation of the tree structure.
    """
    buf = StringIO()
    console = Console(file=buf, force_terminal=True, width=120)
    console.print(tree)
    return buf.getvalue()


def display_dir_tree(path_str: str) -> str:
    """Generates a visual directory tree structure respecting .gitignore rules.

    Args:
        path_str (str): Path to the root directory to visualize.

    Returns:
        str: Formatted string representation of the directory tree.
    """
    base_path = Path(path_str).resolve()
    spec = load_gitignore(base_path)
    tree = Tree(f"{base_path.name}")
    build_tree(base_path, spec, tree)
    return get_tree_str(tree)


if __name__ == "__main__":
    print(display_dir_tree(find_python_code_root_path().parent))
