from pathlib import Path

import pytest

pytest.importorskip("yaml")

from open_ticket_ai.diagram import ConfigFlowDiagramGenerator
from open_ticket_ai.diagram.generator import ConfigLoader, PipelineExtractor


@pytest.fixture
def sample_config_path() -> Path:
    return Path("src/config.yml")


def test_pipeline_extractor_discovers_named_pipelines(sample_config_path: Path) -> None:
    generator = ConfigFlowDiagramGenerator(sample_config_path)
    diagrams = generator.generate()

    assert "ticket-routing" in diagrams
    assert "classification_generic" in diagrams


def test_mermaid_diagram_contains_expected_nodes(sample_config_path: Path) -> None:
    generator = ConfigFlowDiagramGenerator(sample_config_path)
    diagrams = generator.generate()
    routing_diagram = diagrams["ticket-routing"]

    assert "ticket_routing_ticket_fetcher" in routing_diagram
    assert "ticket_routing_queue_classification" in routing_diagram


def test_parser_uses_explicit_dependencies(sample_config_path: Path) -> None:
    loader = ConfigLoader(sample_config_path)
    config = loader.load()
    extractor = PipelineExtractor(config)
    pipelines = extractor.extract()

    classification = next(diagram for diagram in pipelines if diagram.name == "classification_generic")
    step_map = {step.identifier: step for step in classification.steps}

    assert "classify" in step_map["map_value"].dependencies
