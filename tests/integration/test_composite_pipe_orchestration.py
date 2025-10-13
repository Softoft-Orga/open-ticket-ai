"""Integration tests for composite pipe orchestration and multi-step pipeline execution."""

from __future__ import annotations

from typing import Any

import pytest
from injector import Injector

from open_ticket_ai.base.pipes.composite_pipe import CompositeParams, CompositePipe, CompositePipeConfig
from open_ticket_ai.base.pipes.jinja_expression_pipe import JinjaExpressionParams, JinjaExpressionPipeConfig
from open_ticket_ai.base.pipes.ticket_system_pipes import (
    AddNoteParams,
    AddNotePipeConfig,
    FetchTicketsParams,
    FetchTicketsPipeConfig,
    UpdateTicketParams,
    UpdateTicketPipeConfig,
)
from open_ticket_ai.base.pipes.ticket_system_pipes.add_note_pipe import AddNotePipe
from open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe import FetchTicketsPipe
from open_ticket_ai.base.pipes.ticket_system_pipes.update_ticket_pipe import UpdateTicketPipe
from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.renderable import RenderableConfig
from open_ticket_ai.core.config.renderable_factory import RenderableFactory
from open_ticket_ai.core.dependency_injection.logging_module import LoggingModule
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig
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
def logger_factory() -> LoggerFactory:
    """Create a LoggerFactory for testing."""
    injector = Injector([LoggingModule(log_impl="stdlib", log_level="DEBUG")])
    return injector.get(LoggerFactory)


@pytest.fixture
def template_renderer() -> JinjaRenderer:
    """Create a JinjaRenderer for testing."""
    return JinjaRenderer(JinjaRendererConfig())


@pytest.fixture
def app_config() -> AppConfig:
    """Create an AppConfig for testing."""
    return AppConfig()


@pytest.fixture
def mocked_ticket_system() -> MockedTicketSystem:
    """Create a MockedTicketSystem with sample tickets."""
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
        body="This needs attention",
        queue=UnifiedEntity(id="queue-1", name="Support"),
        priority=UnifiedEntity(id="priority-5", name="High"),
        notes=[],
    )

    return system


@pytest.fixture
def renderable_factory(
    logger_factory: LoggerFactory,
    template_renderer: JinjaRenderer,
    app_config: AppConfig,
) -> RenderableFactory:
    """Create a RenderableFactory for testing."""
    ticket_system_config: RenderableConfig[Any] = RenderableConfig(
        id="mock_ticket_system",
        use="tests.unit.mocked_ticket_system:MockedTicketSystem",
        params={},
    )

    factory = RenderableFactory(
        template_renderer=template_renderer,
        app_config=app_config,
        registerable_configs=[ticket_system_config],
        logger_factory=logger_factory,
    )

    return factory


@pytest.mark.asyncio
async def test_composite_pipe_executes_child_pipes_in_order(
    renderable_factory: RenderableFactory,
    logger_factory: LoggerFactory,
) -> None:
    """Test that composite pipe executes child pipes in the correct order."""
    step1_config = JinjaExpressionPipeConfig(
        id="step1",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="value1"),
    )

    step2_config = JinjaExpressionPipeConfig(
        id="step2",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="value2"),
    )

    composite_config = CompositePipeConfig(
        id="composite",
        use="open_ticket_ai.base.pipes.composite_pipe:CompositePipe",
        params=CompositeParams(),
        steps=[step1_config, step2_config],
    )

    context = PipeContext(pipes={}, params={})

    composite_pipe = renderable_factory.create_pipe(composite_config, context)
    result_context = await composite_pipe.process(context)

    assert "composite" in result_context.pipes
    assert result_context.pipes["composite"].success is True
    assert result_context.pipes["composite"].failed is False

    assert "step1" in result_context.pipes
    assert result_context.pipes["step1"].success is True
    assert result_context.pipes["step1"].data.value == "value1"

    assert "step2" in result_context.pipes
    assert result_context.pipes["step2"].success is True
    assert result_context.pipes["step2"].data.value == "value2"


@pytest.mark.asyncio
async def test_composite_pipe_with_dependencies(
    renderable_factory: RenderableFactory,
    logger_factory: LoggerFactory,
) -> None:
    """Test that composite pipe respects depends_on relationships."""
    step1_config = JinjaExpressionPipeConfig(
        id="step1",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="first"),
    )

    step2_config = JinjaExpressionPipeConfig(
        id="step2",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="second"),
        depends_on=["step1"],
    )

    composite_config = CompositePipeConfig(
        id="composite",
        use="open_ticket_ai.base.pipes.composite_pipe:CompositePipe",
        params=CompositeParams(),
        steps=[step1_config, step2_config],
    )

    context = PipeContext(pipes={}, params={})

    composite_pipe = renderable_factory.create_pipe(composite_config, context)
    result_context = await composite_pipe.process(context)

    assert "step1" in result_context.pipes
    assert "step2" in result_context.pipes
    assert result_context.pipes["step2"].success is True


@pytest.mark.asyncio
async def test_composite_pipe_conditional_execution(
    renderable_factory: RenderableFactory,
    logger_factory: LoggerFactory,
) -> None:
    """Test that composite pipe respects conditional execution (if conditions)."""
    step1_config = JinjaExpressionPipeConfig(
        id="step1",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="always_run"),
    )

    step2_config = JinjaExpressionPipeConfig(
        id="step2",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="should_skip"),
        if_=False,
    )

    step3_config = JinjaExpressionPipeConfig(
        id="step3",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="also_run"),
        if_=True,
    )

    composite_config = CompositePipeConfig(
        id="composite",
        use="open_ticket_ai.base.pipes.composite_pipe:CompositePipe",
        params=CompositeParams(),
        steps=[step1_config, step2_config, step3_config],
    )

    context = PipeContext(pipes={}, params={})

    composite_pipe = renderable_factory.create_pipe(composite_config, context)
    result_context = await composite_pipe.process(context)

    assert "step1" in result_context.pipes
    assert result_context.pipes["step1"].success is True

    assert "step2" not in result_context.pipes

    assert "step3" in result_context.pipes
    assert result_context.pipes["step3"].success is True


@pytest.mark.asyncio
async def test_composite_pipe_result_aggregation(
    renderable_factory: RenderableFactory,
    logger_factory: LoggerFactory,
) -> None:
    """Test that composite pipe correctly aggregates results from child pipes."""
    step1_config = JinjaExpressionPipeConfig(
        id="step1",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="first_value"),
    )

    step2_config = JinjaExpressionPipeConfig(
        id="step2",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="second_value"),
    )

    composite_config = CompositePipeConfig(
        id="composite",
        use="open_ticket_ai.base.pipes.composite_pipe:CompositePipe",
        params=CompositeParams(),
        steps=[step1_config, step2_config],
    )

    context = PipeContext(pipes={}, params={})

    composite_pipe = renderable_factory.create_pipe(composite_config, context)
    result_context = await composite_pipe.process(context)

    composite_result = result_context.pipes["composite"]
    assert composite_result.success is True
    assert composite_result.failed is False

    assert hasattr(composite_result.data, "value")


@pytest.mark.asyncio
async def test_composite_pipe_error_propagation(
    logger_factory: LoggerFactory,
) -> None:
    """Test that composite pipe properly propagates errors from child pipes."""
    mock_system = MockedTicketSystem({})

    update_pipe_config = UpdateTicketPipeConfig(
        id="step1",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.update_ticket_pipe:UpdateTicketPipe",
        params=UpdateTicketParams(
            ticket_id="NONEXISTENT-999",
            updated_ticket=UnifiedTicket(priority=UnifiedEntity(id="priority-5", name="High")),
        ),
    )

    update_pipe = UpdateTicketPipe(mock_system, update_pipe_config, logger_factory)

    composite_config = CompositePipeConfig(
        id="composite",
        use="open_ticket_ai.base.pipes.composite_pipe:CompositePipe",
        params=CompositeParams(),
        steps=[update_pipe_config],
    )

    class SimpleFactory:
        def create_pipe(self, config: PipeConfig[Any], context: PipeContext) -> Pipe[Any]:
            if config.id == "step1":
                return update_pipe
            raise ValueError(f"Unknown pipe: {config.id}")

    composite_pipe = CompositePipe(composite_config, factory=SimpleFactory(), logger_factory=logger_factory)  # type: ignore[arg-type]

    context = PipeContext(pipes={}, params={})
    result_context = await composite_pipe.process(context)

    assert "step1" in result_context.pipes
    assert result_context.pipes["step1"].success is False
    assert result_context.pipes["step1"].failed is True

    assert "composite" in result_context.pipes
    composite_result = result_context.pipes["composite"]
    assert composite_result.failed is True


@pytest.mark.asyncio
async def test_realistic_multi_step_pipeline(
    logger_factory: LoggerFactory,
) -> None:
    """Test a realistic multi-step pipeline: fetch, update, add note."""
    mock_system = MockedTicketSystem({})
    await mock_system.create_ticket(
        UnifiedTicket(
            id="TICKET-1",
            subject="Test ticket",
            body="Body",
            queue=UnifiedEntity(id="queue-1", name="Support"),
            priority=UnifiedEntity(id="priority-3", name="Medium"),
        )
    )
    await mock_system.create_ticket(
        UnifiedTicket(
            id="TICKET-2",
            subject="Another ticket",
            body="Body 2",
            queue=UnifiedEntity(id="queue-1", name="Support"),
            priority=UnifiedEntity(id="priority-3", name="Medium"),
        )
    )

    fetch_config = FetchTicketsPipeConfig(
        id="fetch_tickets",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe:FetchTicketsPipe",
        params=FetchTicketsParams(
            ticket_search_criteria=TicketSearchCriteria(
                queue=UnifiedEntity(id="queue-1", name="Support"),
                limit=10,
            )
        ),
    )

    update_config = UpdateTicketPipeConfig(
        id="update_ticket",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.update_ticket_pipe:UpdateTicketPipe",
        params=UpdateTicketParams(
            ticket_id="TICKET-1",
            updated_ticket=UnifiedTicket(priority=UnifiedEntity(id="priority-5", name="High")),
        ),
    )

    add_note_config = AddNotePipeConfig(
        id="add_note",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.add_note_pipe:AddNotePipe",
        params=AddNoteParams(
            ticket_id="TICKET-1",
            note=UnifiedNote(subject="Updated", body="Priority was updated to High"),
        ),
    )

    fetch_pipe = FetchTicketsPipe(mock_system, fetch_config, logger_factory)
    update_pipe = UpdateTicketPipe(mock_system, update_config, logger_factory)
    add_note_pipe = AddNotePipe(mock_system, add_note_config, logger_factory)

    composite_config = CompositePipeConfig(
        id="workflow",
        use="open_ticket_ai.base.pipes.composite_pipe:CompositePipe",
        params=CompositeParams(),
        steps=[fetch_config, update_config, add_note_config],
    )

    class SimpleFactory:
        def create_pipe(self, config: PipeConfig[Any], context: PipeContext) -> Pipe[Any]:
            if config.id == "fetch_tickets":
                return fetch_pipe
            elif config.id == "update_ticket":
                return update_pipe
            elif config.id == "add_note":
                return add_note_pipe
            raise ValueError(f"Unknown pipe: {config.id}")

    composite_pipe = CompositePipe(composite_config, factory=SimpleFactory(), logger_factory=logger_factory)  # type: ignore[arg-type]

    context = PipeContext(pipes={}, params={})
    result_context = await composite_pipe.process(context)

    assert "fetch_tickets" in result_context.pipes
    fetch_result = result_context.pipes["fetch_tickets"]
    assert fetch_result.success is True
    assert len(fetch_result.data.fetched_tickets) == 2

    assert "update_ticket" in result_context.pipes
    update_result = result_context.pipes["update_ticket"]
    assert update_result.success is True
    assert update_result.data.ticket_updated is True

    assert "add_note" in result_context.pipes
    note_result = result_context.pipes["add_note"]
    assert note_result.success is True
    assert note_result.data.note_added is True

    ticket = await mock_system.get_ticket("TICKET-1")
    assert ticket is not None
    assert ticket.priority is not None
    assert ticket.priority.id == "priority-5"
    assert ticket.priority.name == "High"
    assert ticket.notes is not None
    assert len(ticket.notes) == 1
    assert ticket.notes[0].body == "Priority was updated to High"

    assert "workflow" in result_context.pipes
    workflow_result = result_context.pipes["workflow"]
    assert workflow_result.success is True


@pytest.mark.asyncio
async def test_composite_pipe_context_propagation(
    renderable_factory: RenderableFactory,
    logger_factory: LoggerFactory,
) -> None:
    """Test that composite pipe properly propagates context between steps."""
    step1_config = JinjaExpressionPipeConfig(
        id="step1",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="step1_output"),
    )

    step2_config = JinjaExpressionPipeConfig(
        id="step2",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="step2_output"),
        depends_on=["step1"],
    )

    composite_config = CompositePipeConfig(
        id="composite",
        use="open_ticket_ai.base.pipes.composite_pipe:CompositePipe",
        params=CompositeParams(),
        steps=[step1_config, step2_config],
    )

    initial_context = PipeContext(pipes={}, params={"initial_param": "test_value"})

    composite_pipe = renderable_factory.create_pipe(composite_config, initial_context)
    result_context = await composite_pipe.process(initial_context)

    assert result_context.params["initial_param"] == "test_value"

    assert "step1" in result_context.pipes
    assert "step2" in result_context.pipes


@pytest.mark.asyncio
async def test_nested_composite_pipes(
    renderable_factory: RenderableFactory,
    logger_factory: LoggerFactory,
) -> None:
    """Test composite pipes can contain other composite pipes."""
    inner_step1 = JinjaExpressionPipeConfig(
        id="inner_step1",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="inner1"),
    )

    inner_step2 = JinjaExpressionPipeConfig(
        id="inner_step2",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="inner2"),
    )

    inner_composite = CompositePipeConfig(
        id="inner_composite",
        use="open_ticket_ai.base.pipes.composite_pipe:CompositePipe",
        params=CompositeParams(),
        steps=[inner_step1, inner_step2],
    )

    outer_step = JinjaExpressionPipeConfig(
        id="outer_step",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="outer"),
    )

    outer_composite = CompositePipeConfig(
        id="outer_composite",
        use="open_ticket_ai.base.pipes.composite_pipe:CompositePipe",
        params=CompositeParams(),
        steps=[inner_composite, outer_step],
    )

    context = PipeContext(pipes={}, params={})

    composite_pipe = renderable_factory.create_pipe(outer_composite, context)
    result_context = await composite_pipe.process(context)

    assert "inner_composite" in result_context.pipes
    assert result_context.pipes["inner_composite"].success is True

    assert "inner_step1" in result_context.pipes
    assert "inner_step2" in result_context.pipes

    assert "outer_step" in result_context.pipes
    assert result_context.pipes["outer_step"].success is True

    assert "outer_composite" in result_context.pipes
    assert result_context.pipes["outer_composite"].success is True
