import ast
import json
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.template_rendering.jinja_registry import jinja_template_method, jinja_variable


@jinja_template_method("at_path")
def at_path(value: Any, path: Any) -> str:
    def _coerce_path(path: Any) -> list[str]:
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
            try:
                seq = ast.literal_eval(p)
                if isinstance(seq, (list, tuple)):
                    return [str(x) for x in seq]
            except Exception:
                pass

        return [seg for seg in p.split(".") if seg]

    def _nest_value(parts: list[str], value: Any) -> Any:
        result = value
        for key in reversed(parts):
            result = {key: result}
        return result

    if isinstance(value, BaseModel):
        value = value.model_dump()
    parts = _coerce_path(path)
    nested = _nest_value(parts, value) if parts else value
    try:
        return json.dumps(nested)
    except Exception:
        return str(nested)


@jinja_template_method("has_failed")
def has_failed_factory(scope: dict[str, Any]) -> callable:
    def has_failed(pipe_id: str) -> bool:
        pipes = scope.get("pipes", {})
        pipe = pipes.get(pipe_id)
        if pipe is None:
            return False
        return pipe.failed or pipe.get("failed")
    return has_failed


@jinja_template_method("pipe_result")
def pipe_result_factory(scope: dict[str, Any]) -> callable:
    def pipe_result(pipe_id: str, data_key: str = "value") -> Any:
        pipes = scope.get("pipes", {})
        pipe = pipes.get(pipe_id)
        if pipe is None:
            return None
        pipe_data = pipe.data if isinstance(pipe, PipeResult) else pipe.get("data")
        return pipe_data.get(data_key)
    return pipe_result


@jinja_template_method("example_function")
def example_function(value: str) -> str:
    return value.upper()


@jinja_variable("example_variable")
def example_variable() -> str:
    return "example_value"
