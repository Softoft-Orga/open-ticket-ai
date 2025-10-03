from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence, Self
from node import NodeDef, NodeRenderer
from open_ticket_ai.tools.mermaid_conversion.utils import _sanitize_token, _sanitize_mermaid_label


@dataclass
class SubgraphDef:
    identifier: str
    label: str
    nodes: list[str]
    children: list[Self]

def build_subgraph_from_pipeline(pipeline_id: str) -> SubgraphDef:
    sg_id = _make_global_identifier([pipeline_id])
    return SubgraphDef(sg_id, pipeline_id, [], [])

class SubgraphRenderer:
    @staticmethod
    def render_recursive(subgraph: SubgraphDef, nodes_by_id: dict[str, NodeDef]) -> list[str]:
        lines: list[str] = []
        lines.append(f'  subgraph {subgraph.identifier} [{_sanitize_mermaid_label(subgraph.label)}]')
        for nid in subgraph.nodes:
            node = nodes_by_id.get(nid)
            if node:
                lines.append(NodeRenderer.render(node))
        for child in subgraph.children:
            lines.extend(SubgraphRenderer.render_recursive(child, nodes_by_id))
        lines.append('  end')
        lines.append(f'  style {subgraph.identifier} fill:#0b0b0c,stroke:#4b5563,color:#cbd5e1')
        return lines


def _make_global_identifier(parts: Sequence[str]) -> str:
    return "__".join(_sanitize_token(p) for p in parts)

