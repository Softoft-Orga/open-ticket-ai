import ast
import json
import logging
from typing import Any

from jinja2.sandbox import SandboxedEnvironment
from pydantic import BaseModel

from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class JinjaRenderer(TemplateRenderer):
    def __init__(self, env: SandboxedEnvironment | None = None):
        self.env = env or SandboxedEnvironment(autoescape=False, trim_blocks=True, lstrip_blocks=True)
        self.env.filters.setdefault("at_path", self._at_path)

    @staticmethod
    def _coerce_path(path: Any) -> list[str]:
        if path is None:
            return []
        if isinstance(path, (list, tuple)):
            return [str(p) for p in path if str(p)]
        if isinstance(path, str):
            p = path.strip()
            if not p:
                return []
            if (p.startswith("[") and p.endswith("]")) or (p.startswith("(") and p.endswith(")")):
                try:
                    seq = ast.literal_eval(p)
                    if isinstance(seq, (list, tuple)):
                        return [str(x) for x in seq]
                except Exception:
                    pass
            return [seg for seg in p.split(".") if seg]
        return [str(path)]

    @staticmethod
    def _nest_value(parts: list[str], value: Any) -> Any:
        d: Any = value
        for key in reversed(parts):
            d = {key: d}
        return d

    def _at_path(self, value: Any, path: Any) -> str:
        if isinstance(value, BaseModel):
            value = value.model_dump()
        parts = self._coerce_path(path)
        nested = self._nest_value(parts, value) if parts else value
        try:
            return json.dumps(nested)
        except Exception:
            return str(nested)

    def render(self, template_str: str, scope: Context, fail_silently: bool = False) -> Any:
        def has_failed(pipe_id: str):
            return scope.pipes[pipe_id].failed if pipe_id in scope.pipes else False

        def get_pipe_result(pipe_id: str, data_key: str = 'value'):
            if not pipe_id in scope.pipes:
                return None
            pipe = scope.pipes[pipe_id]
            if not data_key in pipe.data:
                return None
            return pipe.data[data_key]

        self.env.globals["has_failed"] = has_failed
        self.env.globals["get_pipe_result"] = get_pipe_result
        scope_dict = self._normalize_scope(scope)
        try:
            template = self.env.from_string(template_str)
            rendered = template.render(scope_dict)
            return self._parse_rendered_value(rendered)
        except Exception as e:
            logging.exception(f"Template rendering failed: {e}")
            if fail_silently:
                return template_str
            raise e
