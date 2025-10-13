"""Unit tests for RenderableFactory assisted injection with explicit inject precedence."""

from __future__ import annotations

import pytest
from injector import Injector
from pydantic import BaseModel

from open_ticket_ai.base.loggers.stdlib_logging_adapter import create_logger_factory
from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.config_models import LoggingDictConfig
from open_ticket_ai.core.config.renderable import EmptyParams, Renderable, RenderableConfig
from open_ticket_ai.core.config.renderable_factory import RenderableFactory
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
)


class MockTicketSystemA(TicketSystemService):
    def __init__(self, params: BaseModel):
        self.name = "SystemA"
        self.params = params

    async def find_tickets(
        self, criteria: TicketSearchCriteria
    ) -> list[UnifiedTicket]:
        return []

    async def find_first_ticket(
        self, criteria: TicketSearchCriteria
    ) -> UnifiedTicket | None:
        return None

    async def get_ticket(self, ticket_id: str | int) -> UnifiedTicket | None:
        return None

    async def create_ticket(self, ticket: UnifiedTicket) -> UnifiedTicket:
        return ticket

    async def update_ticket(
        self, ticket_id: str, updates: UnifiedTicket
    ) -> bool:
        return True

    async def add_note(
        self, ticket_id: str, note: UnifiedNote
    ) -> bool:
        return True


class MockTicketSystemB(TicketSystemService):
    def __init__(self, params: BaseModel):
        self.name = "SystemB"
        self.params = params

    async def find_tickets(
        self, criteria: TicketSearchCriteria
    ) -> list[UnifiedTicket]:
        return []

    async def find_first_ticket(
        self, criteria: TicketSearchCriteria
    ) -> UnifiedTicket | None:
        return None

    async def get_ticket(self, ticket_id: str | int) -> UnifiedTicket | None:
        return None

    async def create_ticket(self, ticket: UnifiedTicket) -> UnifiedTicket:
        return ticket

    async def update_ticket(
        self, ticket_id: str, updates: UnifiedTicket
    ) -> bool:
        return True

    async def add_note(
        self, ticket_id: str, note: UnifiedNote
    ) -> bool:
        return True


class TestPipeParams(BaseModel):
    test_value: str = "test"


class TestPipeConfig(PipeConfig[TestPipeParams]):
    pass


class TestPipeResultData(BaseModel):
    system_name: str


class TestPipe(Pipe[TestPipeParams]):
    def __init__(
        self,
        ticket_system: TicketSystemService,
        pipe_config: TestPipeConfig,
        logger_factory: LoggerFactory | None = None,
    ):
        super().__init__(pipe_config, logger_factory=logger_factory)
        self.ticket_system = ticket_system

    async def _process(self) -> PipeResult[TestPipeResultData]:
        return PipeResult[TestPipeResultData](
            success=True,
            failed=False,
            data=TestPipeResultData(system_name=self.ticket_system.name),
        )


@pytest.fixture
def logger_factory() -> LoggerFactory:
    return create_logger_factory(LoggingDictConfig())


@pytest.fixture
def injector() -> Injector:
    return Injector()


def test_explicit_inject_precedence_over_container_defaults(
    logger_factory: LoggerFactory, injector: Injector
) -> None:
    """Test that explicit injects override container defaults.
    
    This test verifies the core requirement: when a pipe explicitly requests
    a specific service via injects, it receives that service even if the
    container has a different default binding.
    """
    system_a_config: RenderableConfig[EmptyParams] = RenderableConfig(
        id="system_a",
        use="tests.unit.core.config.test_renderable_factory_assisted_injection:MockTicketSystemA",
        params=EmptyParams(),
    )

    system_b_config: RenderableConfig[EmptyParams] = RenderableConfig(
        id="system_b",
        use="tests.unit.core.config.test_renderable_factory_assisted_injection:MockTicketSystemB",
        params=EmptyParams(),
    )

    def configure_default_ticket_system(binder):
        default_system = MockTicketSystemA(EmptyParams())
        binder.bind(TicketSystemService, to=default_system)

    injector_with_default = injector.create_child_injector([configure_default_ticket_system])

    renderer_config = JinjaRendererConfig()
    template_renderer = JinjaRenderer(renderer_config, logger_factory)
    app_config = AppConfig()

    factory = RenderableFactory(
        template_renderer=template_renderer,
        app_config=app_config,
        registerable_configs=[system_a_config, system_b_config],
        logger_factory=logger_factory,
        injector=injector_with_default,
    )

    pipe_config = TestPipeConfig(
        id="test_pipe",
        use="tests.unit.core.config.test_renderable_factory_assisted_injection:TestPipe",
        injects={"ticket_system": "system_b"},
        params=TestPipeParams(),
    )

    context = PipeContext()
    pipe = factory.create_pipe(pipe_config, context)

    assert pipe.ticket_system.name == "SystemB"


def test_no_explicit_inject_uses_container_defaults(
    logger_factory: LoggerFactory, injector: Injector
) -> None:
    """Test that without explicit injects, container defaults are used."""

    def configure_default_ticket_system(binder):
        default_system = MockTicketSystemA(EmptyParams())
        binder.bind(TicketSystemService, to=default_system)

    injector_with_default = injector.create_child_injector([configure_default_ticket_system])

    renderer_config = JinjaRendererConfig()
    template_renderer = JinjaRenderer(renderer_config, logger_factory)
    app_config = AppConfig()

    factory = RenderableFactory(
        template_renderer=template_renderer,
        app_config=app_config,
        registerable_configs=[],
        logger_factory=logger_factory,
        injector=injector_with_default,
    )

    pipe_config = TestPipeConfig(
        id="test_pipe",
        use="tests.unit.core.config.test_renderable_factory_assisted_injection:TestPipe",
        params=TestPipeParams(),
    )

    context = PipeContext()
    pipe = factory.create_pipe(pipe_config, context)

    assert pipe.ticket_system.name == "SystemA"
