import dataclasses

from open_ticket_ai.tools.mermaid_conversion.models import NodeDef, EdgeDef, SubgraphDef

@dataclasses.dataclass
class GraphBuilder:
    nodes: dict[str, NodeDef] = dataclasses.field(default_factory=dict)
    edges: list[EdgeDef] = dataclasses.field(default_factory=list)
    root_subgraphs: list[SubgraphDef] = dataclasses.field(default_factory=list)
    subgraph_nodes: dict[str, list[str]] = dataclasses.field(default_factory=dict)

    def add_node(self, identifier: str, label: str, kind: str) -> None:
        if identifier in self.nodes:
            current = self.nodes[identifier]
            if label and label != current.label:
                self.nodes[identifier] = NodeDef(identifier, label, kind if current.kind != "decision" else current.kind)
            return
        self.nodes[identifier] = NodeDef(identifier, label, kind)
    def add_edge(self, source: str, target: str, label: str | None = None) -> None:
        if source == target:
            return
        self.edges.append(EdgeDef(source, target, label))
    def create_subgraph(self, identifier: str, label: str) -> SubgraphDef:
        sg = SubgraphDef(identifier, label, [], [])
        self.subgraph_nodes[identifier] = sg.nodes
        return sg
    def append_node_to_subgraph(self, subgraph_identifier: str, node_identifier: str) -> None:
        self.subgraph_nodes.setdefault(subgraph_identifier, [])
        if node_identifier not in self.subgraph_nodes[subgraph_identifier]:
            self.subgraph_nodes[subgraph_identifier].append(node_identifier)
