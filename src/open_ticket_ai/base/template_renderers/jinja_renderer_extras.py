import logging
import re
from typing import Any

import jinja2
from pydantic import BaseModel

from open_ticket_ai.core.pipes.pipe_models import PipeResult


class FailMarker:
    pass


def _nest_value_at_path(value: dict[str, Any] | Any, parts: list[str]) -> dict[str, Any] | Any:
    if len(parts) == 0:
        return value
    return _nest_value_at_path(value[parts[0]], parts[1:])


def at_path(value: dict | BaseModel, path: str) -> dict[str, Any] | Any:
    if re.match(r"^[^.]+\..+$", path) is None:
        raise AttributeError("Path must match the format '*.*'")
    if isinstance(value, BaseModel):
        value = value.model_dump()

    parts = path.split(".")
    return _nest_value_at_path(value, parts)


def _get_pipe(ctx: jinja2.runtime.Context, pipe_id: str) -> PipeResult:
    pipe = ctx.get("pipe_results", {}).get(pipe_id)
    if pipe is None:
        raise KeyError(f"Pipe {pipe_id} not found")
    return PipeResult.model_validate(pipe)


@jinja2.pass_context
def has_failed(ctx: jinja2.runtime.Context, pipe_id: str) -> bool:
    return _get_pipe(ctx, pipe_id).has_failed()


@jinja2.pass_context
def get_pipe_result(ctx: jinja2.runtime.Context, pipe_id: str, data_key: str = "value") -> Any:
    result = _get_pipe(ctx, pipe_id).data.get(data_key)
    logging.debug(f"Pipe result {pipe_id} has {data_key}: {result}")
    if result is None:
        raise KeyError(
            f"Data key '{data_key}' not found in pipe '{pipe_id}' result; ctx data: {_get_pipe(ctx, pipe_id).data}"
        )
    return result


def fail() -> FailMarker:
    return FailMarker()
