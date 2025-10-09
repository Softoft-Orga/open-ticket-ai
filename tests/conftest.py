from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from injector import Injector

    from open_ticket_ai.core import RawOpenTicketAIConfig


@pytest.fixture
def mock_pipe_config():
    """Create a mock pipe configuration dictionary for testing.

    Returns a dictionary that can be used to initialize pipes in tests.

    Example:
        def test_something(mock_pipe_config):
            config = mock_pipe_config
            config["field"] = "value"
            my_pipe = MyPipe(config)
    """
    return {"name": "test_pipe", "use": "TestPipe", "when": True, "steps": []}


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
    from injector import Injector

    from open_ticket_ai.core import AppModule

    return Injector([AppModule(tmp_config)])


@pytest.fixture
def test_config(tmp_config: Path) -> RawOpenTicketAIConfig:
    from open_ticket_ai.core import load_config

    return load_config(tmp_config)
