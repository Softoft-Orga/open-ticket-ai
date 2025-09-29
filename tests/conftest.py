"""Top level pytest configuration and shared fixtures."""

from __future__ import annotations

import importlib
from unittest.mock import MagicMock

import pytest

from open_ticket_ai.core.config.raw_config import RenderableConfig, RenderedConfig
from tests.helpers import (
    FrozenRenderableConfig,
    create_frozen_renderable_config,
    create_mock_raw_config,
    create_renderable_from_rendered,
)

__all__ = [
    "FrozenRenderableConfig",
    "create_frozen_renderable_config",
    "create_mock_raw_config",
    "create_renderable_from_rendered",
]


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip heavy experimental tests if dependencies are missing."""

    try:
        importlib.import_module("spacy")
        importlib.import_module("de_core_news_sm")
    except Exception:
        skip_reason = "SpaCy or the German model is not available"
        for item in list(items):
            if "test_anonymize_data.py" in str(item.fspath):
                item.add_marker(pytest.mark.skip(reason=skip_reason))


@pytest.fixture
def frozen_config_factory():
    """Factory fixture for creating frozen renderable configs."""

    return create_frozen_renderable_config


@pytest.fixture
def mock_renderable_config() -> MagicMock:
    """Create a mock ``RenderableConfig`` for testing."""

    mock = MagicMock(spec=RenderableConfig)
    mock.rendered_config = None
    mock.get_rendered.return_value = MagicMock(spec=RenderedConfig)
    return mock


@pytest.fixture
def renderable_from_rendered_factory():
    """Fixture returning the helper for seeding renderable configs."""

    return create_renderable_from_rendered


@pytest.fixture
def raw_config_factory():
    """Fixture exposing ``create_mock_raw_config`` for convenience."""

    return create_mock_raw_config
