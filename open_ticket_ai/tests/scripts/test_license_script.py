"""Tests for the license_script module.

This module contains unit tests for the functions in `open_ticket_ai.scripts.license_script`.
It tests the functionality of:
- Finding the start of code in a file
- Updating license notices in files within a directory
- Handling various file types and content scenarios

The tests use pytest fixtures to create temporary directories with test files
and parametrized tests to cover multiple input cases.
"""
import os

import pytest

pytest.importorskip("rich")

from open_ticket_ai.scripts.license_script import (
    find_start_of_code,
    new_license_notice,
    read_file,
    update_license_in_files,
)

TEST_DIR = "test_license_files_temp"
"""Name of the temporary directory used for testing."""


@pytest.fixture
def setup_test_directory(tmp_path):
    """Sets up a temporary directory with various files for testing.

    This fixture creates a temporary directory structure with multiple test files
    representing different scenarios:

    - Python files with only code
    - Python files with only comments
    - Python files with mixed comments and code
    - Empty Python files
    - Non-Python text files
    - Python files that already have the new license notice

    After the test runs, the temporary directory is automatically cleaned up.

    Args:
        tmp_path: Pytest fixture providing a temporary directory path.

    Yields:
        str: The path to the temporary test directory.
    """
    test_dir = tmp_path / TEST_DIR
    os.makedirs(test_dir, exist_ok=True)

    # File content examples
    file_contents = {
        "file_with_code.py": "print('Hello World')",
        "file_with_comments.py": "# This is a comment\n# Another comment",
        "file_with_mixed_content.py": "# Comment line\nprint('Code line')",
        "empty_file.py": "",
        "non_python_file.txt": "This is a text file.",
        "already_licensed.py": new_license_notice + "\\nprint('already licensed')"
    }

    for filename, content in file_contents.items():
        with open(test_dir / filename, "w") as f:
            f.write(content)

    # Create a subdirectory with a python file
    sub_dir = test_dir / "subdir"
    os.makedirs(sub_dir, exist_ok=True)
    with open(sub_dir / "sub_file.py", "w") as f:
        f.write("print('Hello from sub dir')")

    yield str(test_dir)

    # Teardown: Remove the temporary directory
    # shutil.rmtree(test_dir) # tmp_path fixture handles cleanup


@pytest.mark.parametrize(
    "lines, expected_index",
    [
        (["# comment1", "# comment2", "code_line"], 2),
        (["code_line", "# comment1"], 0),
        (["", "\t", "  ", "code_line"], 3),
        (["# comment", "", "code_line"], 2),
        (["# comment1", "# comment2"], 2),  # Only comments
        ([], 0),  # Empty list
        (["", "   "], 2),  # Only whitespace
        (["\n", "code"], 1)
    ]
)
def test_find_start_of_code(lines, expected_index):
    """Tests the find_start_of_code function with various line inputs.

    This test uses parametrized inputs to verify the function correctly identifies
    the starting index of non-comment, non-whitespace code in different scenarios.

    Args:
        lines (list[str]): List of strings representing lines of a file.
        expected_index (int): The expected index where the code starts.
    """
    assert find_start_of_code(lines) == expected_index


def test_update_license_in_files(setup_test_directory):
    """Tests the update_license_in_files function by updating files in a test directory.

    This test verifies that:

    - Python files get the new license notice at the top while retaining their original content
    - Already licensed files are updated without duplicating the license
    - Non-Python files remain unmodified
    - Files in subdirectories are processed correctly
    - Empty files are handled appropriately

    Args:
        setup_test_directory (str): Pytest fixture that sets up a temporary test directory.
    """
    test_dir = setup_test_directory
    update_license_in_files(test_dir)

    # Check python files
    py_files_to_check = {
        "file_with_code.py": "print('Hello World')",
        "file_with_comments.py": "# This is a comment\n# Another comment",
        "file_with_mixed_content.py": "print('Code line')",  # Code starts after comment
        "empty_file.py": "",
        "subdir/sub_file.py": "print('Hello from sub dir')"
    }

    for py_file, original_code_start in py_files_to_check.items():
        filepath = os.path.join(test_dir, py_file)
        lines = read_file(filepath)
        file_content = "".join(lines)
        assert file_content.startswith(new_license_notice + '\n')
        if original_code_start:  # if not empty file
            # Ensure the original code (or comments if no code) is still there after the license
            assert original_code_start in file_content
        else:  # For empty_file.py
            assert file_content == new_license_notice + '\n'

    # Check already licensed file (should not add another license, but replace)
    already_licensed_filepath = os.path.join(test_dir, "already_licensed.py")
    already_licensed_lines = read_file(already_licensed_filepath)
    already_licensed_content = "".join(already_licensed_lines)
    assert already_licensed_content.startswith(new_license_notice + '\n')
    assert already_licensed_content.count(new_license_notice) == 1  # Only one notice
    assert "print('already licensed')" in already_licensed_content

    # Check non-python file (should not be modified)
    non_python_filepath = os.path.join(test_dir, "non_python_file.txt")
    non_python_content = "".join(read_file(non_python_filepath))
    assert non_python_content == "This is a text file."


# Remove placeholder test
# def test_placeholder():
# assert True