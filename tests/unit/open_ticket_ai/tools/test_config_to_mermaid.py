from pathlib import Path

import pytest

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig, load_config
from open_ticket_ai.tools.config_to_mermaid import generate_mermaid_diagram


def _load_default_config() -> RawOpenTicketAIConfig:
    return load_config(Path("src/config.yml"))


def test_generate_mermaid_diagram_contains_key_nodes() -> None:
    config = _load_default_config()
    diagram = generate_mermaid_diagram(config)

    assert "flowchart TD" in diagram
    assert "ticket_routing_start([Start ticket-routing" in diagram
    assert "ticket_routing_ticket_fetcher[ticket_fetcher" in diagram
    assert "ticket_routing_ticket_fetcher --> ticket_routing_queue_classification_classify" in diagram
    assert "ticket_routing_queue_classification_select_final[select_final" in diagram
    assert "ticket_routing_priority_classification_classify[classify" in diagram


def test_generate_mermaid_diagram_wrap_and_direction_options() -> None:
    config = _load_default_config()
    diagram = generate_mermaid_diagram(config, direction="LR", wrap=True)

    assert diagram.startswith("```mermaid")
    assert "flowchart LR" in diagram


def test_generate_mermaid_diagram_invalid_pipeline_raises() -> None:
    config = _load_default_config()

    with pytest.raises(ValueError):
        generate_mermaid_diagram(config, pipeline_ids=["does-not-exist"])
