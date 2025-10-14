import ast
import json
import os
from typing import Any

from jinja2 import pass_context
from pydantic import BaseModel


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
    pipe = ctx.get("pipe_results", {}).get(pipe_id)
    return pipe is None or not pipe.get("success", True)


@pass_context
def get_pipe_result(ctx: Any, pipe_id: str, data_key: str = "value") -> Any:
    pipe = ctx.get("pipe_results", {}).get(pipe_id)
    if pipe is None:
        return None
    return pipe.get("data").get(data_key)


def build_filtered_env() -> dict[str, str]:
    return os.environ.copy()
