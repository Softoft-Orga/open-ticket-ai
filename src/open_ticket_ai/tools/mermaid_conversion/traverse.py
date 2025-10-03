from __future__ import annotations
from typing import Any

from .graph_builder import GraphBuilder
from .models import SubgraphDef
from .scoped_identifier_map import ScopedIdentifierMap
from .utils import make_global_identifier, format_node_label, build_composite_ports
from .graph_analysis import collect_internal_roots, collect_internal_sinks
from ...core.pipeline.pipe_config import RawPipeConfig


class Traverser:
    def __init__(self, graph: GraphBuilder) -> None:
        self.graph = graph

    def process_simple_step(self, scoped_map: ScopedIdentifierMap, parent_subgraph: SubgraphDef, path_stack: list[str], step_dict: dict[str, Any], index: int) -> str:
        raw_model = RawPipeConfig.model_validate(step_dict)
        display_name = step_dict.get("id") or step_dict.get("use") or f"step_{index}"
        global_identifier = make_global_identifier([*path_stack, str(display_name)])
        label_text = format_node_label(str(display_name), step_dict)
        node_kind = "decision" if isinstance(step_dict.get("if"), str) else "process"
        self.graph.add_node(global_identifier, label_text, node_kind)
        self.graph.append_node_to_subgraph(parent_subgraph.identifier, global_identifier)
        scoped_map.set_value(str(step_dict.get("id") or display_name), global_identifier)
        if isinstance(raw_model.depends_on, list):
            for name in raw_model.depends_on:
                resolved = scoped_map.resolve(str(name))
                if resolved:
                    self.graph.add_edge(resolved, global_identifier, None)
        elif isinstance(raw_model.depends_on, str):
            resolved = scoped_map.resolve(raw_model.depends_on)
            if resolved:
                self.graph.add_edge(resolved, global_identifier, None)
        return global_identifier

    def process_composite_step(self, scoped_map: ScopedIdentifierMap, parent_subgraph: SubgraphDef, path_stack: list[str], step_dict: dict[str, Any], index: int) -> list[str]:
        step_id_value = step_dict.get("id") or step_dict.get("use") or f"step_{index}"
        composite_path = [*path_stack, str(step_id_value)]
        composite_identifier = make_global_identifier(composite_path)
        entry_identifier, exit_identifier = build_composite_ports(composite_path)
        composite_subgraph = self.graph.create_subgraph(composite_identifier, str(step_id_value))
        parent_subgraph.children.append(composite_subgraph)
        self.graph.add_node(entry_identifier, " ", "hidden")
        self.graph.add_node(exit_identifier, " ", "hidden")
        self.graph.append_node_to_subgraph(composite_identifier, entry_identifier)
        self.graph.append_node_to_subgraph(composite_identifier, exit_identifier)
        depends_on_value = step_dict.get("depends_on")
        if isinstance(depends_on_value, list):
            for name in depends_on_value:
                resolved = scoped_map.resolve(str(name))
                if resolved:
                    self.graph.add_edge(resolved, entry_identifier, None)
        elif isinstance(depends_on_value, str):
            resolved = scoped_map.resolve(depends_on_value)
            if resolved:
                self.graph.add_edge(resolved, entry_identifier, None)
        child_scope = ScopedIdentifierMap(scoped_map)
        child_steps = step_dict.get("steps") or []
        inner_identifiers = self.traverse_steps(child_scope, composite_subgraph, composite_path, child_steps)
        for nid in inner_identifiers:
            self.graph.append_node_to_subgraph(composite_identifier, nid)
        internal_edges = [e for e in self.graph.edges if e.source in inner_identifiers or e.target in inner_identifiers]
        for r in collect_internal_roots(inner_identifiers, internal_edges):
            self.graph.add_edge(entry_identifier, r, None)
        for s in collect_internal_sinks(inner_identifiers, internal_edges):
            self.graph.add_edge(s, exit_identifier, None)
        scoped_map.set_value(str(step_id_value), exit_identifier)
        return [entry_identifier, *inner_identifiers, exit_identifier]

    def traverse_steps(self, scoped_map: ScopedIdentifierMap, parent_subgraph: SubgraphDef, path_stack: list[str], steps: list[dict[str, Any]]) -> list[str]:
        created_identifiers: list[str] = []
        for index, step_dict in enumerate(steps):
            if not isinstance(step_dict, dict):
                continue
            child_steps = step_dict.get("steps")
            if isinstance(child_steps, list):
                ids = self.process_composite_step(scoped_map, parent_subgraph, path_stack, step_dict, index)
                created_identifiers.extend(ids)
                continue
            nid = self.process_simple_step(scoped_map, parent_subgraph, path_stack, step_dict, index)
            created_identifiers.append(nid)
        return created_identifiers

    def build_pipelines_from_config(self, config_data: dict[str, Any]) -> GraphBuilder:
        defs = ((config_data.get("open_ticket_ai") or {}).get("defs") or [])
        for def_entry in defs:
            if not isinstance(def_entry, dict):
                continue
            pipeline_id_value = str(def_entry.get("id") or "pipeline")
            pipeline_identifier = make_global_identifier([pipeline_id_value])
            pipeline_subgraph = self.graph.create_subgraph(pipeline_identifier, pipeline_id_value)
            self.graph.root_subgraphs.append(pipeline_subgraph)
            start_identifier = make_global_identifier([pipeline_id_value, "start"])
            self.graph.add_node(start_identifier, f"Start {pipeline_id_value}", "start")
            self.graph.append_node_to_subgraph(pipeline_identifier, start_identifier)
            steps = def_entry.get("steps") or []
            scoped_map = ScopedIdentifierMap()
            inner_nodes = self.traverse_steps(scoped_map, pipeline_subgraph, [pipeline_id_value], steps)
            indegree: dict[str, int] = {nid: 0 for nid in inner_nodes}
            for e in self.graph.edges:
                if e.target in indegree:
                    indegree[e.target] += 1
            for root_id in [nid for nid, d in indegree.items() if d == 0]:
                self.graph.add_edge(start_identifier, root_id, None)
        return self.graph
