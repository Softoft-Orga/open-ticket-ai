from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import BaseModel, ConfigDict

from open_ticket_ai.base.loggers.stdlib_logging_adapter import create_logger_factory
from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.config_models import InfrastructureConfig, RawOpenTicketAIConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.orchestration.orchestrator_models import OrchestratorConfig
from open_ticket_ai.core.pipeline.pipe_context_model import PipeContext
from open_ticket_ai.core.renderable.renderable import Renderable
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import (
    TicketSystemService,
)
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    UnifiedEntity,
    UnifiedNote,
)
from tests.unit.mocked_ticket_system import MockedTicketSystem

pytestmark = [pytest.mark.unit]


class MutableRenderableConfig(RenderableConfig):
    """A mutable version of RenderableConfig for testing purposes."""

    model_config = ConfigDict(frozen=False, extra="forbid")


class SimpleParams(BaseModel):
    value: str = "default"


class SimpleRenderable(Renderable[SimpleParams]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return SimpleParams


@pytest.fixture
def logging_config() -> LoggingConfig:
    return LoggingConfig(level="DEBUG")


@pytest.fixture
def logger_factory(logging_config) -> LoggerFactory:
    return create_logger_factory(logging_config)


@pytest.fixture
def empty_pipeline_context() -> PipeContext:
    return PipeContext(pipe_results={}, params={})


@pytest.fixture
def mock_ticket_system_service() -> MagicMock:
    mock = MagicMock(spec=TicketSystemService)
    mock.create_ticket = AsyncMock(return_value="TICKET-123")
    mock.update_ticket = AsyncMock(return_value=True)
    mock.add_note = AsyncMock(return_value=True)
    mock.get_ticket = AsyncMock(return_value={})
    return mock


@pytest.fixture
def empty_mocked_ticket_system(logger_factory) -> MockedTicketSystem:
    return MockedTicketSystem(config=RenderableConfig(id="mocked-ticket-system"), logger_factory=logger_factory)


@pytest.fixture(scope="function")
def mocked_ticket_system(logger_factory) -> MockedTicketSystem:
    system = MockedTicketSystem(config=RenderableConfig(id="mocked-ticket-system"), logger_factory=logger_factory)

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
def valid_raw_config() -> RawOpenTicketAIConfig:
    return RawOpenTicketAIConfig(
        infrastructure=InfrastructureConfig(logging=LoggingConfig(), default_template_renderer="jinja_renderer"),
        services=[
            RenderableConfig(
                id="jinja_renderer",
                use="open_ticket_ai.base.template_renderers.jinja_renderer.JinjaRenderer",
                params={"type": "jinja"},
            )
        ],
        orchestrator=OrchestratorConfig(),
    )


@pytest.fixture
def invalid_raw_config() -> RawOpenTicketAIConfig:
    return RawOpenTicketAIConfig(
        infrastructure=InfrastructureConfig(logging=LoggingConfig(), default_template_renderer="nonexistent_renderer"),
        services=[],
        orchestrator=OrchestratorConfig(),
    )


@pytest.fixture
def mock_template_renderer() -> MagicMock:
    mock = MagicMock(spec=TemplateRenderer)
    mock.render.side_effect = lambda obj, _: obj
    return mock


@pytest.fixture
def mock_app_config() -> MagicMock:
    return MagicMock(spec=AppConfig)


@pytest.fixture
def sample_renderable_config() -> MutableRenderableConfig:
    return MutableRenderableConfig(
        id="test_renderable",
        use="tests.unit.conftest.SimpleRenderable",
        params={"value": "test_value"},
    )


@pytest.fixture
def sample_pipe_context() -> PipeContext:
    return PipeContext(
        pipe_results={},
        params={"context_key": "context_value"},
    )


@pytest.fixture
def sample_registerable_configs() -> list[MutableRenderableConfig]:
    return [
        MutableRenderableConfig(
            id="service1",
            use="tests.unit.conftest.SimpleRenderable",
            params={"value": "service1_value"},
        ),
        MutableRenderableConfig(
            id="service2",
            use="tests.unit.conftest.SimpleRenderable",
            params={"value": "service2_value"},
        ),
    ]
