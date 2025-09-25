"""Script to update license notices in Python files within a specified directory.

This script walks through all Python files in a given directory and replaces
any existing license notice at the top of the file with a new license notice.
Non-comment code and empty/whitespace-only files are handled appropriately.
"""
import datetime
import os

# Path to the directory containing Python files to update
directory_path = 'src'
"""str: Path to the directory containing Python files to update."""

# The new license notice text to insert at the top of files
current_year = datetime.datetime.now().year
"""int: The current year used in the license notice."""

#: str: The new license notice text to insert at the top of files.
new_license_notice = f"""# Copyright (c) {current_year} by Softoft, Tobias Bueck Einzelunternehmen
# This code is part of the Open Ticket AI and is governed
# by its license agreement. Full license in LICENSE_DE.md / LICENSE_EN.md.
"""


def find_start_of_code(lines):
    """Return the index of the first non-comment line.

    Scans through lines until it finds the first line that contains non-whitespace
    characters and doesn't start with a '#' comment marker.

    Args:
        lines (list): List of strings representing lines in a file.

    Returns:
        int: Index of the first line that is not a comment or whitespace.
            Returns len(lines) if no such line exists.
    """
    for i, line in enumerate(lines):
        if line.strip() and not line.strip().startswith('#'):
            return i
    return len(lines)


def read_file(filepath):
    """Read all lines from ``filepath``.

    Opens the specified file in read mode and returns all lines as a list of strings.

    Args:
        filepath (str): Path to the file to read.

    Returns:
        list: List of strings representing lines in the file.
    """
    with open(filepath) as file:
        return file.readlines()


def write_file(filepath, lines):
    """Write ``lines`` to ``filepath``.

    Opens the specified file in write mode and writes all lines to it.

    Args:
        filepath (str): Path to the file to write.
        lines (list): List of strings to write to the file.
    """
    with open(filepath, 'w') as file:
        file.writelines(lines)


def update_license_in_files(directory):
    """Inserts the license notice at the top of all `.py` files.

    Walks through all Python files in the specified directory and inserts the new license notice.
    The function removes any leading comments and blank lines (which typically include the old license)
    and replaces them with the new license notice, except in the case where the file consists entirely
    of comments and blank lines (and is not empty or entirely whitespace). In that case, the new license
    is inserted at the top and the existing comments and blank lines are preserved below.

    For empty files or files containing only whitespace, the license notice is inserted and the rest of
    the file remains empty.

    Args:
        directory (str): Path to the directory containing files to update.

    Note:
        This function modifies the files in-place. It is recommended to have backups before running.
    """
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            if not filename.endswith(".py"):
                continue
            filepath = os.path.join(subdir, filename)
            lines = read_file(filepath)
            start_of_code = find_start_of_code(lines)

            # Check if the file is empty or contains only whitespace
            is_empty_or_whitespace_only = not any(line.strip() for line in lines)

            if start_of_code == len(lines) and not is_empty_or_whitespace_only:
                # File contains only comments (and possibly blank lines)
                updated_lines = [new_license_notice + '\n'] + lines
            else:
                # File has executable code, or is empty/whitespace only
                # For empty/whitespace only files, lines[start_of_code:] will be empty,
                # so only license notice is added, which is correct.
                updated_lines = [new_license_notice + '\n'] + lines[start_of_code:]

            write_file(filepath, updated_lines)
            print(f'Updated license in {filepath}')


if __name__ == '__main__':
    update_license_in_files(directory_path)
