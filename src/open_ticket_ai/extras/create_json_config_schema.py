import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


class RootConfig(BaseModel):
    open_ticket_ai: RawOpenTicketAIConfig


def get_type_description(type_info: dict[str, Any]) -> str:
    if "type" in type_info:
        type_val = type_info["type"]
        if isinstance(type_val, list):
            return " or ".join(str(t) for t in type_val)
        return str(type_val)

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
    if isinstance(default, str):
        return f'`"{default}"`'
    if isinstance(default, (list, dict)):
        return f"`{json.dumps(default)}`"
    return f"`{default}`"


def resolve_ref(ref: str, defs: dict[str, Any]) -> dict[str, Any] | None:
    if ref.startswith("#/$defs/"):
        ref_name = ref.split("/")[-1]
        return defs.get(ref_name)
    return None


def generate_property_table(
    properties: dict[str, Any],
    required: list[str],
    defs: dict[str, Any],
    indent_level: int = 0,
    max_depth: int = 3,
) -> str:
    if not properties:
        return "_No properties defined._\n"

    lines = []
    if indent_level == 0:
        lines.extend([
            "| Field | Type | Required | Default | Description |",
            "|-------|------|----------|---------|-------------|",
        ])

    prop_items = list(properties.items())
    for _idx, (prop_name, prop_info) in enumerate(prop_items):
        is_required = "✓" if prop_name in required else ""

        type_desc = get_type_description(prop_info)

        default = prop_info.get("default", "")
        if default:
            default = format_default(default)

        description = prop_info.get("description", "").replace("\n", " ")

        indent = "  " * indent_level
        prefix = "└─ " if indent_level > 0 else ""
        field_name = f"{indent}{prefix}`{prop_name}`"

        lines.append(f"| {field_name} | {type_desc} | {is_required} | {default} | {description} |")

        if indent_level < max_depth:
            nested_schema = None
            if "$ref" in prop_info:
                nested_schema = resolve_ref(prop_info["$ref"], defs)
            elif "items" in prop_info and isinstance(prop_info["items"], dict):
                if "$ref" in prop_info["items"]:
                    nested_schema = resolve_ref(prop_info["items"]["$ref"], defs)
            elif "allOf" in prop_info and len(prop_info["allOf"]) > 0 and "$ref" in prop_info["allOf"][0]:
                nested_schema = resolve_ref(prop_info["allOf"][0]["$ref"], defs)

            if nested_schema and "properties" in nested_schema:
                nested_properties = nested_schema.get("properties", {})
                nested_required = nested_schema.get("required", [])
                if nested_properties:
                    nested_lines = generate_property_table(
                        nested_properties,
                        nested_required,
                        defs,
                        indent_level + 1,
                        max_depth,
                    )
                    lines.extend([
                        line
                        for line in nested_lines.split("\n")
                        if line and not line.startswith("|----") and not line.startswith("| Field")
                    ])

    return "\n".join(lines) + "\n"


def generate_model_docs(
    name: str, schema: dict[str, Any], defs: dict[str, Any], level: int = 2
) -> str:
    heading = "#" * level
    lines = [f"{heading} {name}\n"]

    if "description" in schema:
        lines.append(f"{schema['description']}\n")

    properties = schema.get("properties", {})
    required = schema.get("required", [])

    lines.append(generate_property_table(properties, required, defs))

    return "\n".join(lines) + "\n"


def generate_markdown_docs(schema: dict[str, Any]) -> str:
    lines = [
        "# Configuration Schema Reference\n",
        "_Auto-generated from Pydantic models_\n",
        "---\n",
    ]

    defs = schema.get("$defs", {})

    lines.append(generate_model_docs("Root Configuration", schema, defs))

    if defs:
        lines.append("## Type Definitions\n")
        for def_name, def_schema in sorted(defs.items()):
            lines.append(generate_model_docs(def_name, def_schema, defs, level=3))

    return "\n".join(lines)


if __name__ == "__main__":
    schema: dict[str, Any] = RootConfig.model_json_schema()
    generate_markdown_docs(schema)
    with open(Path.cwd() / "CONFIG_SCHEMA.md", "w", encoding="utf-8") as f:
        f.write(generate_markdown_docs(schema))
    with open(Path.cwd() / "config.schema.json", "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
