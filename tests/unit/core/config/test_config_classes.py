from __future__ import annotations

import pytest

from open_ticket_ai.core.config.renderable import RenderableConfig
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig


def test_registerable_config_defaults_are_independent() -> None:
    first = RenderableConfig()
    second = RenderableConfig()

    assert first.id != second.id

    custom = RenderableConfig(use="collections.Counter", id="custom")
    assert custom.use == "collections.Counter"
    assert custom.id == "custom"


def test_rendered_pipe_config_should_run_field() -> None:
    config = PipeConfig()
    assert config.should_run == "True"

    config_false = PipeConfig(**{"if": False})
    assert config_false.should_run is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("if", "True"),
        ("if", "{{ some_var }}"),
        ("if", False),
    ],
)
def test_raw_pipe_config_accepts_strings_and_bools(field: str, value: str | bool) -> None:
    config = PipeConfig(**{field: value})
    assert config.if_ == value
