from unittest.mock import AsyncMock, MagicMock

import pytest

from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import (
    TicketSystemService,
)


@pytest.fixture
def empty_pipeline_context() -> Context:
    return Context(pipes={}, config={})


@pytest.fixture
def mock_ticket_system_service() -> MagicMock:
    mock = MagicMock(spec=TicketSystemService)
    mock.create_ticket = AsyncMock(return_value="TICKET-123")
    mock.update_ticket = AsyncMock(return_value=True)
    mock.add_note = AsyncMock(return_value=True)
    mock.get_ticket = AsyncMock(return_value={})
    return mock


@pytest.fixture
def pipe_config_factory():
    def factory(**kwargs) -> dict:
        defaults = {
            "name": "test_pipe",
            "use": "open_ticket_ai.basic_pipes.DefaultPipe",
            "when": True,
            "steps": [],
        }
        defaults.update(kwargs)
        return defaults

    return factory


@pytest.fixture
def mock_registry():
    mock = MagicMock(spec=UnifiedRegistry)
    mock.get_instance.return_value = MagicMock()
    mock.register_instance.return_value = MagicMock()
    return mock


@pytest.fixture
def mock_ticket_system_pipe_config():
    return {
        "name": "test_ticket_pipe",
        "use": "TestTicketPipe",
        "when": True,
        "steps": [],
        "ticket_system_id": "mock_ticket_system",
    }
