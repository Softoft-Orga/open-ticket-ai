import asyncio
import inspect
from contextlib import contextmanager
from unittest.mock import AsyncMock, MagicMock, patch

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
            "use": "open_ticket_ai.base.DefaultPipe",
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


@contextmanager
def patched_registry(mock_registry):
    """Context manager to patch UnifiedRegistry for pipe testing."""
    with patch.object(UnifiedRegistry, "get_registry_instance", return_value=mock_registry):
        yield


@pytest.fixture
def pipe_runner(mock_registry, mock_ticket_system_service):
    """Factory to run pipes with mocked registry."""
    def _run_pipe(pipe_class, config, context):
        with patched_registry(mock_registry):
            # Check if pipe needs ticket_system as first arg (ticket system pipes)
            import inspect
            sig = inspect.signature(pipe_class.__init__)
            params = list(sig.parameters.keys())
            if len(params) > 2 and params[1] == 'ticket_system':
                pipe = pipe_class(mock_ticket_system_service, config)
            else:
                pipe = pipe_class(config)
            return asyncio.run(pipe.process(context))
    return _run_pipe


@pytest.fixture
def ticket_system_pipe_factory(mock_ticket_system_service, mock_registry):
    """Factory for creating ticket system pipes with common setup."""
    def _create_pipe(pipe_class, **config_overrides):
        base_config = {
            "name": "test_pipe",
            "use": pipe_class.__name__,
            "when": True,
            "steps": [],
            "ticket_system_id": "test_system",
        }
        base_config.update(config_overrides)
        
        mock_registry.get_instance.return_value = mock_ticket_system_service
        
        with patched_registry(mock_registry):
            return pipe_class(base_config)
    
    return _create_pipe
