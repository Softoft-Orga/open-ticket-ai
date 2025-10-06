from __future__ import annotations

import pytest

from open_ticket_ai.core.config.registerable_config import RegisterableConfig
from open_ticket_ai.core.pipeline.pipe_config import (
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
    # if field has a default value of True
    config = RenderedPipeConfig()
    assert config.should_run is True

    config_false = RenderedPipeConfig(**{"if": False})
    assert config_false.should_run is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("if", "True"),
        ("if", "{{ some_var }}"),
    ],
)
def test_raw_pipe_config_accepts_optional_strings(field: str, value: str) -> None:
    config = RawPipeConfig(**{field: value})
    # Access the field using if_ attribute since 'if' is aliased
    assert config.if_ == value


def test_raw_pipe_config_requires_string_when() -> None:
    # if field accepts both str and bool, with default "True"
    config_bool = RawPipeConfig(**{"if": False})
    assert config_bool.if_ is False

    config_str = RawPipeConfig(**{"if": "{{ some_condition }}"})
    assert config_str.if_ == "{{ some_condition }}"
