from pathlib import Path
from typing import Any, ClassVar
from unittest.mock import AsyncMock, MagicMock

import pytest
from injector import AssistedBuilder, Injector
from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import InfrastructureConfig, OpenTicketAIConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig, InjectableConfigBase
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.logging.stdlib_logging_adapter import create_logger_factory
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedEntity, UnifiedNote
from tests.mocked_ticket_system import MockedTicketSystem

pytestmark = [pytest.mark.unit]


class MutablePipeConfig(PipeConfig):
    """A mutable version of PipeConfig for testing purposes."""

    model_config = ConfigDict(frozen=False, extra="forbid")


class MutableTriggerConfig(PipeConfig):
    """A mutable version of TriggerConfig for testing purposes."""

    model_config = ConfigDict(frozen=False, extra="forbid")


class MutableRenderableConfig(InjectableConfig):
    """A mutable version of RenderableConfig for testing purposes."""

    model_config = ConfigDict(frozen=False, extra="forbid")


class SimpleParams(BaseModel):
    value: str = Field(default="default_value")


class SimpleInjectable(Injectable[SimpleParams]):
    ParamsModel: ClassVar[type[BaseModel]] = SimpleParams


class SimplePipe(Pipe[SimpleParams]):
    ParamsModel: ClassVar[type[BaseModel]] = SimpleParams

    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)

    async def _process(self, _: PipeContext) -> PipeResult:
        return PipeResult.success(data={"value": self._params.value})


class SimpleTrigger(Pipe[SimpleParams]):
    ParamsModel: ClassVar[type[BaseModel]] = SimpleParams

    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)

    def _should_trigger(self) -> bool:
        return True


@pytest.fixture
def app_module():
    some_path = Path(__file__)
    return AppModule(some_path)


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
    return MockedTicketSystem(config=InjectableConfig(id="mocked-ticket-system"), logger_factory=logger_factory)


@pytest.fixture(scope="function")
def mocked_ticket_system(logger_factory) -> MockedTicketSystem:
    system = MockedTicketSystem(config=InjectableConfig(id="mocked-ticket-system"), logger_factory=logger_factory)

    # Clear any data from previous tests (global store isolation)
    system.clear_all_data()

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

    yield system

    # Clean up after test to prevent leakage to next test
    system.clear_all_data()


@pytest.fixture
def valid_raw_config() -> OpenTicketAIConfig:
    return OpenTicketAIConfig(
        infrastructure=InfrastructureConfig(logging=LoggingConfig(), default_template_renderer="jinja_renderer"),
        services={
            "jinja_renderer": InjectableConfigBase(
                use="open_ticket_ai.otai_base.template_renderers.jinja_renderer.JinjaRenderer",
                params={"type": "jinja"},
            )
        },
        orchestrator=PipeConfig(),
    )


@pytest.fixture
def invalid_raw_config() -> OpenTicketAIConfig:
    return OpenTicketAIConfig(
        infrastructure=InfrastructureConfig(logging=LoggingConfig()),
        services=[],
        orchestrator=PipeConfig(),
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


@pytest.fixture
def mock_injector() -> MagicMock:
    mock = MagicMock(spec=Injector)
    mock_builder = MagicMock(spec=AssistedBuilder)
    mock_builder.build.side_effect = lambda config, pipe_context, **kwargs: SimplePipe(
        config=config, pipe_context=pipe_context, logger_factory=create_logger_factory(LoggingConfig()), **kwargs
    )
    mock.get.return_value = mock_builder
    return mock


@pytest.fixture
def mock_otai_config() -> MagicMock:
    mock = MagicMock(spec=OpenTicketAIConfig)
    mock.get_services_list.return_value = []
    return mock


@pytest.fixture
def mock_component_registry() -> MagicMock:
    return MagicMock(spec=ComponentRegistry)
