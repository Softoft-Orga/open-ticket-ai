"""Helpers for working with configuration models in tests."""

from __future__ import annotations

from typing import Any, TypeVar
from unittest.mock import MagicMock

from pydantic import BaseModel

from open_ticket_ai.core.config.raw_config import (
    RawConfig,
    RenderableConfig,
    RenderedConfig,
)

RawConfigT = TypeVar("RawConfigT", bound=RawConfig)
RenderedConfigT = TypeVar("RenderedConfigT", bound=RenderedConfig)


class FrozenRenderableConfig(RenderableConfig[RawConfigT, RenderedConfigT]):
    """RenderableConfig variant that cannot be rendered again."""

    def __init__(self, rendered_config: RenderedConfigT, raw_config: RawConfigT | None = None):
        if raw_config is None:
            raw_config = create_mock_raw_config(rendered_config)
        super().__init__(raw_config)
        self.rendered_config = rendered_config
        self._frozen = True

    def render(self, scope: dict[str, Any] | BaseModel) -> RenderedConfigT:  # pragma: no cover - defensive guard
        raise RuntimeError(
            "FrozenRenderableConfig cannot be re-rendered. Use get_rendered() to access the frozen config."
        )

    def save_rendered(self, scope: dict[str, Any] | BaseModel) -> RenderedConfigT:  # pragma: no cover - defensive guard
        raise RuntimeError(
            "FrozenRenderableConfig cannot be re-rendered. The config is already frozen with a specific RenderedConfig."
        )


def create_mock_raw_config(rendered_config: RenderedConfigT) -> RawConfigT:
    """Create a RawConfig mock that mirrors a rendered configuration."""

    mock_raw = MagicMock(spec=RawConfig)
    mock_raw.model_dump.return_value = rendered_config.model_dump()
    return mock_raw  # type: ignore[return-value]


def create_frozen_renderable_config(
    rendered_config: RenderedConfigT,
    raw_config: RawConfigT | None = None,
) -> FrozenRenderableConfig[RawConfigT, RenderedConfigT]:
    """Build a FrozenRenderableConfig from a rendered configuration."""

    return FrozenRenderableConfig(rendered_config, raw_config)


def create_renderable_from_rendered(
    rendered_config: RenderedConfigT,
    config_class: type[RenderableConfig[RawConfigT, RenderedConfigT]] | None = None,
) -> RenderableConfig[RawConfigT, RenderedConfigT]:
    """Construct a RenderableConfig seeded with a rendered configuration."""

    if config_class is None:
        return FrozenRenderableConfig(rendered_config)

    raw_config = create_mock_raw_config(rendered_config)
    config_instance = config_class(raw_config)
    config_instance.rendered_config = rendered_config
    return config_instance
