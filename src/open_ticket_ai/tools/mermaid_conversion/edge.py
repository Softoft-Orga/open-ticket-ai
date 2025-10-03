from __future__ import annotations
from dataclasses import dataclass

@dataclass
class EdgeDef:
    source: str
    target: str
    label: str | None = None

def _sanitize_mermaid_label(text: str) -> str:
    s = text.replace("\\", "\\\\")
    s = s.replace("\n", "<br/>")
    s = s.replace("[", "&#91;").replace("]", "&#93;")
    s = s.replace("{", "&#123;").replace("}", "&#125;")
    s = s.replace("|", "&#124;")
    return s

class EdgeRenderer:
    @staticmethod
    def render(edge: EdgeDef) -> str:
        if edge.label:
            return f'  {edge.source} -->|{_sanitize_mermaid_label(edge.label)}| {edge.target}'
        return f'  {edge.source} --> {edge.target}'
