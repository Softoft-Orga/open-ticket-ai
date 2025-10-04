from __future__ import annotations

from typing import Any, Self

from .graph_builder import Graph
from .models import SubgraphDef
from .node import _format_node_label, _choose_display_name
from .utils import build_composite_ports, _make_global_identifier
from ...core.pipeline.pipe_config import RawPipeConfig


class Traverser:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def process_simple_step(
        self,
        scoped_map: ScopedIdentifierMap,
        parent_subgraph: SubgraphDef,
        path_stack: list[str],
        step_dict: dict[str, Any],
        index: int
    ) -> str:
        raw_model = RawPipeConfig.model_validate(step_dict)
        display_name = _choose_display_name(step_dict, index)
        global_identifier = _make_global_identifier([*path_stack, display_name])
        label_text = _format_node_label(display_name, step_dict)
        node_kind = "process"

        self.graph.add_node(global_identifier, label_text, node_kind)
        self.graph.append_node_to_subgraph(parent_subgraph.identifier, global_identifier)
        scoped_map.set_value(step_dict.get("id") or display_name, global_identifier)

        if isinstance(raw_model.depends_on, list):
            for name in raw_model.depends_on:
                resolved = scoped_map.resolve(str(name))
                if resolved:
                    self.graph.add_edge(resolved, global_identifier)
        elif isinstance(raw_model.depends_on, str):
            resolved = scoped_map.resolve(raw_model.depends_on)
            if resolved:
                self.graph.add_edge(resolved, global_identifier)

        return global_identifier

    def process_composite_step(
        self,
        scoped_map: ScopedIdentifierMap,
        parent_subgraph: SubgraphDef,
        path_stack: list[str],
        step_dict: dict[str, Any],
        index: int
    ) -> list[str]:
        step_id_value = _choose_display_name(step_dict, index)
        composite_path = [*path_stack, step_id_value]
        composite_identifier = _make_global_identifier(composite_path)
        entry_identifier, exit_identifier = build_composite_ports(composite_path)

        composite_subgraph = self.graph.create_subgraph(composite_identifier, step_id_value)
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
                    self.graph.add_edge(resolved, entry_identifier)
        elif isinstance(depends_on_value, str):
            resolved = scoped_map.resolve(depends_on_value)
            if resolved:
                self.graph.add_edge(resolved, entry_identifier)

        child_scope = ScopedIdentifierMap(scoped_map)
        child_steps = step_dict.get("steps") or []
        inner_identifiers = self.traverse_steps(child_scope, composite_subgraph, composite_path, child_steps)

        for nid in inner_identifiers:
            self.graph.append_node_to_subgraph(composite_identifier, nid)

        roots = self.graph.collect_internal_roots(inner_identifiers)
        for root_id in roots:
            self.graph.add_edge(entry_identifier, root_id)

        sinks = self.graph.collect_internal_sinks(inner_identifiers)
        for sink_id in sinks:
            self.graph.add_edge(sink_id, exit_identifier)

        scoped_map.set_value(step_id_value, exit_identifier)
        return [entry_identifier, *inner_identifiers, exit_identifier]

    def traverse_steps(
        self,
        scoped_map: ScopedIdentifierMap,
        parent_subgraph: SubgraphDef,
        path_stack: list[str],
        steps: list[dict[str, Any]]
    ) -> list[str]:
        created_identifiers: list[str] = []

        for index, step_dict in enumerate(steps):
            if not isinstance(step_dict, dict):
                continue

            child_steps = step_dict.get("steps")
            if isinstance(child_steps, list):
                ids = self.process_composite_step(scoped_map, parent_subgraph, path_stack, step_dict, index)
                created_identifiers.extend(ids)
            else:
                nid = self.process_simple_step(scoped_map, parent_subgraph, path_stack, step_dict, index)
                created_identifiers.append(nid)

        return created_identifiers

    def build_pipelines_from_config(self, config_data: dict[str, Any]) -> Graph:
        orchestrator_entries = config_data.get("orchestrator") or []

        for orch_index, orch_entry in enumerate(orchestrator_entries):
            if not isinstance(orch_entry, dict):
                continue

            pipe_config = orch_entry.get("pipe")
            if not isinstance(pipe_config, dict):
                continue

            pipeline_id_value = str(pipe_config.get("id") or f"pipeline_{orch_index}")
            run_every = orch_entry.get("run_every_milli_seconds")

            pipeline_identifier = _make_global_identifier([pipeline_id_value])
            pipeline_subgraph = self.graph.create_subgraph(pipeline_identifier, pipeline_id_value)
            self.graph.root_subgraphs.append(pipeline_subgraph)

            start_identifier = _make_global_identifier([pipeline_id_value, "start"])
            start_label = f"Start {pipeline_id_value}"
            if isinstance(run_every, (int, float)):
                start_label += f"<br/>Every {run_every} ms"

            self.graph.add_node(start_identifier, start_label, "start")
            self.graph.append_node_to_subgraph(pipeline_identifier, start_identifier)

            steps = pipe_config.get("steps") or []
            scoped_map = ScopedIdentifierMap()
            inner_nodes = self.traverse_steps(scoped_map, pipeline_subgraph, [pipeline_id_value], steps)

            roots = self.graph.collect_internal_roots(inner_nodes)
            for root_id in roots:
                self.graph.add_edge(start_identifier, root_id)

        return self.graph


class ScopedIdentifierMap:
    def __init__(self, parent: Self | None = None) -> None:
        self.parent = parent
        self.values: dict[str, str] = {}

    def set_value(self, local_name: str, global_identifier: str) -> None:
        self.values[local_name] = global_identifier

    def resolve(self, name: str) -> str | None:
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.resolve(name)
        return None
