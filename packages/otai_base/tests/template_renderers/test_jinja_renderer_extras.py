from __future__ import annotations

from unittest.mock import MagicMock

import jinja2
import pytest
from open_ticket_ai import TemplateRenderError
from open_ticket_ai.core.pipes.pipe_models import PipeResult
from pydantic import BaseModel

from otai_base.template_renderers.jinja_renderer_extras import (
    _get_pipe,
    at_path,
)


class SampleModel(BaseModel):
    p1: dict[str, str]


def test_at_path_with_valid_nested_dict() -> None:
    data = {"p1": {"p2": "test"}}
    result = at_path(data, "p1.p2")
    assert result == "test"


def test_at_path_with_multiple_levels() -> None:
    data = {"level1": {"level2": {"level3": "value"}}}
    result = at_path(data, "level1.level2.level3")
    assert result == "value"


def test_at_path_with_pydantic_model() -> None:
    model = SampleModel(p1={"p2": "test"})
    result = at_path(model, "p1.p2")
    assert result == "test"


def test_at_path_with_colon_separator_raises_error() -> None:
    data = {"p1": {"p2": "test"}}
    with pytest.raises(AttributeError, match="Path must match the format"):
        at_path(data, "p1:p2")


def test_at_path_with_underscore_separator_raises_error() -> None:
    data = {"p1": {"p2": "test"}}
    with pytest.raises(AttributeError, match="Path must match the format"):
        at_path(data, "p1_p2")


def test_at_path_with_bracket_notation_raises_error() -> None:
    data = {"p1": {"p2": "test"}}
    with pytest.raises(AttributeError, match="Path must match the format"):
        at_path(data, "[p1][p2]")


def test_at_path_with_no_separator_raises_error() -> None:
    data = {"p1": {"p2": "test"}}
    with pytest.raises(AttributeError, match="Path must match the format"):
        at_path(data, "p1")


def test_get_pipe_raises_key_error_when_pipe_not_found() -> None:
    mock_ctx = MagicMock(spec=jinja2.runtime.Context)
    mock_ctx.get.return_value = {}

    with pytest.raises(TemplateRenderError, match=".*nonexistent.*"):
        _get_pipe(mock_ctx, "nonexistent")


def test_get_pipe_returns_pipe_result_when_found() -> None:
    pipe_result = PipeResult(succeeded=True, data={"value": "test"})
    mock_ctx = MagicMock(spec=jinja2.runtime.Context)
    mock_ctx.get.return_value = {"test_pipe": pipe_result.model_dump()}

    result = _get_pipe(mock_ctx, "test_pipe")

    assert isinstance(result, PipeResult)
    assert result.succeeded is True
    assert result.data["value"] == "test"
