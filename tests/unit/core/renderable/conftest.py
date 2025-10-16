from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe_context_model import PipeContext
from open_ticket_ai.core.renderable.renderable import Renderable
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class SimpleParams(BaseModel):
    value: str = "default"


class SimpleRenderable(Renderable[SimpleParams]):
    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return SimpleParams


@pytest.fixture
def mock_template_renderer() -> MagicMock:
    mock = MagicMock(spec=TemplateRenderer)
    mock.render.side_effect = lambda obj, _: obj
    return mock


@pytest.fixture
def mock_app_config() -> MagicMock:
    return MagicMock(spec=AppConfig)


@pytest.fixture
def mock_logger_factory() -> MagicMock:
    mock = MagicMock(spec=LoggerFactory)
    mock.create.return_value = MagicMock()
    return mock


@pytest.fixture
def sample_renderable_config() -> RenderableConfig:
    return RenderableConfig(
        id="test_renderable",
        use="tests.unit.core.renderable.conftest.SimpleRenderable",
        params={"value": "test_value"},
    )


@pytest.fixture
def sample_pipe_context() -> PipeContext:
    return PipeContext(
        pipe_results={},
        params={"context_key": "context_value"},
    )


@pytest.fixture
def sample_registerable_configs() -> list[RenderableConfig]:
    return [
        RenderableConfig(
            id="service1",
            use="tests.unit.core.renderable.conftest.SimpleRenderable",
            params={"value": "service1_value"},
        ),
        RenderableConfig(
            id="service2",
            use="tests.unit.core.renderable.conftest.SimpleRenderable",
            params={"value": "service2_value"},
        ),
    ]
