import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


class RootConfig(BaseModel):
    open_ticket_ai: RawOpenTicketAIConfig


def resolve_ref(ref: str, defs: dict[str, Any]) -> dict[str, Any] | None:
    ref_name = ref.split("/")[-1]
    return defs.get(ref_name)


def get_type_description(type_info: dict[str, Any], defs: dict[str, Any]) -> str:
    if "type" in type_info:
        type_val = type_info["type"]
        if isinstance(type_val, list):
            return " or ".join(str(t) for t in type_val)
        if type_val == "array":
            items = type_info.get("items", {})
            if "$ref" in items:
                ref_name = items["$ref"].split("/")[-1]
                return f"array of [{ref_name}](#{ref_name.lower()})"
            item_type = get_type_description(items, defs)
            return f"array of {item_type}"
        return str(type_val)

    if "anyOf" in type_info:
        types = [get_type_description(t, defs) for t in type_info["anyOf"]]
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


def _expand_nested_ref(
    ref: str, defs: dict[str, Any], indent: int, max_depth: int
) -> list[str]:
    ref_schema = resolve_ref(ref, defs)
    if not ref_schema or "properties" not in ref_schema:
        return []

    nested_props = ref_schema.get("properties", {})
    nested_required = ref_schema.get("required", [])
    if not nested_props:
        return []

    return generate_nested_properties(nested_props, nested_required, defs, indent, max_depth)


def generate_property_table(
    properties: dict[str, Any],
    required: list[str],
    defs: dict[str, Any],
    indent: int = 0,
    max_depth: int = 3,
) -> str:
    if not properties:
        return "_No properties defined._\n"

    lines = [
        "| Field | Type | Required | Default | Description |",
        "|-------|------|----------|---------|-------------|",
    ]

    for prop_name, prop_info in properties.items():
        is_required = "✓" if prop_name in required else ""
        type_desc = get_type_description(prop_info, defs)
        default = format_default(prop_info.get("default", "")) if prop_info.get("default", "") else ""
        description = prop_info.get("description", "").replace("\n", " ")
        indent_prefix = "  " * indent
        field_name = f"{indent_prefix}`{prop_name}`"

        lines.append(f"| {field_name} | {type_desc} | {is_required} | {default} | {description} |")

        if indent >= max_depth:
            continue

        if "$ref" in prop_info:
            nested_lines = _expand_nested_ref(prop_info["$ref"], defs, indent + 1, max_depth)
            lines.extend(nested_lines)
        elif prop_info.get("type") == "array" and "$ref" in prop_info.get("items", {}):
            nested_lines = _expand_nested_ref(prop_info["items"]["$ref"], defs, indent + 1, max_depth)
            lines.extend(nested_lines)

    return "\n".join(lines) + "\n"


def generate_nested_properties(
    properties: dict[str, Any],
    required: list[str],
    defs: dict[str, Any],
    indent: int,
    max_depth: int,
) -> list[str]:
    lines = []

    for prop_name, prop_info in properties.items():
        is_required = "✓" if prop_name in required else ""
        type_desc = get_type_description(prop_info, defs)
        default = format_default(prop_info.get("default", "")) if prop_info.get("default", "") else ""
        description = prop_info.get("description", "").replace("\n", " ")
        indent_prefix = "  " * indent
        field_name = f"{indent_prefix}`{prop_name}`"

        lines.append(f"| {field_name} | {type_desc} | {is_required} | {default} | {description} |")

        if indent >= max_depth:
            continue

        if "$ref" in prop_info:
            nested_lines = _expand_nested_ref(prop_info["$ref"], defs, indent + 1, max_depth)
            lines.extend(nested_lines)
        elif prop_info.get("type") == "array" and "$ref" in prop_info.get("items", {}):
            nested_lines = _expand_nested_ref(prop_info["items"]["$ref"], defs, indent + 1, max_depth)
            lines.extend(nested_lines)

    return lines


def generate_model_docs(
    name: str,
    schema: dict[str, Any],
    defs: dict[str, Any],
    level: int = 2,
    expand_nested: bool = True,
) -> str:
    heading = "#" * level
    lines = [f"{heading} {name}\n"]

    if "description" in schema:
        lines.append(f"{schema['description']}\n")

    properties = schema.get("properties", {})
    required = schema.get("required", [])

    if expand_nested:
        lines.append(generate_property_table(properties, required, defs))
    else:
        lines.append(generate_property_table(properties, required, defs, max_depth=0))

    return "\n".join(lines) + "\n"


def generate_markdown_docs(schema: dict[str, Any]) -> str:
    lines = [
        "# Configuration Schema Reference\n",
        "_Auto-generated from Pydantic models_\n",
        "---\n",
    ]

    defs = schema.get("$defs", {})

    lines.append(generate_model_docs("Root Configuration", schema, defs, expand_nested=True))

    if defs:
        lines.append("## Type Definitions\n")
        for def_name, def_schema in sorted(defs.items()):
            lines.append(generate_model_docs(def_name, def_schema, defs, level=3, expand_nested=False))

    return "\n".join(lines)


if __name__ == "__main__":
    schema: dict[str, Any] = RootConfig.model_json_schema()
    generate_markdown_docs(schema)
    with open(Path.cwd() / "CONFIG_SCHEMA.md", "w", encoding="utf-8") as f:
        f.write(generate_markdown_docs(schema))
    with open(Path.cwd() / "config.schema.json", "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
