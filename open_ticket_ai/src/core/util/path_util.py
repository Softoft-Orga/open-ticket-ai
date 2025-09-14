# FILE_PATH: open_ticket_ai\src\ce\core\util\path_util.py
from pathlib import Path


def find_python_code_root_path(project_name: str = 'open_ticket_ai') -> Path:
    start_path = Path(__file__).resolve()
    for parent in [start_path, *start_path.parents]:
        if parent.name == project_name:
            return parent
    raise FileNotFoundError(f"Project folder '{project_name}' not found in parents of {start_path}")
