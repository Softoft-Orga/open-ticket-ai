from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from open_ticket_ai.extras.create_json_config_schema import RootConfig, generate_markdown_docs


def test_root_config_generates_schema() -> None:
    schema = RootConfig.model_json_schema()
    assert schema is not None
    assert isinstance(schema, dict)
    assert "$defs" in schema
    assert "properties" in schema


def test_generate_markdown_docs() -> None:
    schema = RootConfig.model_json_schema()
    result = generate_markdown_docs(schema)
    assert "# Configuration Schema Reference" in result
    assert "## Root Configuration" in result


def test_nested_structure_generation() -> None:
    schema = RootConfig.model_json_schema()
    result = generate_markdown_docs(schema)

    # Check for indented fields (nested structure)
    # Pattern: lines with 2+ spaces before backtick indicate nested fields
    nested_pattern = re.compile(r"\|\s{2,}`\w+`\s*\|")
    nested_fields = nested_pattern.findall(result)
    assert len(nested_fields) > 0, "Should have nested fields with indentation"

    # Check Type Definitions section exists
    assert "## Type Definitions" in result

    # Check table structure is present
    assert "| Field | Type | Required | Default | Description |" in result


def test_main_execution_creates_files(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "open_ticket_ai.extras.create_json_config_schema"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0
    assert (tmp_path / "CONFIG_SCHEMA.md").exists()
    assert (tmp_path / "config.schema.json").exists()
