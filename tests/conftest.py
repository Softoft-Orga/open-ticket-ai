# FILE_PATH: open_ticket_ai\tests\conftest.py
import importlib
from unittest.mock import MagicMock

import pytest


def pytest_collection_modifyitems(config, items):
    """Skip heavy experimental tests if dependencies are missing.

    This pytest hook function checks for the availability of SpaCy and the German language model.
    If either module fails to import, marks all tests from 'test_anonymize_data.py' to be skipped.

    Modifies the test items list in-place by adding skip markers to relevant tests.

    Args:
        config (pytest.Config):
            The pytest configuration object (unused in this function but required by hook signature).
        items (list[pytest.Item]):
            List of collected test items. Will be modified in-place by adding skip markers.
    """
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
