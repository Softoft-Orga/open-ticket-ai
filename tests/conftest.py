from __future__ import annotations

from pathlib import Path

import pytest


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
def logger_factory():
    """Create a logger factory for testing."""
    from open_ticket_ai.base.loggers.stdlib_logging_adapter import create_logger_factory
    from open_ticket_ai.core.config.logging_config import LoggingDictConfig

    return create_logger_factory(LoggingDictConfig())
