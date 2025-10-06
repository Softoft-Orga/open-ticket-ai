from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from open_ticket_ai.core.pipeline.pipe_config import RawPipeConfig
from open_ticket_ai.tools.mermaid_conversion.utils import _make_global_identifier, _sanitize_mermaid_label


@dataclass
class NodeDef:
    identifier: str
    label: str
    kind: str


class NodeRenderer:
    @staticmethod
    def render(node: NodeDef) -> str:
        label = _sanitize_mermaid_label(node.label or " ")
        if node.kind == "start":
            return f'    {node.identifier}(["{label}"])'
        if node.kind == "hidden":
            return f'    {node.identifier}[" "]:::hidden'
        return f'    {node.identifier}["{label}"]:::step'


def build_node_from_pipe(step_dict: dict[str, Any], path_stack: list[str], index: int) -> NodeDef | None:
    if _is_composite(step_dict):
        return None
    raw = RawPipeConfig.model_validate(step_dict)
    display_name = _choose_display_name(step_dict, index)
    global_identifier = _make_global_identifier([*path_stack, display_name])
    label = _format_node_label(display_name, step_dict)
    kind = "process"
    return NodeDef(global_identifier, label, kind)


def _is_composite(step_dict: dict[str, Any]) -> bool:
    return isinstance(step_dict.get("steps"), list)


def _choose_display_name(step_dict: dict[str, Any], index: int) -> str:
    v = step_dict.get("id")
    if isinstance(v, str) and v:
        return v
    u = step_dict.get("use")
    if isinstance(u, str) and u:
        return u.split(":")[-1]
    return f"step_{index}"


def _format_node_label(primary: str, step_dict: dict[str, Any]) -> str:
    lines: list[str] = []
    if primary:
        lines.append(primary)
    u = step_dict.get("use")
    u = u.split(":")[-1] if isinstance(u, str) else u
    if isinstance(u, str) and u and u != primary:
        lines.append(u)
    cond = step_dict.get("if")
    if isinstance(cond, str) and cond:
        cond = cond.replace("{{", "").replace("}}", "").strip() if isinstance(cond, str) else ""
        lines.append(f"if {cond}")
    return "<br/>".join(lines)
