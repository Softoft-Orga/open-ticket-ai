"""Convert OpenTicketAI YAML configuration files into Mermaid flowcharts."""

from __future__ import annotations

import argparse
import re
import sys
from collections import OrderedDict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig, load_config


@dataclass
class Node:
    """Graph node definition used when rendering Mermaid diagrams."""

    identifier: str
    label: str
    shape: str  # process | start


class ScopedIdMap:
    """Maintain dependency identifiers with lexical scoping."""

    def __init__(self, parent: ScopedIdMap | None = None) -> None:
        self._parent = parent
        self._values: dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        self._values[key] = value

    def get(self, key: str) -> str | None:
        if key in self._values:
            return self._values[key]
        if self._parent is not None:
            return self._parent.get(key)
        return None


class GraphBuilder:
    """Accumulate nodes and edges while traversing the pipeline definition."""

    def __init__(self) -> None:
        self.nodes: "OrderedDict[str, Node]" = OrderedDict()
        self.edges: list[tuple[str, str, str | None]] = []
        self._edge_set: set[tuple[str, str, str | None]] = set()

    def add_node(self, identifier: str, label: str, shape: str) -> None:
        label = label.strip()
        node = self.nodes.get(identifier)
        if node is None:
            self.nodes[identifier] = Node(identifier, label, shape)
            return
        if label and label != node.label:
            node.label = label
        if shape == "start":
            node.shape = shape

    def append_to_label(self, identifier: str, extra: str) -> None:
        extra = extra.strip()
        if not extra:
            return
        node = self.nodes.get(identifier)
        if node is None:
            self.nodes[identifier] = Node(identifier, extra, "process")
            return
        existing_lines = node.label.split("\n") if node.label else []
        if extra not in existing_lines:
            node.label = "\n".join([line for line in existing_lines if line] + [extra])

    def add_edge(self, source: str, target: str, label: str | None = None) -> None:
        if source == target:
            return
        entry = (source, target, label)
        if entry in self._edge_set:
            return
        self._edge_set.add(entry)
        self.edges.append(entry)


def _sanitize_token(token: str) -> str:
    token = re.sub(r"[^0-9A-Za-z_]+", "_", str(token))
    token = re.sub(r"_+", "_", token).strip("_")
    if not token:
        token = "node"
    if token[0].isdigit():
        token = f"n_{token}"
    return token


def _make_node_identifier(parts: Sequence[str]) -> str:
    return "_".join(_sanitize_token(part) for part in parts)


def _determine_display_name(step: dict[str, object], fallback_index: int) -> str:
    step_id = step.get("id")
    if isinstance(step_id, str) and step_id:
        return step_id
    use = step.get("use")
    if isinstance(use, str) and use:
        return use.split(":")[-1]
    return f"step_{fallback_index}"


def _format_label(display_name: str, step: dict[str, object]) -> str:
    parts: list[str] = []
    if display_name:
        parts.append(display_name)
    use = step.get("use")
    if isinstance(use, str) and use and use != display_name:
        parts.append(use)
    depends_on = step.get("depends_on")
    if isinstance(depends_on, Sequence) and not isinstance(depends_on, (str, bytes)) and depends_on:
        deps_list = ", ".join(str(dep) for dep in depends_on)
        parts.append(f"depends on: {deps_list}")
    return "\n".join(parts)


def _build_steps(
    builder: GraphBuilder,
    steps: Sequence[dict[str, object]],
    prefix: tuple[str, ...],
    scope: ScopedIdMap,
) -> tuple[str | None, str | None]:
    previous_last: str | None = None
    first_node: str | None = None

    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            continue

        token = step.get("id") or step.get("use") or f"step_{index}"
        step_prefix = prefix + (str(token),)

        raw_nested = step.get("steps")
        nested_list = (
            list(raw_nested)
            if isinstance(raw_nested, Sequence) and not isinstance(raw_nested, (str, bytes))
            else None
        )

        if nested_list is not None and not step.get("use"):
            child_scope = ScopedIdMap(scope)
            child_first, child_last = _build_steps(builder, nested_list, step_prefix, child_scope)
            if child_first is None:
                continue

            depends_on = step.get("depends_on")
            if isinstance(depends_on, Sequence) and not isinstance(depends_on, (str, bytes)):
                for dependency in depends_on:
                    dependency_id = scope.get(str(dependency))
                    if dependency_id:
                        builder.add_edge(dependency_id, child_first)
            elif previous_last:
                builder.add_edge(previous_last, child_first)

            step_id = step.get("id")
            if isinstance(step_id, str) and step_id:
                builder.append_to_label(child_first, f"Group: {step_id}")

            previous_last = child_last
            if first_node is None:
                first_node = child_first
            if isinstance(step_id, str) and step_id and child_last:
                scope.set(step_id, child_last)
            continue

        display_name = _determine_display_name(step, index)
        node_identifier = _make_node_identifier(step_prefix)
        shape = "process"
        builder.add_node(node_identifier, _format_label(display_name, step), shape)

        depends_on = step.get("depends_on")
        if isinstance(depends_on, Sequence) and not isinstance(depends_on, (str, bytes)):
            has_dependency_edge = False
            for dependency in depends_on:
                dependency_id = scope.get(str(dependency))
                if dependency_id:
                    builder.add_edge(dependency_id, node_identifier)
                    has_dependency_edge = True
            if not has_dependency_edge and previous_last:
                builder.add_edge(previous_last, node_identifier)
        elif previous_last:
            builder.add_edge(previous_last, node_identifier)

        if first_node is None:
            first_node = node_identifier
        previous_last = node_identifier

        step_id = step.get("id")
        if isinstance(step_id, str) and step_id:
            scope.set(step_id, node_identifier)

        if nested_list is not None:
            child_scope = ScopedIdMap(scope)
            child_first, child_last = _build_steps(builder, nested_list, step_prefix, child_scope)
            if child_first:
                builder.add_edge(node_identifier, child_first)
                previous_last = child_last or node_identifier
                if isinstance(step_id, str) and step_id and child_last:
                    scope.set(step_id, child_last)

    return first_node, previous_last


def _sanitize_label_text(text: str) -> str:
    cleaned = text.replace("\\", "\\\\")
    cleaned = cleaned.replace("\n", "<br/>")
    cleaned = cleaned.replace("[", "&#91;").replace("]", "&#93;")
    cleaned = cleaned.replace("{", "&#123;").replace("}", "&#125;")
    cleaned = cleaned.replace("|", "&#124;")
    return cleaned


def _render_node(node: Node) -> str:
    label = _sanitize_label_text(node.label)
    if node.shape == "start":
        return f"    {node.identifier}([\"{label}\"])"
    return f"    {node.identifier}[\"{label}\"]"


def _render_edge(source: str, target: str, label: str | None) -> str:
    if label:
        sanitized = _sanitize_label_text(label)
        return f"    {source} -->|{sanitized}| {target}"
    return f"    {source} --> {target}"


def _build_start_label(pipeline_id: str, entry: dict[str, object]) -> str:
    run_every = entry.get("run_every_milli_seconds")
    label = f"Start {pipeline_id}"
    if isinstance(run_every, (int, float)):
        label += f"\nEvery {run_every} ms"
    return label


def _select_pipelines(
    config: RawOpenTicketAIConfig,
    *,
    pipeline_ids: Sequence[str] | None,
    indexes: Sequence[int] | None,
) -> list[tuple[int, dict[str, object], dict[str, object]]]:
    selected: list[tuple[int, dict[str, object], dict[str, object]]] = []
    allowed_ids = set(pipeline_ids or [])
    allowed_indexes = set(indexes or []) if indexes is not None else None

    for index, entry in enumerate(config.orchestrator):
        pipe = entry.get("pipe") if isinstance(entry, dict) else None
        if not isinstance(pipe, dict):
            continue
        pipeline_id = pipe.get("id") if isinstance(pipe.get("id"), str) else None
        if allowed_ids and (pipeline_id is None or pipeline_id not in allowed_ids):
            continue
        if allowed_indexes is not None and index not in allowed_indexes:
            continue
        selected.append((index, entry, pipe))

    if pipeline_ids and not selected:
        raise ValueError("No orchestrator entries matched the requested pipeline ids")
    if indexes is not None and not selected:
        raise ValueError("No orchestrator entries matched the requested indexes")

    return selected


def generate_mermaid_diagram(
    config: RawOpenTicketAIConfig,
    *,
    pipeline_ids: Sequence[str] | None = None,
    indexes: Sequence[int] | None = None,
    direction: str = "TD",
    wrap: bool = False,
) -> str:
    """Create a Mermaid flowchart for the given configuration."""

    if direction not in {"TD", "LR"}:
        raise ValueError("direction must be either 'TD' or 'LR'")

    selected = _select_pipelines(config, pipeline_ids=pipeline_ids, indexes=indexes)
    if not selected:
        raise ValueError("Configuration does not define any orchestrator pipelines")

    builder = GraphBuilder()
    comments: list[str] = []

    for index, entry, pipe in selected:
        pipeline_id = str(pipe.get("id") or f"pipeline_{index + 1}")
        comments.append(f"Pipeline {index}: {pipeline_id}")
        start_identifier = _make_node_identifier((pipeline_id, "start"))
        builder.add_node(start_identifier, _build_start_label(pipeline_id, entry), "start")
        first, _ = _build_steps(builder, pipe.get("steps", []), (pipeline_id,), ScopedIdMap())
        if first:
            builder.add_edge(start_identifier, first)

    lines = [f"flowchart {direction}"]
    if comments:
        for comment in comments:
            lines.append(f"    %% {comment}")
    for node in builder.nodes.values():
        lines.append(_render_node(node))
    if builder.edges:
        lines.append("")
        for source, target, label in builder.edges:
            lines.append(_render_edge(source, target, label))

    diagram = "\n".join(lines)
    if wrap:
        return f"```mermaid\n{diagram}\n```"
    return diagram


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "config",
        nargs="?",
        default="src/config.yml",
        type=Path,
        help="Path to the OpenTicketAI config.yml file (default: src/config.yml)",
    )
    parser.add_argument(
        "--pipeline-id",
        dest="pipeline_ids",
        action="append",
        help="Limit the output to specific pipeline identifiers (can be repeated)",
    )
    parser.add_argument(
        "--index",
        dest="indexes",
        action="append",
        type=int,
        help="Limit the output to orchestrator entries by zero-based index",
    )
    parser.add_argument(
        "--direction",
        default="TD",
        choices=["TD", "LR"],
        help="Mermaid flowchart direction (TD for top-down, LR for left-right)",
    )
    parser.add_argument(
        "--wrap",
        dest="wrap",
        action="store_true",
        help="Wrap the output in a ```mermaid fenced code block",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    try:
        config = load_config(args.config)
        diagram = generate_mermaid_diagram(
            config,
            pipeline_ids=args.pipeline_ids,
            indexes=args.indexes,
            direction=args.direction,
            wrap=args.wrap,
        )
    except Exception as exc:  # pragma: no cover - CLI convenience
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(diagram)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    project_dir = Path("../../../tests/system_test/otobo_demo/")
    config = load_config(project_dir / "config.yml")
    diagram = generate_mermaid_diagram(
        config,
    )
    with open(project_dir / "diagram.md", "w") as fh:
        fh.write(diagram)
