# FILE_PATH: open_ticket_ai\tests\conftest.py
import importlib
from typing import Any, TypeVar
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from open_ticket_ai.core.config.raw_config import (
    RawConfig,
    RenderedConfig,
    RenderableConfig,
)


def pytest_collection_modifyitems(config, items):
    """Skip heavy experimental tests if dependencies are missing.

    This pytest hook function checks for the availability of SpaCy and the German language model.
    If either module fails to import, marks all tests from 'test_anonymize_data.py' to be skipped.

    Modifies the test items list in-place by adding skip markers to relevant tests.

    Args:
        config (pytest.Config):
            The pytest configuration object (unused in this function but required by hook signature).
        items (list[pytest.Item]):
            List of collected test items. Will be modified in-place by adding skip markers.
    """
    try:
        importlib.import_module("spacy")
        importlib.import_module("de_core_news_sm")
    except Exception:
        skip_reason = "SpaCy or the German model is not available"
        for item in list(items):
            if "test_anonymize_data.py" in str(item.fspath):
                item.add_marker(pytest.mark.skip(reason=skip_reason))


RawConfigT = TypeVar("RawConfigT", bound=RawConfig)
RenderedConfigT = TypeVar("RenderedConfigT", bound=RenderedConfig)


class FrozenRenderableConfig(RenderableConfig[RawConfigT, RenderedConfigT]):
    """A RenderableConfig that is frozen with a pre-rendered config.
    
    This class is used for testing when you want to provide a specific
    RenderedConfig directly without going through the rendering process.
    The render() method is disabled to prevent accidental re-rendering.
    """
    
    def __init__(self, rendered_config: RenderedConfigT, raw_config: RawConfigT | None = None):
        if raw_config is None:
            raw_config = create_mock_raw_config(rendered_config)
        super().__init__(raw_config)
        self.rendered_config = rendered_config
        self._frozen = True
    
    def render(self, scope: dict[str, Any] | BaseModel) -> RenderedConfigT:
        raise RuntimeError(
            "FrozenRenderableConfig cannot be re-rendered. "
            "Use get_rendered() to access the frozen config."
        )
    
    def save_rendered(self, scope: dict[str, Any] | BaseModel) -> RenderedConfigT:
        raise RuntimeError(
            "FrozenRenderableConfig cannot be re-rendered. "
            "The config is already frozen with a specific RenderedConfig."
        )


def create_frozen_renderable_config(
    rendered_config: RenderedConfigT,
    raw_config: RawConfigT | None = None
) -> FrozenRenderableConfig[RawConfigT, RenderedConfigT]:
    """Create a FrozenRenderableConfig from a RenderedConfig.
    
    This helper function creates a RenderableConfig that is frozen with
    a specific RenderedConfig, useful for testing when you want to bypass
    the rendering process.
    
    Args:
        rendered_config: The pre-rendered configuration to use
        raw_config: Optional raw config. If not provided, a mock will be created
    
    Returns:
        A FrozenRenderableConfig instance that cannot be re-rendered
    """
    return FrozenRenderableConfig(rendered_config, raw_config)


def create_mock_raw_config(rendered_config: RenderedConfig) -> RawConfig:
    """Create a mock RawConfig based on a RenderedConfig.
    
    This creates a minimal RawConfig that would theoretically render
    to the given RenderedConfig. Useful for testing when you only
    care about the rendered result.
    
    Args:
        rendered_config: The rendered configuration to base the mock on
    
    Returns:
        A mock RawConfig instance
    """
    mock_raw = MagicMock(spec=RawConfig)
    mock_raw.model_dump.return_value = rendered_config.model_dump()
    return mock_raw


def create_renderable_from_rendered(
    rendered_config: RenderedConfigT,
    config_class: type[RenderableConfig[RawConfigT, RenderedConfigT]] | None = None
) -> RenderableConfig[RawConfigT, RenderedConfigT]:
    """Create a RenderableConfig from a RenderedConfig for testing.
    
    This is a convenience function that creates a RenderableConfig
    with a pre-set rendered configuration, useful for unit tests
    where you want to test with specific rendered values.
    
    Args:
        rendered_config: The pre-rendered configuration
        config_class: Optional specific RenderableConfig class to use.
                     If not provided, FrozenRenderableConfig is used.
    
    Returns:
        A RenderableConfig instance with the rendered config pre-set
    """
    if config_class is None:
        return FrozenRenderableConfig(rendered_config)
    
    raw_config = create_mock_raw_config(rendered_config)
    config_instance = config_class(raw_config)
    config_instance.rendered_config = rendered_config
    return config_instance


@pytest.fixture
def frozen_config_factory():
    """Factory fixture for creating frozen renderable configs.
    
    Returns a function that can be called to create FrozenRenderableConfig
    instances from RenderedConfig objects.
    
    Example:
        def test_something(frozen_config_factory):
            rendered = MyRenderedConfig(field="value")
            config = frozen_config_factory(rendered)
            my_pipe = MyPipe(config)
    """
    return create_frozen_renderable_config


@pytest.fixture
def mock_renderable_config():
    """Create a mock RenderableConfig for testing.
    
    Returns a MagicMock that behaves like a RenderableConfig
    with commonly used methods stubbed.
    """
    mock = MagicMock(spec=RenderableConfig)
    mock.rendered_config = None
    mock.get_rendered.return_value = MagicMock(spec=RenderedConfig)
    return mock
