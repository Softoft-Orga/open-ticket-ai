"""Path utility functions for the Open Ticket AI project."""

from pathlib import Path


def find_python_code_root_path() -> Path:
    """
    Find the root path of the Python source code (src directory).

    Returns:
        Path: The path to the src directory containing open_ticket_ai package.
    """
    current_file = Path(__file__).resolve()
    src_dir = current_file.parent.parent.parent.parent
    
    if not (src_dir / "open_ticket_ai").exists():
        msg = f"Could not find open_ticket_ai package in expected location: {src_dir}"
        raise RuntimeError(msg)
    
    return src_dir / "open_ticket_ai"
