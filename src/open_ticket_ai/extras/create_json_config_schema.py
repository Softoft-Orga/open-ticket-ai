import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


class RootConfig(BaseModel):
    open_ticket_ai: RawOpenTicketAIConfig


def _get_type_str(type_info: dict[str, Any], defs: dict[str, Any]) -> str:
    if "type" in type_info:
        t = type_info["type"]
        if isinstance(t, list):
            return " or ".join(str(x) for x in t)
        if t == "array" and "items" in type_info:
            items = type_info["items"]
            if "$ref" in items:
                name = items["$ref"].split("/")[-1]
                return f"array of [{name}](#{name.lower()})"
            return f"array of {_get_type_str(items, defs)}"
        return str(t)
    if "anyOf" in type_info:
        return " or ".join(_get_type_str(t, defs) for t in type_info["anyOf"])
    if "$ref" in type_info:
        name = type_info["$ref"].split("/")[-1]
        return f"[{name}](#{name.lower()})"
    return "any"


def _add_row(prop_name: str, prop_info: dict[str, Any], required: list[str], defs: dict[str, Any], indent: int) -> str:
    req = "✓" if prop_name in required else ""
    type_str = _get_type_str(prop_info, defs)
    default = prop_info.get("default", "")
    if default:
        default = f'`"{default}"`' if isinstance(default, str) else f"`{json.dumps(default)}`"
    desc = prop_info.get("description", "").replace("\n", " ")
    return f"| {'  ' * indent}`{prop_name}` | {type_str} | {req} | {default} | {desc} |"


def _expand_props(
    props: dict[str, Any], req: list[str], defs: dict[str, Any], indent: int, max_depth: int
) -> list[str]:
    rows = []
    for name, info in props.items():
        rows.append(_add_row(name, info, req, defs, indent))
        if indent < max_depth:
            ref = info.get("$ref") or (info.get("items", {}).get("$ref") if info.get("type") == "array" else None)
            if ref:
                ref_schema = defs.get(ref.split("/")[-1], {})
                if "properties" in ref_schema:
                    nested = _expand_props(
                        ref_schema["properties"],
                        ref_schema.get("required", []),
                        defs,
                        indent + 1,
                        max_depth,
                    )
                    rows.extend(nested)
    return rows


def generate_markdown_docs(schema: dict[str, Any]) -> str:
    defs = schema.get("$defs", {})
    props = schema.get("properties", {})
    req = schema.get("required", [])

    lines = [
        "# Configuration Schema Reference\n",
        "_Auto-generated from Pydantic models_\n",
        "---\n",
        "## Root Configuration\n",
    ]

    if props:
        lines.extend([
            "| Field | Type | Required | Default | Description |",
            "|-------|------|----------|---------|-------------|",
        ])
        lines.extend(_expand_props(props, req, defs, 0, 3))

    if defs:
        lines.append("\n## Type Definitions\n")
        for name, def_schema in sorted(defs.items()):
            lines.append(f"### {name}\n")
            if "description" in def_schema:
                lines.append(f"{def_schema['description']}\n")
            def_props = def_schema.get("properties", {})
            if def_props:
                lines.extend([
                    "| Field | Type | Required | Default | Description |",
                    "|-------|------|----------|---------|-------------|",
                ])
                lines.extend(_expand_props(def_props, def_schema.get("required", []), defs, 0, 0))
            lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    schema: dict[str, Any] = RootConfig.model_json_schema()
    generate_markdown_docs(schema)
    with open(Path.cwd() / "CONFIG_SCHEMA.md", "w", encoding="utf-8") as f:
        f.write(generate_markdown_docs(schema))
    with open(Path.cwd() / "config.schema.json", "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
