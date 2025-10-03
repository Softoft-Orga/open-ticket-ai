from __future__ import annotations
import re
from typing import Any, Sequence

def sanitize_token(raw: str) -> str:
    token = re.sub(r"[^0-9A-Za-z_]+", "_", str(raw))
    token = re.sub(r"_+", "_", token).strip("_")
    if not token:
        token = "node"
    if token[0].isdigit():
        token = f"n_{token}"
    return token

def make_global_identifier(path_parts: Sequence[str]) -> str:
    return "__".join(sanitize_token(p) for p in path_parts)

def format_node_label(primary: str, step_data: dict[str, Any]) -> str:
    lines: list[str] = []
    if primary:
        lines.append(primary)
    use_value = step_data.get("use")
    if isinstance(use_value, str) and use_value and use_value != primary:
        lines.append(use_value)
    condition_value = step_data.get("if")
    if isinstance(condition_value, str) and condition_value:
        lines.append(f"if {condition_value}")
    return "<br/>".join(lines)

def build_composite_ports(global_path: list[str]) -> tuple[str, str]:
    entry_identifier = make_global_identifier([*global_path, "entry"])
    exit_identifier = make_global_identifier([*global_path, "exit"])
    return entry_identifier, exit_identifier

def sanitize_for_mermaid_label(text: str) -> str:
    s = text.replace("\\", "\\\\")
    s = s.replace("\n", "<br/>")
    s = s.replace("[", "&#91;").replace("]", "&#93;")
    s = s.replace("{", "&#123;").replace("}", "&#125;")
    s = s.replace("|", "&#124;")
    return s
