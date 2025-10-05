from __future__ import annotations

import importlib
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import pytest

if TYPE_CHECKING:
    from injector import Injector

    from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


def pytest_collection_modifyitems(config, items):
    try:
        importlib.import_module("spacy")
        importlib.import_module("de_core_news_sm")
    except Exception:
        skip_reason = "SpaCy or the German model is not available"
        for item in list(items):
            if "test_anonymize_data.py" in str(item.fspath):
                item.add_marker(pytest.mark.skip(reason=skip_reason))


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
def mock_registry():
    """Create a mock UnifiedRegistry for testing.

    Returns a MagicMock that behaves like UnifiedRegistry.
    """
    from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry

    mock = MagicMock(spec=UnifiedRegistry)
    mock.get_instance.return_value = MagicMock()
    mock.register_instance.return_value = MagicMock()

    # Mock the singleton pattern
    UnifiedRegistry.get_registry_instance = MagicMock(return_value=mock)

    return mock


@pytest.fixture
def mock_context():
    """Create a mock Context for testing pipes.

    Returns a Context instance with test data.
    """
    from open_ticket_ai.core.pipeline.context import Context

    return Context(pipes={}, config={})


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
  orchestrator: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")
    return config_path


@pytest.fixture
def app_injector(tmp_config: Path) -> Injector:
    from injector import Injector

    from open_ticket_ai.core.dependency_injection.container import AppModule

    return Injector([AppModule(tmp_config)])


@pytest.fixture
def test_config(tmp_config: Path) -> RawOpenTicketAIConfig:
    from open_ticket_ai.core.config.config_models import load_config

    return load_config(tmp_config)
