from __future__ import annotations

import subprocess
from pathlib import Path
from textwrap import dedent

import pytest


@pytest.fixture
def sample_python_file(tmp_path: Path) -> Path:
    file_path = tmp_path / "test_module.py"
    content = dedent("""
        from scripts.pdgen.decorator import include_in_uml

        @include_in_uml
        class Vehicle:
            pass

        class Car(Vehicle):
            pass
        
        @include_in_uml
        class Bike(Vehicle):
            pass
    """)
    file_path.write_text(content)
    return file_path


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).parent.parent.parent.parent


def test_pdgen_cli_with_file(sample_python_file: Path, repo_root: Path):
    result = subprocess.run(
        ["python", str(repo_root / "scripts" / "pdgen_cli.py"), str(sample_python_file)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    output = result.stdout

    assert "@startuml" in output
    assert "@enduml" in output
    assert "class Vehicle <<@include_in_uml>>" in output
    assert "class Bike <<@include_in_uml>>" in output
    assert "class Car" in output
    assert "Vehicle <|-- Car" in output
    assert "Vehicle <|-- Bike" in output


def test_pdgen_cli_with_output_file(sample_python_file: Path, tmp_path: Path, repo_root: Path):
    output_file = tmp_path / "diagram.puml"

    result = subprocess.run(
        [
            "python",
            str(repo_root / "scripts" / "pdgen_cli.py"),
            str(sample_python_file),
            "-o",
            str(output_file),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert output_file.exists()

    content = output_file.read_text()
    assert "@startuml" in content
    assert "@enduml" in content
    assert "class Vehicle <<@include_in_uml>>" in content


def test_pdgen_cli_with_nonexistent_file(repo_root: Path):
    result = subprocess.run(
        ["python", str(repo_root / "scripts" / "pdgen_cli.py"), "/nonexistent/path.py"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "does not exist" in result.stdout
