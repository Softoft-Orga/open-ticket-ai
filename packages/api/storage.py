"""Storage helpers for reading and writing text files."""

from pathlib import Path


def read_text_file(file_path: Path | str) -> str:
    """Read text content from a file.

    Args:
        file_path: Path to the file to read

    Returns:
        String content of the file

    Raises:
        FileNotFoundError: If the file does not exist
        IOError: If there's an error reading the file
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with path.open("r", encoding="utf-8") as f:
        return f.read()


def write_text_file(file_path: Path | str, content: str) -> None:
    """Write text content to a file.

    Args:
        file_path: Path to the file to write
        content: String content to write

    Raises:
        IOError: If there's an error writing the file
    """
    path = Path(file_path)

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        f.write(content)
