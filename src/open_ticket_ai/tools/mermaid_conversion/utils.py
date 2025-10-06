from __future__ import annotations

import re
from typing import Sequence


def _make_global_identifier(parts: Sequence[str]) -> str:
    return "__".join(_sanitize_token(p) for p in parts)


def sanitize_token(raw: str) -> str:
    token = re.sub(r"[^0-9A-Za-z_]+", "_", str(raw))
    token = re.sub(r"_+", "_", token).strip("_")
    if not token:
        token = "node"
    if token[0].isdigit():
        token = f"n_{token}"
    return token


def build_composite_ports(global_path: list[str]) -> tuple[str, str]:
    entry_identifier = _make_global_identifier([*global_path, "entry"])
    exit_identifier = _make_global_identifier([*global_path, "exit"])
    return entry_identifier, exit_identifier


def sanitize_for_mermaid_label(text: str) -> str:
    s = text.replace("\\", "\\\\")
    s = s.replace("\n", "<br/>")
    s = s.replace("[", "&#91;").replace("]", "&#93;")
    s = s.replace("{", "&#123;").replace("}", "&#125;")
    s = s.replace("|", "&#124;")
    return s


def _sanitize_token(value: str) -> str:
    token = re.sub(r"[^0-9A-Za-z_]+", "_", str(value))
    token = re.sub(r"_+", "_", token).strip("_")
    if not token:
        token = "node"
    if token[0].isdigit():
        token = f"n_{token}"
    return token


def _sanitize_mermaid_label(text: str) -> str:
    s = text.replace("\\", "\\\\")
    s = s.replace("\n", "<br/>")
    s = s.replace("[", "&#91;").replace("]", "&#93;")
    s = s.replace("{", "&#123;").replace("}", "&#125;")
    s = s.replace("|", "&#124;")
    return s
