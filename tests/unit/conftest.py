from unittest.mock import AsyncMock, MagicMock

import pytest

from open_ticket_ai.core.config.raw_config import (
    RawConfig,
    RenderedConfig,
    RenderableConfig,
)
from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.configurable_pipe_config import (
    RenderedPipeConfig,
)
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import (
    TicketSystemService,
)
from tests.conftest import (
    FrozenRenderableConfig,
    create_frozen_renderable_config,
)


@pytest.fixture
def empty_pipeline_context() -> PipelineContext:
    return PipelineContext(pipes={}, config={})


@pytest.fixture
def mock_ticket_system_service() -> MagicMock:
    mock = MagicMock(spec=TicketSystemService)
    mock.create_ticket = AsyncMock(return_value="TICKET-123")
    mock.update_ticket = AsyncMock(return_value=True)
    mock.add_note = AsyncMock(return_value=True)
    mock.get_ticket = AsyncMock(return_value={})
    return mock


@pytest.fixture
def rendered_pipe_config_factory():
    def factory(**kwargs) -> RenderedPipeConfig:
        defaults = {
            "id": "test_pipe",
            "use": "open_ticket_ai.basic_pipes.DefaultPipe",
            "when": True,
        }
        defaults.update(kwargs)

        class CustomRenderedPipeConfig(RenderedPipeConfig):
            pass

        return CustomRenderedPipeConfig(
            id=defaults["id"],
            use=defaults["use"],
            when=defaults.get("when", True)
        )

    return factory


@pytest.fixture
def frozen_pipe_config_factory(rendered_pipe_config_factory):
    def factory(**kwargs) -> FrozenRenderableConfig:
        rendered_config = rendered_pipe_config_factory(**kwargs)
        return create_frozen_renderable_config(rendered_config)

    return factory


@pytest.fixture
def raw_config_with_jinja():
    class TestRawConfig(RawConfig):
        name: str = "{{ test_name }}"
        value: str = "{{ test_value | upper }}"
        items: list[str] = ["{{ item1 }}", "{{ item2 }}"]

    return TestRawConfig()


@pytest.fixture
def rendered_config_sample():
    class TestRenderedConfig(RenderedConfig):
        name: str
        value: str
        items: list[str]

    return TestRenderedConfig(
        name="Test Name",
        value="TEST VALUE",
        items=["item_one", "item_two"]
    )


@pytest.fixture
def create_frozen_config():
    return create_frozen_renderable_config


@pytest.fixture
def mock_registry():
    mock = MagicMock(spec=UnifiedRegistry)
    mock.get_pipe_class.return_value = MagicMock()
    mock.get_service_class.return_value = MagicMock()
    mock.build_pipe_instance.return_value = MagicMock()
    mock.get_instance.return_value = MagicMock()

    return mock


@pytest.fixture
def renderable_config_assertions():
    class ConfigAssertions:
        @staticmethod
        def assert_is_frozen(config: RenderableConfig) -> None:
            assert isinstance(config, FrozenRenderableConfig)
            assert config._frozen is True

            with pytest.raises(RuntimeError, match="cannot be re-rendered"):
                config.render({})

            with pytest.raises(RuntimeError, match="cannot be re-rendered"):
                config.save_rendered({})

        @staticmethod
        def assert_config_equals(
                config: RenderableConfig,
                expected_rendered: RenderedConfig
        ) -> None:
            actual = config.get_rendered()
            assert actual.model_dump() == expected_rendered.model_dump()

        @staticmethod
        def assert_can_get_rendered(config: RenderableConfig) -> None:
            rendered = config.get_rendered()
            assert rendered is not None
            assert isinstance(rendered, RenderedConfig)

    return ConfigAssertions()
