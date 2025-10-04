import dataclasses

from open_ticket_ai.tools.mermaid_conversion.models import EdgeDef, SubgraphDef
from open_ticket_ai.tools.mermaid_conversion.node import NodeDef


@dataclasses.dataclass
class Graph:
    nodes: dict[str, NodeDef] = dataclasses.field(default_factory=dict)
    edges: list[EdgeDef] = dataclasses.field(default_factory=list)
    root_subgraphs: list[SubgraphDef] = dataclasses.field(default_factory=list)
    _subgraphs_by_id: dict[str, SubgraphDef] = dataclasses.field(default_factory=dict)

    def add_node(self, identifier: str, label: str, kind: str) -> None:
        if identifier in self.nodes:
            current = self.nodes[identifier]
            if label and label != current.label:
                self.nodes[identifier] = NodeDef(identifier, label, kind)
            return
        self.nodes[identifier] = NodeDef(identifier, label, kind)

    def add_edge(self, source: str, target: str, label: str | None = None) -> None:
        if source == target:
            return
        self.edges.append(EdgeDef(source, target, label))

    def create_subgraph(self, identifier: str, label: str) -> SubgraphDef:
        sg = SubgraphDef(identifier, label, [], [])
        self._subgraphs_by_id[identifier] = sg
        return sg

    def append_node_to_subgraph(self, subgraph_identifier: str, node_identifier: str) -> None:
        subgraph = self._subgraphs_by_id.get(subgraph_identifier)
        if subgraph is None:
            return
        if node_identifier not in subgraph.nodes:
            subgraph.nodes.append(node_identifier)

    def collect_internal_roots(self, node_identifiers: list[str]) -> list[str]:
        indegree: dict[str, int] = {nid: 0 for nid in node_identifiers}
        for e in self.edges:
            if e.target in indegree:
                indegree[e.target] += 1
        return [nid for nid, d in indegree.items() if d == 0]

    def collect_internal_sinks(self, node_identifiers: list[str]) -> list[str]:
        outdegree: dict[str, int] = {nid: 0 for nid in node_identifiers}
        for e in self.edges:
            if e.source in outdegree:
                outdegree[e.source] += 1
        return [nid for nid, d in outdegree.items() if d == 0]
