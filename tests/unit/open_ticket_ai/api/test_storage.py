"""Tests for the flow editor API storage module."""

import tempfile
from pathlib import Path

import pytest

from open_ticket_ai.api.storage import read_text_file, write_text_file


def test_write_and_read_text_file():
    """Test writing and reading a text file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.txt"
        content = "Hello, World!"

        write_text_file(file_path, content)
        read_content = read_text_file(file_path)

        assert read_content == content


def test_read_text_file_not_found():
    """Test reading a non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_text_file("/nonexistent/file.txt")


def test_write_text_file_creates_parent_dirs():
    """Test that write_text_file creates parent directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "subdir" / "test.txt"
        content = "Test content"

        write_text_file(file_path, content)

        assert file_path.exists()
        assert read_text_file(file_path) == content


def test_read_text_file_with_utf8():
    """Test reading and writing UTF-8 encoded text."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "utf8.txt"
        content = "Hello 世界 🌍"

        write_text_file(file_path, content)
        read_content = read_text_file(file_path)

        assert read_content == content
