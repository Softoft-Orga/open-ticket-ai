from __future__ import annotations

from pathlib import Path

import pytest
from injector import Injector

from open_ticket_ai.core import AppModule, RawOpenTicketAIConfig, load_config


@pytest.fixture
def mock_ticket_system_config():
    """Create a mock ticket system pipe configuration for testing.

    Returns a dictionary with ticket_system_id for ticket system pipes.
    """
    return {
        "id": "test_ticket_pipe",
        "use": "TestTicketPipe",
        "when": True,
        "steps": [],
        "ticket_system_id": "mock_ticket_system",
    }


@pytest.fixture
def tmp_config(tmp_path: Path) -> Path:
    config_content = """
open_ticket_ai:
  plugins: []
  general_config:
    logging:
      version: 1
      disable_existing_loggers: false
      formatters:
        simple:
          format: '%(levelname)s - %(message)s'
      handlers:
        console:
          class: logging.StreamHandler
          formatter: simple
      root:
        level: INFO
        handlers: [console]
  defs: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")
    return config_path


@pytest.fixture
def app_injector(tmp_config: Path) -> Injector:
    return Injector([AppModule(tmp_config)])


@pytest.fixture
def test_config(tmp_config: Path) -> RawOpenTicketAIConfig:
    return load_config(tmp_config)
