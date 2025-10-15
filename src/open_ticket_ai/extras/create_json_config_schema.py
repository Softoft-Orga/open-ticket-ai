import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


class RootConfig(BaseModel):
    open_ticket_ai: RawOpenTicketAIConfig


def format_default(value: Any) -> str:
    if isinstance(value, str):
        return f'`"{value}"`'
    if isinstance(value, (list, dict)):
        return f"`{json.dumps(value)}`"
    return f"`{value}`"


def resolve_ref(ref: str, defs: dict[str, Any]) -> dict[str, Any] | None:
    if ref.startswith("#/$defs/"):
        return defs.get(ref.split("/")[-1])
    return None


def get_type_description(schema: dict[str, Any], defs: dict[str, Any]) -> str:
    if "$ref" in schema:
        name = schema["$ref"].split("/")[-1]
        return f"[{name}](#{name.lower()})"
    if "anyOf" in schema:
        return " or ".join(get_type_description(s, defs) for s in schema["anyOf"])
    if "oneOf" in schema:
        return " or ".join(get_type_description(s, defs) for s in schema["oneOf"])
    if schema.get("allOf"):
        return " & ".join(get_type_description(s, defs) for s in schema["allOf"])
    t = schema.get("type")
    if isinstance(t, list):
        return " or ".join(str(x) for x in t)
    if t == "array":
        items = schema.get("items", {})
        if "$ref" in items:
            name = items["$ref"].split("/")[-1]
            return f"array of [{name}](#{name.lower()})"
        return f"array of {get_type_description(items, defs)}"
    if t:
        return str(t)
    return "any"


def generate_property_table(
    properties: dict[str, Any],
    required: list[str],
    defs: dict[str, Any],
    indent_level: int = 0,
    max_depth: int = 3,
) -> str:
    if not properties:
        return "_No properties defined._\n"

    lines: list[str] = []
    if indent_level == 0:
        lines.extend(
            [
                "| Field | Type | Required | Default | Description |",
                "|-------|------|----------|---------|-------------|",
            ]
        )

    for prop_name, prop_info in properties.items():
        is_required = "✓" if prop_name in required else ""
        type_desc = get_type_description(prop_info, defs)
        default_str = format_default(prop_info["default"]) if "default" in prop_info else ""
        description = str(prop_info.get("description", "")).replace("\n", " ")

        indent = "  " * indent_level
        prefix = "└─ " if indent_level > 0 else ""
        field_name = f"{indent}{prefix}`{prop_name}`"

        lines.append(f"| {field_name} | {type_desc} | {is_required} | {default_str} | {description} |")

        if indent_level >= max_depth:
            continue

        nested_schema: dict[str, Any] | None = None
        if "$ref" in prop_info:
            nested_schema = resolve_ref(prop_info["$ref"], defs)
        elif prop_info.get("type") == "array" and isinstance(prop_info.get("items"), dict):
            items = prop_info["items"]
            if "$ref" in items:
                nested_schema = resolve_ref(items["$ref"], defs)
            elif items.get("type") == "object" and "properties" in items:
                nested_schema = items
        elif prop_info.get("type") == "object" and "properties" in prop_info:
            nested_schema = prop_info
        elif "allOf" in prop_info:
            for s in prop_info["allOf"]:
                if "$ref" in s:
                    nested_schema = resolve_ref(s["$ref"], defs)
                    if nested_schema:
                        break

        if nested_schema and "properties" in nested_schema:
            nested_props = nested_schema.get("properties", {})
            nested_required = nested_schema.get("required", [])
            nested_block = generate_property_table(
                nested_props,
                nested_required,
                defs,
                indent_level + 1,
                max_depth,
            )
            lines.extend(
                [
                    line
                    for line in nested_block.split("\n")
                    if line and not line.startswith("|----") and not line.startswith("| Field")
                ]
            )

    return "\n".join(lines) + "\n"


def generate_model_docs(name: str, schema: dict[str, Any], defs: dict[str, Any], level: int = 2) -> str:
    heading = "#" * level
    lines = [f"{heading} {name}\n"]
    if "description" in schema:
        lines.append(f"{schema['description']}\n")
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    lines.append(generate_property_table(properties, required, defs))
    return "\n".join(lines) + "\n"


def generate_markdown_docs(schema: dict[str, Any]) -> str:
    defs = schema.get("$defs", {})
    lines = [
        "# Configuration Schema Reference\n",
        "_Auto-generated from Pydantic models_\n",
        "---\n",
    ]
    lines.append(generate_model_docs("Root Configuration", schema, defs, level=2))
    if defs:
        lines.append("## Type Definitions\n")
        for def_name, def_schema in sorted(defs.items()):
            lines.append(generate_model_docs(def_name, def_schema, defs, level=3))
    return "\n".join(lines)


if __name__ == "__main__":
    schema: dict[str, Any] = RootConfig.model_json_schema()
    md = generate_markdown_docs(schema)
    Path("CONFIG_SCHEMA.md").write_text(md, encoding="utf-8")
    Path("config.schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
