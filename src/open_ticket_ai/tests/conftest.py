import asyncio
from contextlib import contextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import (
    TicketSystemService,
)
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    UnifiedEntity,
    UnifiedNote,
)
from open_ticket_ai.tests.mocked_ticket_system import MockedTicketSystem


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
            "id": "test_pipe",
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
        "id": "test_ticket_pipe",
        "use": "TestTicketPipe",
        "when": True,
        "steps": [],
        "ticket_system_id": "mock_ticket_system",
    }


@pytest.fixture
def pipe_runner(mock_registry, mock_ticket_system_service):
    def _run_pipe(pipe_class, config, context):
        with patched_registry(mock_registry):
            # Check if pipe needs ticket_system as first arg (ticket system pipes)
            import inspect

            sig = inspect.signature(pipe_class.__init__)
            params = list(sig.parameters.keys())
            if len(params) > 2 and params[1] == "ticket_system":
                pipe = pipe_class(mock_ticket_system_service, config)
            else:
                pipe = pipe_class(config)
            return asyncio.run(pipe.process(context))

    return _run_pipe


@pytest.fixture
def ticket_system_pipe_factory(mock_ticket_system_service, mock_registry):
    def _create_pipe(pipe_class, **config_overrides):
        base_config = {
            "id": "test_pipe",
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


@pytest.fixture
def empty_mocked_ticket_system() -> MockedTicketSystem:
    """Empty MockedTicketSystem for custom test scenarios."""
    return MockedTicketSystem()


@pytest.fixture
def mocked_ticket_system() -> MockedTicketSystem:
    system = MockedTicketSystem()

    # Add sample tickets
    system.add_test_ticket(
        id="TICKET-1",
        subject="Test ticket 1",
        body="This is the first test ticket",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="Medium"),
        notes=[],
    )

    system.add_test_ticket(
        id="TICKET-2",
        subject="Test ticket 2",
        body="This is the second test ticket",
        queue=UnifiedEntity(id="2", name="Development"),
        priority=UnifiedEntity(id="5", name="High"),
        notes=[
            UnifiedNote(id="NOTE-1", subject="Initial note", body="First note on ticket 2"),
        ],
    )

    system.add_test_ticket(
        id="TICKET-3",
        subject="Urgent issue",
        body="This needs immediate attention",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="5", name="High"),
        notes=[],
    )

    return system


@pytest.fixture
def stateful_pipe_runner(mock_registry, mocked_ticket_system):
    def _run_pipe(pipe_class, config, context):
        with patched_registry(mock_registry):
            import inspect

            sig = inspect.signature(pipe_class.__init__)
            params = list(sig.parameters.keys())
            if len(params) > 2 and params[1] == "ticket_system":
                pipe = pipe_class(mocked_ticket_system, config)
            else:
                pipe = pipe_class(config)
            return asyncio.run(pipe.process(context))

    return _run_pipe


@contextmanager
def patched_registry(mock_registry):
    with patch(
        "open_ticket_ai.core.dependency_injection.unified_registry.UnifiedRegistry.instance",
        return_value=mock_registry,
    ):
        yield
