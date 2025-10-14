from __future__ import annotations

from open_ticket_ai.core.pipeline.pipe_config import PipeConfig
from open_ticket_ai.core.renderable.renderable import RenderableConfig


def test_registerable_config_defaults() -> None:
    first: RenderableConfig = RenderableConfig()
    second: RenderableConfig = RenderableConfig()
    assert first.id != second.id


def test_pipe_config_should_run() -> None:
    config: PipeConfig = PipeConfig()
    assert config.should_run == "True"
