import pytest
from otai_base.pipes.composite_pipe import CompositePipe
from otai_base.pipes.expression_pipe import ExpressionParams, ExpressionPipe
from otai_base.pipes.ticket_system_pipes import AddNoteParams, AddNotePipe, FetchTicketsParams, FetchTicketsPipe

from open_ticket_ai.core.config.config_models import InfrastructureConfig, OpenTicketAIConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.pipes.pipe_models import PipeConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)
from tests.mocked_ticket_system import MockedTicketSystem


@pytest.fixture
def registry() -> ComponentRegistry:
    r = ComponentRegistry()
    r.register("tests:MockedTicketSystem", MockedTicketSystem)
    r.register("base:FetchTicketsPipe", FetchTicketsPipe)
    r.register("base:AddNotePipe", AddNotePipe)
    r.register("base:ExpressionPipe", ExpressionPipe)
    return r


@pytest.fixture
def otai_with_ticketsvc() -> OpenTicketAIConfig:
    svc = InjectableConfig(id="tickets", use="tests:MockedTicketSystem", params={})
    return OpenTicketAIConfig(
        infrastructure=InfrastructureConfig(logging=LoggingConfig()),
        services={"tickets": svc},
        orchestrator=PipeConfig(),
    )


@pytest.fixture
def renderer(integration_template_renderer: TemplateRenderer) -> TemplateRenderer:
    return integration_template_renderer


@pytest.fixture
def factory(
    registry: ComponentRegistry,
    renderer: TemplateRenderer,
    integration_logger_factory,
    otai_with_ticketsvc: OpenTicketAIConfig,
) -> PipeFactory:
    return PipeFactory(
        component_registry=registry,
        template_renderer=renderer,
        logger_factory=integration_logger_factory,
        otai_config=otai_with_ticketsvc,
    )


@pytest.fixture
def ctx() -> PipeContext:
    return PipeContext(pipe_results={}, params={})


@pytest.fixture
def fetch_cfg() -> callable:
    def _make(q_name: str = "Support", limit: int = 10) -> PipeConfig:
        criteria = TicketSearchCriteria(queue=UnifiedEntity(name=q_name), limit=limit, offset=0)
        return PipeConfig(
            id="fetch",
            use="base:FetchTicketsPipe",
            params=FetchTicketsParams(ticket_search_criteria=criteria).model_dump(),
            injects={"ticket_system": "tickets"},
        )

    return _make


@pytest.fixture
def expr_cfg() -> callable:
    def _make(pid: str, expr: str) -> PipeConfig:
        return PipeConfig(id=pid, use="base:ExpressionPipe", params=ExpressionParams(expression=expr).model_dump())

    return _make


@pytest.fixture
def addnote_cfg() -> callable:
    def _make(ticket_id_expr: str, subject: str, body: str) -> PipeConfig:
        p = AddNoteParams(ticket_id=ticket_id_expr, note=UnifiedNote(subject=subject, body=body))
        return PipeConfig(id="add", use="base:AddNotePipe", params=p.model_dump(), injects={"ticket_system": "tickets"})

    return _make


@pytest.fixture
async def seed_tickets(factory: PipeFactory):
    async def _seed(items: list[UnifiedTicket]) -> MockedTicketSystem:
        # Get the shared ticket system instance from the factory so seeded data is visible to all pipes
        svc: MockedTicketSystem = await factory._get_service_by_id("tickets")
        for t in items:
            svc.add_test_ticket(**t.model_dump())
        return svc

    return _seed


@pytest.mark.integration
@pytest.mark.asyncio
async def test_pipes_use_same_ticketsystem_instance(factory: PipeFactory, ctx: PipeContext, fetch_cfg, addnote_cfg):
    f = await factory.create_pipe(fetch_cfg("Support"), ctx)
    a = await factory.create_pipe(addnote_cfg("1", "s", "b"), ctx)
    assert isinstance(f, FetchTicketsPipe)
    assert isinstance(a, AddNotePipe)
    assert isinstance(f._ticket_system, MockedTicketSystem)
    assert isinstance(a._ticket_system, MockedTicketSystem)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_flow_fetch_select_highest_priority_and_add_note(
    factory: PipeFactory, registry: ComponentRegistry, ctx: PipeContext, fetch_cfg, expr_cfg, addnote_cfg, seed_tickets
):
    await seed_tickets(
        [
            UnifiedTicket(
                id="1", subject="A", queue=UnifiedEntity(name="Support"), priority=UnifiedEntity(name="1"), notes=[]
            ),
            UnifiedTicket(
                id="2", subject="B", queue=UnifiedEntity(name="Support"), priority=UnifiedEntity(name="5"), notes=[]
            ),
            UnifiedTicket(
                id="3", subject="C", queue=UnifiedEntity(name="Support"), priority=UnifiedEntity(name="3"), notes=[]
            ),
        ]
    )
    fetch = fetch_cfg("Support")
    select = expr_cfg(
        "select", "{{ (get_pipe_result('fetch','fetched_tickets') | sort(attribute='priority.name') | last).id }}"
    )
    add = addnote_cfg(
        "{{ get_pipe_result('select','value') }}", "Highest Priority", "This note has the highest priority!"
    )
    composite = PipeConfig(id="flow", use="core:CompositePipe", params={"steps": [fetch, select, add]})
    registry.register("core:CompositePipe", CompositePipe)
    pipe = await factory.create_pipe(composite, ctx)
    res = await pipe.process(ctx)
    assert res.succeeded is True
    refetch = await factory.create_pipe(fetch_cfg("Support"), ctx)
    out = await refetch.process(ctx)
    tickets = out.data["fetched_tickets"]
    t2 = next(t for t in tickets if t.id == "2")
    assert any(
        n.subject == "Highest Priority" and n.body == "This note has the highest priority!" for n in (t2.notes or [])
    )
