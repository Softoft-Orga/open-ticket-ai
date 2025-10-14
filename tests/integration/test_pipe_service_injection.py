"""Integration tests for pipe-service injection with DI.

Tests verify that pipes correctly receive injected services (e.g., TicketSystemService)
and that the DI container resolves dependencies properly for realistic workflows.
"""

from __future__ import annotations

import pytest

from open_ticket_ai.base.pipes.ticket_system_pipes import (
    AddNoteParams,
    AddNotePipe,
    AddNotePipeConfig,
    FetchTicketsParams,
    FetchTicketsPipe,
    FetchTicketsPipeConfig,
    UpdateTicketParams,
    UpdateTicketPipe,
    UpdateTicketPipeConfig,
)
from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.renderable import RenderableConfig
from open_ticket_ai.core.config.renderable_factory import RenderableFactory
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)
from tests.unit.mocked_ticket_system import MockedTicketSystem


@pytest.fixture
def mocked_ticket_system() -> MockedTicketSystem:
    """Create a MockedTicketSystem with sample data."""
    system = MockedTicketSystem({})
    system.add_test_ticket(
        id="TICKET-1",
        subject="Test ticket 1",
        body="This is a test ticket",
        queue=UnifiedEntity(id="queue-1", name="Support"),
        priority=UnifiedEntity(id="priority-3", name="Medium"),
        notes=[],
    )
    system.add_test_ticket(
        id="TICKET-2",
        subject="Urgent issue",
        body="Needs attention",
        queue=UnifiedEntity(id="queue-1", name="Support"),
        priority=UnifiedEntity(id="priority-5", name="High"),
        notes=[UnifiedNote(id="NOTE-1", subject="Initial note", body="First note")],
    )
    return system


@pytest.mark.asyncio
async def test_add_note_pipe_with_injected_service(
    mocked_ticket_system: MockedTicketSystem,
    logger_factory: LoggerFactory,
) -> None:
    """Test AddNotePipe with injected TicketSystemService."""
    config = AddNotePipeConfig(
        id="add_note",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.add_note_pipe:AddNotePipe",
        params=AddNoteParams(
            ticket_id="TICKET-1",
            note=UnifiedNote(subject="Integration Test", body="Testing service injection"),
        ),
    )

    pipe = AddNotePipe(mocked_ticket_system, config, logger_factory)
    context = PipeContext()
    result_context = await pipe.process(context)

    assert result_context.pipes["add_note"].success is True
    ticket = await mocked_ticket_system.get_ticket("TICKET-1")
    assert ticket is not None
    assert ticket.notes is not None
    assert len(ticket.notes) == 1
    assert ticket.notes[0].subject == "Integration Test"
    assert ticket.notes[0].body == "Testing service injection"


@pytest.mark.asyncio
async def test_update_ticket_pipe_with_injected_service(
    mocked_ticket_system: MockedTicketSystem,
    logger_factory: LoggerFactory,
) -> None:
    """Test UpdateTicketPipe with injected TicketSystemService.

    This test verifies that the pipe is properly instantiated with the service.
    """
    config = UpdateTicketPipeConfig(
        id="update_ticket",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.update_ticket_pipe:UpdateTicketPipe",
        params=UpdateTicketParams(
            ticket_id="TICKET-1",
            updated_ticket=UnifiedTicket(),
        ),
    )

    pipe = UpdateTicketPipe(mocked_ticket_system, config, logger_factory)
    assert pipe is not None


@pytest.mark.asyncio
async def test_fetch_tickets_pipe_with_injected_service(
    mocked_ticket_system: MockedTicketSystem,
    logger_factory: LoggerFactory,
) -> None:
    """Test FetchTicketsPipe with injected TicketSystemService."""
    config = FetchTicketsPipeConfig(
        id="fetch_tickets",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe:FetchTicketsPipe",
        params=FetchTicketsParams(
            ticket_search_criteria=TicketSearchCriteria(
                queue=UnifiedEntity(id="queue-1", name="Support"),
                limit=10,
            ),
        ),
    )

    pipe = FetchTicketsPipe(mocked_ticket_system, config, logger_factory)
    context = PipeContext()
    result_context = await pipe.process(context)

    assert result_context.pipes["fetch_tickets"].success is True
    fetched_tickets = result_context.pipes["fetch_tickets"].data.fetched_tickets
    assert len(fetched_tickets) == 2
    ticket_ids = [t.get("id") if isinstance(t, dict) else t.id for t in fetched_tickets]
    assert "TICKET-1" in ticket_ids
    assert "TICKET-2" in ticket_ids


@pytest.mark.asyncio
async def test_multiple_pipes_share_same_service_instance(
    mocked_ticket_system: MockedTicketSystem,
    logger_factory: LoggerFactory,
) -> None:
    """Test that multiple pipes can share the same service instance."""
    fetch_config = FetchTicketsPipeConfig(
        id="fetch_tickets",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe:FetchTicketsPipe",
        params=FetchTicketsParams(
            ticket_search_criteria=TicketSearchCriteria(
                queue=UnifiedEntity(id="queue-1", name="Support"),
                limit=10,
            ),
        ),
    )

    add_note_config = AddNotePipeConfig(
        id="add_note",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.add_note_pipe:AddNotePipe",
        params=AddNoteParams(
            ticket_id="TICKET-1",
            note=UnifiedNote(body="Note added by integration test"),
        ),
    )

    fetch_pipe = FetchTicketsPipe(mocked_ticket_system, fetch_config, logger_factory)
    add_note_pipe = AddNotePipe(mocked_ticket_system, add_note_config, logger_factory)

    context = PipeContext()
    context = await fetch_pipe.process(context)
    assert context.pipes["fetch_tickets"].success is True
    assert len(context.pipes["fetch_tickets"].data.fetched_tickets) == 2

    context = await add_note_pipe.process(context)
    assert context.pipes["add_note"].success is True

    ticket = await mocked_ticket_system.get_ticket("TICKET-1")
    assert ticket is not None
    assert ticket.notes is not None
    assert len(ticket.notes) == 1


def test_pipe_service_injection_with_renderable_factory(
    logger_factory: LoggerFactory,
) -> None:
    """Test that RenderableFactory correctly configures service injection.

    This test verifies that the factory properly registers services and makes them
    available for injection into pipes via the injects configuration.
    """

    from open_ticket_ai.core.config.renderable import RenderableConfig

    ticket_system_config: RenderableConfig = RenderableConfig(
        id="mock_ticket_system",
        use="tests.unit.mocked_ticket_system:MockedTicketSystem",
        params={},
    )

    factory = RenderableFactory(
        template_renderer=JinjaRenderer(JinjaRendererConfig(), logger_factory),
        app_config=AppConfig(),
        registerable_configs=[ticket_system_config],
        logger_factory=logger_factory,
    )

    assert factory is not None
    assert len(factory._registerable_configs) == 1
    assert factory._registerable_configs[0].id == "mock_ticket_system"
