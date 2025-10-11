"""Tests for the path utility module."""

from pathlib import Path

from open_ticket_ai.core.util.path_util import find_python_code_root_path


def test_find_python_code_root_path_returns_path():
    """Test that find_python_code_root_path returns a valid Path object."""
    result = find_python_code_root_path()
    
    assert isinstance(result, Path)
    assert result.exists()
    assert result.is_dir()


def test_find_python_code_root_path_contains_open_ticket_ai():
    """Test that the returned path points to the open_ticket_ai package."""
    result = find_python_code_root_path()
    
    assert result.name == "open_ticket_ai"
    assert (result / "__init__.py").exists()


def test_find_python_code_root_path_parent_is_src():
    """Test that the parent of the returned path is the src directory."""
    result = find_python_code_root_path()
    
    assert result.parent.name == "src"
