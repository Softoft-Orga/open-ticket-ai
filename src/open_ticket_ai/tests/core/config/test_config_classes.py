from __future__ import annotations

import pytest

from open_ticket_ai.open_ticket_ai.core.config.registerable_config import RegisterableConfig
from open_ticket_ai.open_ticket_ai.core.pipeline.pipe_config import (
    RawPipeConfig,
    RenderedPipeConfig,
)


def test_registerable_config_defaults_are_independent() -> None:
    first = RegisterableConfig()
    second = RegisterableConfig()

    assert first.id != second.id
    assert first.use == "open_ticket_ai.base.CompositePipe"

    custom = RegisterableConfig(use="collections.Counter", id="custom")
    assert custom.use == "collections.Counter"
    assert custom.id == "custom"


def test_rendered_pipe_config_requires_boolean_when() -> None:
    # _if has a default value of True
    config = RenderedPipeConfig()
    assert config.should_run is True

    config_false = RenderedPipeConfig(_if=False)
    assert config_false.should_run is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("_if", "True"),
        ("_if", "{{ some_var }}"),
    ],
)
def test_raw_pipe_config_accepts_optional_strings(field: str, value: str) -> None:
    config = RawPipeConfig(**{field: value})
    assert getattr(config, field) == value


def test_raw_pipe_config_requires_string_when() -> None:
    # _if accepts both str and bool, with default "True"
    config_bool = RawPipeConfig(_if=False)
    assert config_bool._if is False

    config_str = RawPipeConfig(_if="{{ some_condition }}")
    assert config_str._if == "{{ some_condition }}"
