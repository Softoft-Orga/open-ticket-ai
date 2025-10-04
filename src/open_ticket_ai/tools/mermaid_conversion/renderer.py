from __future__ import annotations

from .models import SubgraphDef, EdgeDef
from .node import NodeDef
from .utils import sanitize_for_mermaid_label


def render_node_to_mermaid(node: NodeDef) -> str:
    label = sanitize_for_mermaid_label(node.label or " ")
    if node.kind == "decision":
        return f'    {node.identifier}"{label}"'
    if node.kind == "start":
        return f'    {node.identifier}(["{label}"])'
    if node.kind == "hidden":
        return f'    {node.identifier}[" "]:::hidden'
    return f'    {node.identifier}["{label}"]:::step'


def render_edge_to_mermaid(edge: EdgeDef) -> str:
    if edge.label:
        return f'  {edge.source} -->|{sanitize_for_mermaid_label(edge.label)}| {edge.target}'
    return f'  {edge.source} --> {edge.target}'


def render_subgraph_recursive(subgraph: SubgraphDef, all_nodes: dict[str, NodeDef]) -> list[str]:
    lines: list[str] = [f'  subgraph {subgraph.identifier} [{sanitize_for_mermaid_label(subgraph.label)}]']
    for nid in subgraph.nodes:
        lines.append(render_node_to_mermaid(all_nodes[nid]))
    for child in subgraph.children:
        lines.extend(render_subgraph_recursive(child, all_nodes))
    lines.append('  end')
    lines.append(f'  style {subgraph.identifier} fill:#0b0b0c,stroke:#4b5563,color:#cbd5e1')
    return lines


def build_mermaid_diagram(nodes: dict[str, NodeDef], edges: list[EdgeDef], roots: list[SubgraphDef],
                          direction: str = "TD") -> str:
    header = [
        f"flowchart {direction}",
        "  classDef start fill:#0ea5e9,stroke:#0e7490,color:#fff",
        "  classDef step fill:#1f2937,stroke:#475569,color:#e5e7eb",
        "  classDef hidden fill:none,stroke:none,color:transparent",
    ]
    lines: list[str] = []
    lines.extend(header)
    for root in roots:
        lines.extend(render_subgraph_recursive(root, nodes))
    for e in edges:
        lines.append(render_edge_to_mermaid(e))
    return "\n".join(lines)
