import ast
import json
import os
from typing import Any

from jinja2 import pass_context
from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig


def _coerce_path_to_list(path: str | list[str] | tuple[str, ...] | None) -> list[str]:
    if path is None:
        return []

    if isinstance(path, (list, tuple)):
        return [str(p) for p in path if str(p)]

    if not isinstance(path, str):
        return [str(path)]

    p = path.strip()
    if not p:
        return []

    if p.startswith(("[", "(")) and p.endswith(("]", ")")):
        seq = _try_parse_literal(p)
        if seq is not None:
            return [str(x) for x in seq]

    return [seg for seg in p.split(".") if seg]


def _try_parse_literal(s: str) -> list[Any] | tuple[Any, ...] | None:
    try:
        seq = ast.literal_eval(s)
        if isinstance(seq, (list, tuple)):
            return seq
    except (ValueError, SyntaxError):
        pass
    return None


def _nest_value_at_path(parts: list[str], value: Any) -> dict[str, Any] | Any:
    if not parts:
        return value

    result: dict[str, Any] | Any = value
    for key in reversed(parts):
        result = {key: result}
    return result


def _serialize_to_json(obj: Any) -> str:
    try:
        return json.dumps(obj)
    except (TypeError, ValueError):
        return str(obj)


def at_path(value: Any, path: str | list[str] | tuple[str, ...] | None) -> str:
    if isinstance(value, BaseModel):
        value = value.model_dump()

    parts = _coerce_path_to_list(path)
    nested = _nest_value_at_path(parts, value)
    return _serialize_to_json(nested)


@pass_context
def has_failed(ctx: Any, pipe_id: str) -> bool:
    pipes = ctx.get("pipe_results", {})
    pipe = pipes.get(pipe_id)
    if pipe is None:
        return False
    if isinstance(pipe, PipeResult):
        return not pipe.success
    return not pipe.get("success", True)


@pass_context
def get_pipe_result(ctx: Any, pipe_id: str, data_key: str = "value") -> Any:
    pipes = ctx.get("pipe_results", {})
    pipe = pipes.get(pipe_id)
    if pipe is None:
        return None
    pipe_data = pipe.data if isinstance(pipe, PipeResult) else pipe.get("data")
    if isinstance(pipe_data, BaseModel):
        pipe_data_dict = pipe_data.model_dump()
        return pipe_data_dict.get(data_key)
    return pipe_data.get(data_key)


def build_filtered_env() -> dict[str, str]:
    return os.environ.copy()
