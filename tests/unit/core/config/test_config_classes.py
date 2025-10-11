from __future__ import annotations

import pytest

from open_ticket_ai.core.config.registerable import RegisterableConfig
from open_ticket_ai.core.pipeline.pipe_config import (
    RawPipeConfig,
    RenderedPipeConfig,
)


def test_registerable_config_defaults_are_independent() -> None:
    first = RegisterableConfig()
    second = RegisterableConfig()

    assert first.id != second.id

    custom = RegisterableConfig(use="collections.Counter", id="custom")
    assert custom.use == "collections.Counter"
    assert custom.id == "custom"


def test_rendered_pipe_config_should_run_field() -> None:
    config = RenderedPipeConfig()
    assert config.should_run is True

    config_false = RenderedPipeConfig(**{"if": False})
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
    config = RawPipeConfig(**{field: value})
    assert config.if_ == value
