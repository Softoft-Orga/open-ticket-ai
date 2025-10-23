import json
from pathlib import Path
from typing import Any

from tabulate import tabulate

from open_ticket_ai.core.config.config_models import OpenTicketAIConfig


def load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ref_name(ref: str) -> str:
    return ref.split("/")[-1]


def unwrap_ref(node: dict[str, Any], defs: dict[str, Any], seen: set[str] | None = None) -> dict[str, Any]:
    seen = seen or set()
    while "$ref" in node:
        name = ref_name(node["$ref"])
        if name in seen:
            break
        seen.add(name)
        node = defs.get(name, node)
    return node


def type_str(node: dict[str, Any], defs: dict[str, Any]) -> str:
    if "$ref" in node:
        name = ref_name(node["$ref"])
        return f"[{name}](#{name.lower()})"
    if "enum" in node:
        return "enum " + ", ".join(f"`{x}`" for x in node["enum"])
    if "const" in node:
        return f"const `{node['const']}`"
    if "anyOf" in node:
        return " or ".join(type_str(x, defs) for x in node["anyOf"])
    if "oneOf" in node:
        return " | ".join(type_str(x, defs) for x in node["oneOf"])
    if "allOf" in node:
        return " & ".join(type_str(x, defs) for x in node["allOf"])
    t = node.get("type")
    if isinstance(t, list):
        return " or ".join(t)
    if t == "array":
        items = node.get("items", {})
        return f"array of {type_str(items, defs) if items else 'any'}"
    if t == "object" or "properties" in node:
        return "object"
    if "format" in node:
        return node["format"]
    return "any"


def default_str(node: dict[str, Any]) -> str:
    if "default" in node:
        v = node["default"]
        return "`null`" if v is None else f"`{v}`"
    return ""


def desc_str(node: dict[str, Any]) -> str:
    d = node.get("description") or node.get("title") or ""
    return str(d).replace("\n", " ").strip()


def flatten(
    node: dict[str, Any],
    defs: dict[str, Any],
    base: str = "",
    required: bool = False,
    seen_nodes: set[int] | None = None,
) -> list[tuple[str, str, str, str, str]]:
    seen_nodes = seen_nodes or set()
    n = unwrap_ref(node, defs)
    if id(n) in seen_nodes:
        return []
    seen_nodes.add(id(n))
    rows: list[tuple[str, str, str, str, str]] = []
    t = type_str(n, defs)
    d = desc_str(n)
    dv = default_str(n)
    if base:
        rows.append((f"`{base}`", t, "✓" if required else "", dv, d))
    if n.get("type") == "object" or "properties" in n:
        req = set(n.get("required", []))
        props = n.get("properties", {})
        for name, prop in props.items():
            child_path = f"{base}.{name}" if base else name
            rows.extend(flatten(prop, defs, child_path, name in req, seen_nodes))
    elif n.get("type") == "array":
        items = n.get("items", {})
        child_path = f"{base}[]" if base else "[]"
        if isinstance(items, dict):
            rows.extend(flatten(items, defs, child_path, required, seen_nodes))
    return rows


def root_node(schema: dict[str, Any], defs: dict[str, Any]) -> dict[str, Any]:
    if "$ref" in schema:
        return unwrap_ref({"$ref": schema["$ref"]}, defs)
    return schema


def generate_markdown_single_table(schema: dict[str, Any]) -> str:
    defs = schema.get("$defs") or schema.get("definitions") or {}
    title = schema.get("title") or "Schema"
    root = root_node(schema, defs)
    rows = flatten(root, defs)
    header = ["Attribute", "type", "required", "default", "description"]
    table = tabulate(rows, headers=header, tablefmt="github") if rows else "_No Fields_"
    return f"# {title}\n\n{table}\n"


def main() -> None:
    schema = OpenTicketAIConfig.model_json_schema()
    md = generate_markdown_single_table(schema)
    Path("schema.md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
