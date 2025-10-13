from __future__ import annotations

from pathlib import Path

import pytest
from injector import Injector

from open_ticket_ai.core import AppConfig, AppModule, ConfigLoader, RawOpenTicketAIConfig


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
  infrastructure:
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
  services: []
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
def test_config(tmp_config: Path, logger_factory) -> RawOpenTicketAIConfig:
    config_loader = ConfigLoader(AppConfig(), logger_factory)
    return config_loader.load_config(tmp_config)


@pytest.fixture
def logger_factory():
    """Create a logger factory for testing."""
    from open_ticket_ai.base.loggers.stdlib_logging_adapter import create_logger_factory
    from open_ticket_ai.core.config.config_models import LoggingDictConfig

    return create_logger_factory(LoggingDictConfig())
