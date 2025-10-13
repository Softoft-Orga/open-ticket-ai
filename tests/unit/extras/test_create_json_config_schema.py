from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from open_ticket_ai.extras.create_json_config_schema import (
    RootConfig,
    format_default,
    generate_markdown_docs,
    generate_model_docs,
    generate_property_table,
    get_type_description,
)


def test_root_config_generates_schema() -> None:
    schema = RootConfig.model_json_schema()

    assert schema is not None
    assert isinstance(schema, dict)
    assert "$defs" in schema
    assert "properties" in schema


def test_get_type_description_simple_type() -> None:
    type_info = {"type": "string"}
    result = get_type_description(type_info)
    assert result == "string"


def test_get_type_description_list_types() -> None:
    type_info = {"type": ["string", "null"]}
    result = get_type_description(type_info)
    assert "string" in result
    assert "null" in result


def test_get_type_description_anyof() -> None:
    type_info = {"anyOf": [{"type": "string"}, {"type": "integer"}]}
    result = get_type_description(type_info)
    assert "string" in result
    assert "integer" in result


def test_get_type_description_ref() -> None:
    type_info = {"$ref": "#/$defs/SomeModel"}
    result = get_type_description(type_info)
    assert "SomeModel" in result
    assert result.startswith("[")
    assert result.endswith(")")


def test_format_default_string() -> None:
    result = format_default("test_value")
    assert result == '`"test_value"`'


def test_format_default_list() -> None:
    result = format_default(["item1", "item2"])
    assert result == '`["item1", "item2"]`'


def test_format_default_dict() -> None:
    result = format_default({"key": "value"})
    assert result == '`{"key": "value"}`'


def test_format_default_number() -> None:
    result = format_default(42)
    assert result == "`42`"


def test_format_default_boolean() -> None:
    result = format_default(True)
    assert result == "`True`"


def test_generate_property_table_empty() -> None:
    result = generate_property_table({}, [], {})
    assert "_No properties defined._" in result


def test_generate_property_table_with_properties() -> None:
    properties = {"test_prop": {"type": "string", "default": "test", "description": "A test property"}}
    required = ["test_prop"]
    result = generate_property_table(properties, required, {})

    assert "| Field | Type | Required | Default | Description |" in result
    assert "test_prop" in result
    assert "string" in result
    assert "✓" in result
    assert "test" in result


def test_generate_model_docs() -> None:
    schema = {"properties": {"field1": {"type": "string"}}, "required": ["field1"], "description": "Test model"}
    result = generate_model_docs("TestModel", schema, {}, level=2)

    assert "## TestModel" in result
    assert "Test model" in result
    assert "field1" in result


def test_generate_markdown_docs() -> None:
    schema = RootConfig.model_json_schema()
    result = generate_markdown_docs(schema)

    assert "# Configuration Schema Reference" in result
    assert "_Auto-generated from Pydantic models_" in result
    assert "## Root Configuration" in result
    assert "## Type Definitions" in result


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

    md_file = tmp_path / "CONFIG_SCHEMA.md"
    json_file = tmp_path / "config.schema.json"

    assert md_file.exists(), "CONFIG_SCHEMA.md should be created"
    assert json_file.exists(), "config.schema.json should be created"

    md_content = md_file.read_text(encoding="utf-8")
    assert "# Configuration Schema Reference" in md_content
    assert "## Root Configuration" in md_content

    json_content = json.loads(json_file.read_text(encoding="utf-8"))
    assert "$defs" in json_content
    assert "properties" in json_content


def test_generated_json_schema_structure() -> None:
    schema = RootConfig.model_json_schema()

    assert "properties" in schema
    assert "open_ticket_ai" in schema["properties"]
    assert "$defs" in schema

    open_ticket_ai_ref = schema["properties"]["open_ticket_ai"]
    assert "$ref" in open_ticket_ai_ref or "anyOf" in open_ticket_ai_ref or "allOf" in open_ticket_ai_ref


def test_markdown_docs_includes_definitions() -> None:
    schema = RootConfig.model_json_schema()
    result = generate_markdown_docs(schema)

    defs = schema.get("$defs", {})
    if defs:
        for def_name in list(defs.keys())[:3]:
            assert def_name in result
