import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


class RootConfig(BaseModel):
    open_ticket_ai: RawOpenTicketAIConfig


def get_type_description(type_info: dict[str, Any]) -> str:
    """Convert JSON Schema type info to human-readable string."""
    if "type" in type_info:
        type_val = type_info["type"]
        if isinstance(type_val, list):
            return " or ".join(type_val)
        return type_val

    if "anyOf" in type_info:
        types = [get_type_description(t) for t in type_info["anyOf"]]
        return " or ".join(types)

    if "allOf" in type_info:
        return "object"

    if "$ref" in type_info:
        ref_name = type_info["$ref"].split("/")[-1]
        return f"[{ref_name}](#{ref_name.lower()})"

    return "any"


def format_default(default: Any) -> str:
    """Format default value for display."""
    if isinstance(default, str):
        return f'`"{default}"`'
    if isinstance(default, (list, dict)):
        return f"`{json.dumps(default)}`"
    return f"`{default}`"


def generate_property_table(properties: dict[str, Any], required: list[str], defs: dict[str, Any]) -> str:
    """Generate a Markdown table for properties."""
    if not properties:
        return "_No properties defined._\n"

    lines = [
        "| Field | Type | Required | Default | Description |",
        "|-------|------|----------|---------|-------------|",
    ]

    for prop_name, prop_info in properties.items():
        is_required = "✓" if prop_name in required else ""

        # Get type
        type_desc = get_type_description(prop_info)

        # Get default
        default = prop_info.get("default", "")
        if default:
            default = format_default(default)

        # Get description
        description = prop_info.get("description", "").replace("\n", " ")

        lines.append(f"| `{prop_name}` | {type_desc} | {is_required} | {default} | {description} |")

    return "\n".join(lines) + "\n"


def generate_model_docs(name: str, schema: dict[str, Any], defs: dict[str, Any], level: int = 2) -> str:
    """Generate documentation for a single model."""
    heading = "#" * level
    lines = [f"{heading} {name}\n"]

    if "description" in schema:
        lines.append(f"{schema['description']}\n")

    properties = schema.get("properties", {})
    required = schema.get("required", [])

    lines.append(generate_property_table(properties, required, defs))

    return "\n".join(lines) + "\n"


def generate_markdown_docs(schema: dict[str, Any]) -> str:
    """Generate complete Markdown documentation from JSON Schema."""
    lines = [
        "# Configuration Schema Reference\n",
        "_Auto-generated from Pydantic models_\n",
        "---\n",
    ]

    defs = schema.get("$defs", {})

    # Generate root config
    lines.append(generate_model_docs("Root Configuration", schema, defs, level=2))

    # Generate definitions
    if defs:
        lines.append("## Type Definitions\n")
        for def_name, def_schema in sorted(defs.items()):
            lines.append(generate_model_docs(def_name, def_schema, defs, level=3))

    return "\n".join(lines)


if __name__ == "__main__":
    """Generates JSON schema for RootConfig and writes it to config.schema.json."""
    schema: dict = RootConfig.model_json_schema()
    generate_markdown_docs(schema)  # for side effects, if needed
    with open(Path.cwd() / "CONFIG_SCHEMA.md", "w", encoding="utf-8") as f:
        f.write(generate_markdown_docs(schema))
    with open(Path.cwd() / "config.schema.json", "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
