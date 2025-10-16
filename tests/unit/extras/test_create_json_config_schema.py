from __future__ import annotations

from scripts.create_json_config_schema import RootConfig, generate_markdown_docs


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


def test_nested_structure_in_markdown() -> None:
    schema = RootConfig.model_json_schema()
    result = generate_markdown_docs(schema)
    assert "└─ `plugins`" in result
    assert "└─ `infrastructure`" in result
    assert "    └─ `logging`" in result or "  └─ `logging`" in result
