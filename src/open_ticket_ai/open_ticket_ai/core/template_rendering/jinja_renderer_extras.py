import ast
import json
import os
from json import JSONDecodeError
from typing import Any

from jinja2 import pass_context
from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.template_rendering import JinjaRendererConfig


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
    except JSONDecodeError:
        return str(nested)

@pass_context
def has_failed(ctx, pipe_id: str) -> bool:
    pipes = ctx.get("pipes", {})
    pipe = pipes.get(pipe_id)
    if pipe is None:
        return False
    return pipe.failed or pipe.get("failed")

@pass_context
def pipe_result(ctx, pipe_id: str, data_key: str = "value") -> Any:
    pipes = ctx.get("pipes", {})
    pipe = pipes.get(pipe_id)
    if pipe is None:
        return None
    pipe_data = pipe.data if isinstance(pipe, PipeResult) else pipe.get("data")
    return pipe_data.get(data_key)


def build_filtered_env(jinja_renderer_config: JinjaRendererConfig) -> dict[str, str]:
    env_config = jinja_renderer_config.env_config

    def _pref(k: str) -> bool:
        return True if not env_config.prefix else k.startswith(env_config.prefix)

    out = {k: v for k, v in dict(os.environ).items() if _pref(k)}
    if env_config.allowlist is not None:
        out = {k: v for k, v in out.items() if k in env_config.allowlist}
    if env_config.denylist is not None:
        out = {k: v for k, v in out.items() if k not in env_config.denylist}
    return out