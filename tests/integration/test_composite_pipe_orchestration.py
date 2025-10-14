"""Integration tests for composite pipe orchestration and multi-step pipeline execution."""

from __future__ import annotations

import pytest
from pydantic import BaseModel

from open_ticket_ai.base.loggers.stdlib_logging_adapter import create_logger_factory
from open_ticket_ai.base.pipes.composite_pipe import CompositeParams, CompositePipe, CompositePipeConfig
from open_ticket_ai.base.pipes.expression_pipe import ExpressionParams, ExpressionPipeConfig
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
from open_ticket_ai.core.config.logging_config import LoggingDictConfig
from open_ticket_ai.core.renderable.renderable import RenderableConfig
from open_ticket_ai.core.renderable.renderable_factory import RenderableFactory
from open_ticket_ai.core.logging_iface import LoggerFactory
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

JINJA_PIPE_USE = "open_ticket_ai.base.pipes.expression_pipe:ExpressionPipe"
COMPOSITE_PIPE_USE = "open_ticket_ai.base.pipes.composite_pipe:CompositePipe"


class Empty(BaseModel):
    pass


def create_jinja_step(step_id: str, expression: str, **kwargs) -> ExpressionPipeConfig:
    return ExpressionPipeConfig(
        id=step_id, use=JINJA_PIPE_USE, params=ExpressionParams(expression=expression), **kwargs
    )


def create_composite(composite_id: str, steps: list) -> CompositePipeConfig:
    return CompositePipeConfig(id=composite_id, use=COMPOSITE_PIPE_USE, params=CompositeParams(), steps=steps)


@pytest.fixture
def logger_factory() -> LoggerFactory:
    return create_logger_factory(LoggingDictConfig())


@pytest.fixture
def template_renderer(logger_factory) -> JinjaRenderer:
    return JinjaRenderer(JinjaRendererConfig(), logger_factory)


@pytest.fixture
def app_config() -> AppConfig:
    return AppConfig()


@pytest.fixture
def mocked_ticket_system() -> MockedTicketSystem:
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
    ticket_system_config = RenderableConfig(
        id="mock_ticket_system", use="tests.unit.mocked_ticket_system:MockedTicketSystem", params={}
    )
    return RenderableFactory(
        template_renderer=template_renderer,
        app_config=app_config,
        registerable_configs=[ticket_system_config],
        logger_factory=logger_factory,
    )


@pytest.mark.asyncio
async def test_composite_pipe_executes_child_pipes_in_order(renderable_factory: RenderableFactory) -> None:
    steps = [create_jinja_step("step1", "value1"), create_jinja_step("step2", "value2")]
    composite_config = create_composite("composite", steps)
    context = PipeContext(pipe_results={}, params={})

    result_ctx = await renderable_factory.create_pipe(composite_config, context).process(context)

    assert result_ctx.pipe_results["composite"].success
    assert not result_ctx.pipe_results["composite"].failed
    assert result_ctx.pipe_results["step1"].success and result_ctx.pipe_results["step1"].data.value == "value1"
    assert result_ctx.pipe_results["step2"].success and result_ctx.pipe_results["step2"].data.value == "value2"


@pytest.mark.asyncio
async def test_composite_pipe_with_dependencies(renderable_factory: RenderableFactory) -> None:
    steps = [create_jinja_step("step1", "first"), create_jinja_step("step2", "second", depends_on=["step1"])]
    composite_config = create_composite("composite", steps)

    result_ctx = await renderable_factory.create_pipe(composite_config, PipeContext()).process(PipeContext())

    assert "step1" in result_ctx.pipe_results and "step2" in result_ctx.pipe_results
    assert result_ctx.pipe_results["step2"].success


@pytest.mark.asyncio
async def test_composite_pipe_conditional_execution(renderable_factory: RenderableFactory) -> None:
    steps = [
        create_jinja_step("step1", "always_run"),
        create_jinja_step("step2", "should_skip", if_=False),
        create_jinja_step("step3", "also_run", if_=True),
    ]
    composite_config = create_composite("composite", steps)

    result_ctx = await renderable_factory.create_pipe(composite_config, PipeContext()).process(PipeContext())

    assert result_ctx.pipe_results["step1"].success
    assert "step2" not in result_ctx.pipe_results
    assert result_ctx.pipe_results["step3"].success


@pytest.mark.asyncio
async def test_composite_pipe_result_aggregation(renderable_factory: RenderableFactory) -> None:
    steps = [create_jinja_step("step1", "first_value"), create_jinja_step("step2", "second_value")]
    composite_config = create_composite("composite", steps)

    result_ctx = await renderable_factory.create_pipe(composite_config, PipeContext()).process(PipeContext())

    composite_result = result_ctx.pipe_results["composite"]
    assert composite_result.success and not composite_result.failed
    assert hasattr(composite_result.data, "value")


@pytest.mark.asyncio
async def test_composite_pipe_error_propagation(logger_factory: LoggerFactory) -> None:
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

    from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
    from open_ticket_ai.core import AppConfig
    from open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig

    class SimpleFactory(RenderableFactory):
        def __init__(self) -> None:
            super().__init__(JinjaRenderer(JinjaRendererConfig(), logger_factory), AppConfig(), [], logger_factory)

        def create_pipe(self, config_raw: PipeConfig, scope: PipeContext):
            return update_pipe if config_raw.id == "step1" else None

    composite_pipe = CompositePipe(create_composite("composite", [update_pipe_config]), SimpleFactory(), logger_factory)
    result_ctx = await composite_pipe.process(PipeContext())

    assert not result_ctx.pipe_results["step1"].success and result_ctx.pipe_results["step1"].failed
    assert result_ctx.pipe_results["composite"].failed


@pytest.mark.asyncio
async def test_realistic_multi_step_pipeline(logger_factory: LoggerFactory) -> None:
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

    configs = [
        FetchTicketsPipeConfig(
            id="fetch_tickets",
            use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe:FetchTicketsPipe",
            params=FetchTicketsParams(
                ticket_search_criteria=TicketSearchCriteria(queue=UnifiedEntity(id="queue-1", name="Support"), limit=10)
            ),
        ),
        UpdateTicketPipeConfig(
            id="update_ticket",
            use="open_ticket_ai.base.pipes.ticket_system_pipes.update_ticket_pipe:UpdateTicketPipe",
            params=UpdateTicketParams(
                ticket_id="TICKET-1", updated_ticket=UnifiedTicket(priority=UnifiedEntity(id="priority-5", name="High"))
            ),
        ),
        AddNotePipeConfig(
            id="add_note",
            use="open_ticket_ai.base.pipes.ticket_system_pipes.add_note_pipe:AddNotePipe",
            params=AddNoteParams(
                ticket_id="TICKET-1", note=UnifiedNote(subject="Updated", body="Priority was updated to High")
            ),
        ),
    ]

    pipes = {
        "fetch_tickets": FetchTicketsPipe(mock_system, configs[0], logger_factory),
        "update_ticket": UpdateTicketPipe(mock_system, configs[1], logger_factory),
        "add_note": AddNotePipe(mock_system, configs[2], logger_factory),
    }

    from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
    from open_ticket_ai.core import AppConfig
    from open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig

    class SimpleFactory(RenderableFactory):
        def __init__(self) -> None:
            super().__init__(JinjaRenderer(JinjaRendererConfig(), logger_factory), AppConfig(), [], logger_factory)

        def create_pipe(self, config_raw: PipeConfig, scope: PipeContext):
            return pipes.get(config_raw.id)

    composite = CompositePipe(create_composite("workflow", configs), SimpleFactory(), logger_factory)
    result_ctx = await composite.process(PipeContext())

    assert (
            result_ctx.pipe_results["fetch_tickets"].success and len(result_ctx.pipe_results["fetch_tickets"].data.fetched_tickets) == 2
    )
    assert result_ctx.pipe_results["update_ticket"].success and result_ctx.pipe_results["update_ticket"].data.ticket_updated
    assert result_ctx.pipe_results["add_note"].success and result_ctx.pipe_results["add_note"].data.note_added

    ticket = await mock_system.get_ticket("TICKET-1")
    assert ticket.priority.id == "priority-5" and ticket.priority.name == "High"
    assert len(ticket.notes) == 1 and ticket.notes[0].body == "Priority was updated to High"
    assert result_ctx.pipe_results["workflow"].success


@pytest.mark.asyncio
async def test_composite_pipe_context_propagation(renderable_factory: RenderableFactory) -> None:
    steps = [
        create_jinja_step("step1", "step1_output"),
        create_jinja_step("step2", "step2_output", depends_on=["step1"]),
    ]
    composite_config = create_composite("composite", steps)
    initial_context = PipeContext(pipe_results={}, params={"initial_param": "test_value"})

    result_ctx = await renderable_factory.create_pipe(composite_config, initial_context).process(initial_context)

    assert result_ctx.params["initial_param"] == "test_value"
    assert "step1" in result_ctx.pipe_results and "step2" in result_ctx.pipe_results


@pytest.mark.asyncio
async def test_nested_composite_pipes(renderable_factory: RenderableFactory) -> None:
    inner_steps = [create_jinja_step("inner_step1", "inner1"), create_jinja_step("inner_step2", "inner2")]
    inner_composite = create_composite("inner_composite", inner_steps)
    outer_steps = [inner_composite, create_jinja_step("outer_step", "outer")]
    outer_composite = create_composite("outer_composite", outer_steps)

    result_ctx = await renderable_factory.create_pipe(outer_composite, PipeContext()).process(PipeContext())

    assert result_ctx.pipe_results["inner_composite"].success
    assert "inner_step1" in result_ctx.pipe_results and "inner_step2" in result_ctx.pipe_results
    assert result_ctx.pipe_results["outer_step"].success
    assert result_ctx.pipe_results["outer_composite"].success
