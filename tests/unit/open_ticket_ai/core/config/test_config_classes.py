from __future__ import annotations

import importlib

import pytest
from pydantic import ValidationError

from open_ticket_ai.core.pipeline.configurable_pipe_config import (
    OnType,
    RawPipeConfig,
    RenderedPipeConfig,
)
from open_ticket_ai.core.config.registerable_config import RegisterableConfig


def test_registerable_config_defaults_are_independent() -> None:
    first = RegisterableConfig()
    second = RegisterableConfig()

    assert first.id != second.id
    assert first.name == ""
    assert first.when is True
    assert first.steps == []
    assert first.use == "open_ticket_ai.base.DefaultPipe"

    first.steps.append({"use": "some.pipe"})
    assert second.steps == []

    custom = RegisterableConfig(use="collections.Counter")
    module = importlib.import_module("collections")
    assert custom.use is module.Counter


def test_rendered_pipe_config_requires_boolean_when() -> None:
    with pytest.raises(ValidationError):
        RenderedPipeConfig()

    config = RenderedPipeConfig(when=True)
    assert config.when is True
    assert config.on_failure is OnType.FAIL_CONTAINER
    assert config.on_success is OnType.CONTINUE


@pytest.mark.parametrize(
    "field,value",
    [
        ("on_failure", "finish_container"),
        ("on_success", "continue"),
    ],
)
def test_raw_pipe_config_accepts_optional_strings(field: str, value: str) -> None:
    config = RawPipeConfig(**{field: value})
    assert getattr(config, field) == value
    assert config.when == "True"


def test_raw_pipe_config_requires_string_when() -> None:
    with pytest.raises(ValidationError):
        RawPipeConfig(when=False)
