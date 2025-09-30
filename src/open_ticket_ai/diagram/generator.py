"""Generate Mermaid flow diagrams from Open Ticket AI configuration files."""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence


@dataclass
class PipelineStep:
    """Represents a single pipeline step."""

    identifier: str
    label: str
    condition: Optional[str]
    dependencies: Sequence[str]


@dataclass
class PipelineDiagram:
    """A pipeline and its parsed steps."""

    name: str
    steps: Sequence[PipelineStep]


class ConfigLoader:
    """Load YAML configuration files."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    def load(self) -> Dict[str, object]:
        try:
            import yaml
        except ModuleNotFoundError as exc:  # pragma: no cover - depends on environment
            raise ModuleNotFoundError(
                "PyYAML is required to load configuration files. Install it with 'pip install pyyaml'."
            ) from exc

        if not self.path.exists():
            raise FileNotFoundError(f"Configuration file '{self.path}' does not exist")

        with self.path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)

        if not isinstance(data, dict):
            raise ValueError("Expected the configuration file to contain a mapping at the top level")

        return data


class PipelineExtractor:
    """Extract pipeline definitions from the Open Ticket AI configuration."""

    def __init__(self, config: Dict[str, object]) -> None:
        self._config = config

    def extract(self) -> List[PipelineDiagram]:
        open_ticket_config = self._config.get("open_ticket_ai")
        if not isinstance(open_ticket_config, dict):
            return []

        pipelines: List[PipelineDiagram] = []
        definitions = open_ticket_config.get("defs", [])
        pipelines.extend(self._parse_definitions(definitions))

        orchestrator = open_ticket_config.get("orchestrator", [])
        pipelines.extend(self._parse_orchestrator(orchestrator))

        return pipelines

    def _parse_definitions(self, definitions: object) -> List[PipelineDiagram]:
        if not isinstance(definitions, list):
            return []

        pipelines: List[PipelineDiagram] = []
        for index, item in enumerate(definitions):
            if not isinstance(item, dict):
                continue

            raw_steps = item.get("steps")
            if not isinstance(raw_steps, list):
                continue

            name = str(item.get("id", f"definition_{index}"))
            parser = PipelineStepParser(name)
            steps = parser.parse(raw_steps)
            pipelines.append(PipelineDiagram(name=name, steps=steps))

        return pipelines

    def _parse_orchestrator(self, orchestrator: object) -> List[PipelineDiagram]:
        if not isinstance(orchestrator, list):
            return []

        pipelines: List[PipelineDiagram] = []
        for index, item in enumerate(orchestrator):
            if not isinstance(item, dict):
                continue

            pipe = item.get("pipe")
            if not isinstance(pipe, dict):
                continue

            raw_steps = pipe.get("steps")
            if not isinstance(raw_steps, list):
                continue

            name = str(pipe.get("id", f"orchestrator_{index}"))
            parser = PipelineStepParser(name)
            steps = parser.parse(raw_steps)
            pipelines.append(PipelineDiagram(name=name, steps=steps))

        return pipelines


class PipelineStepParser:
    """Convert raw pipeline step definitions into :class:`PipelineStep` objects."""

    def __init__(self, pipeline_name: str) -> None:
        self._pipeline_name = pipeline_name

    def parse(self, raw_steps: Sequence[object]) -> List[PipelineStep]:
        steps: List[PipelineStep] = []
        previous_identifier: Optional[str] = None

        for index, raw_step in enumerate(raw_steps):
            if not isinstance(raw_step, dict):
                continue

            step_id = self._resolve_identifier(raw_step, index)
            dependencies = self._resolve_dependencies(raw_step, previous_identifier)
            label = self._format_label(step_id, raw_step)
            condition = self._extract_condition(raw_step)

            steps.append(
                PipelineStep(
                    identifier=step_id,
                    label=label,
                    condition=condition,
                    dependencies=dependencies,
                )
            )

            previous_identifier = step_id

        return steps

    def _resolve_identifier(self, raw_step: Dict[str, object], index: int) -> str:
        identifier = raw_step.get("id")
        if identifier is None:
            identifier = f"step_{index}"
        return str(identifier)

    def _resolve_dependencies(
        self, raw_step: Dict[str, object], previous_identifier: Optional[str]
    ) -> Sequence[str]:
        depends_on = raw_step.get("depends_on")
        if depends_on is None:
            return [previous_identifier] if previous_identifier else []

        if isinstance(depends_on, str):
            return [depends_on]

        if isinstance(depends_on, Iterable):
            deps = [str(dep) for dep in depends_on if dep]
            return deps

        return [previous_identifier] if previous_identifier else []

    def _format_label(self, step_id: str, raw_step: Dict[str, object]) -> str:
        parts: List[str] = [step_id]

        use_value = raw_step.get("use")
        if isinstance(use_value, str):
            parts.append(use_value)

        if raw_step.get("if"):
            parts.append(f"if {raw_step['if']}")

        return "\n".join(parts)

    def _extract_condition(self, raw_step: Dict[str, object]) -> Optional[str]:
        condition = raw_step.get("if")
        return str(condition) if condition is not None else None


class MermaidDiagramRenderer:
    """Render :class:`PipelineDiagram` instances into Mermaid flowcharts."""

    def render(self, pipeline: PipelineDiagram) -> str:
        lines = ["flowchart TD"]

        for step in pipeline.steps:
            node_id = self._node_identifier(pipeline.name, step.identifier)
            label = self._escape_label(step.label, step.condition)
            lines.append(f"    {node_id}[\"{label}\"]")

        for step in pipeline.steps:
            target_id = self._node_identifier(pipeline.name, step.identifier)
            for dependency in step.dependencies:
                if not dependency:
                    continue
                source_id = self._node_identifier(pipeline.name, dependency)
                lines.append(f"    {source_id} --> {target_id}")

        return "\n".join(lines)

    def _node_identifier(self, pipeline_name: str, step_id: str) -> str:
        raw_identifier = f"{pipeline_name}_{step_id}"
        return re.sub(r"[^0-9A-Za-z_]", "_", raw_identifier)

    def _escape_label(self, label: str, condition: Optional[str]) -> str:
        combined = label
        if condition and "if" not in label:
            combined = f"{label}\nif {condition}" if label else f"if {condition}"

        escaped = combined.replace("\\", "\\\\").replace("\"", r"\"")
        return escaped.replace("\n", "<br/>")


class ConfigFlowDiagramGenerator:
    """High level helper that loads the configuration and renders pipelines."""

    def __init__(self, config_path: Path | str, renderer: Optional[MermaidDiagramRenderer] = None) -> None:
        self._config_path = Path(config_path)
        self._renderer = renderer or MermaidDiagramRenderer()

    def generate(self) -> Dict[str, str]:
        loader = ConfigLoader(self._config_path)
        config = loader.load()

        extractor = PipelineExtractor(config)
        diagrams = extractor.extract()

        return {diagram.name: self._renderer.render(diagram) for diagram in diagrams}

