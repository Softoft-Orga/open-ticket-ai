"""Factories and helpers for pipeline related tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

from open_ticket_ai.core.pipeline.configurable_pipe_config import RenderedPipeConfig


@dataclass
class PipeConfigFactory:
    """Factory for building ``RenderedPipeConfig`` instances for tests."""

    defaults: Mapping[str, Any] = field(
        default_factory=lambda: {
            "id": "test_pipe",
            "use": "open_ticket_ai.basic_pipes.DefaultPipe",
            "when": True,
        }
    )
    model: type[RenderedPipeConfig] = field(
        default_factory=lambda: type("TestRenderedPipeConfig", (RenderedPipeConfig,), {})
    )

    def __call__(self, **overrides: Any) -> RenderedPipeConfig:
        """Create a ``RenderedPipeConfig`` instance with optional overrides."""

        payload = dict(self.defaults)
        payload.update(overrides)
        return self.model(**payload)

    def with_defaults(self, **defaults: Any) -> "PipeConfigFactory":
        """Return a new factory instance with updated defaults."""

        merged = dict(self.defaults)
        merged.update(defaults)
        return PipeConfigFactory(defaults=merged, model=self.model)

    def using_model(self, model: type[RenderedPipeConfig]) -> "PipeConfigFactory":
        """Return a new factory that uses a custom ``RenderedPipeConfig`` subclass."""

        return PipeConfigFactory(defaults=self.defaults, model=model)

    @classmethod
    def create(cls, configurator: Callable[["PipeConfigFactory"], Mapping[str, Any]] | None = None) -> RenderedPipeConfig:
        """Convenience helper for one-off ``RenderedPipeConfig`` creation."""

        factory = cls()
        payload = factory.defaults if configurator is None else configurator(factory)
        return factory(**payload)
