import ast
import json
import logging
import os
from types import MappingProxyType
from typing import Any
from typing import Mapping, Callable

from jinja2.sandbox import SandboxedEnvironment
from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer
from open_ticket_ai.core.template_rendering.jinja_registry import (
    get_registered_methods,
    get_registered_variables,
)


class JinjaRenderer(TemplateRenderer):
    def __init__(
        self,
        env: SandboxedEnvironment | None = None,
        env_prefix: str = "OTAI_",
        env_extra_prefixes: tuple[str, ...] = (),
        env_allowlist: set[str] | None = None,
        env_denylist: set[str] | None = None,
        env_key: str = "env",
        env_provider: Callable[[], Mapping[str, str]] | None = None,
        refresh_env_on_each_render: bool = False,
    ):
        self._logger = logging.getLogger(__name__)
        self.env = env or SandboxedEnvironment(autoescape=False, trim_blocks=True, lstrip_blocks=True)
        self.env.filters.setdefault("at_path", self._at_path)

        def _build_filtered_env() -> dict[str, str]:
            src = dict(env_provider()) if env_provider else dict(os.environ)
            pref_ok = {env_prefix, *env_extra_prefixes} if env_prefix else set(env_extra_prefixes)

            def _pref(k: str) -> bool:
                return True if not pref_ok else any(k.startswith(p) for p in pref_ok)

            out = {k: v for k, v in src.items() if _pref(k)}
            if env_allowlist is not None:
                out = {k: v for k, v in out.items() if k in env_allowlist}
            if env_denylist is not None:
                out = {k: v for k, v in out.items() if k not in env_denylist}
            return out

        _static_env = MappingProxyType(_build_filtered_env())

        def get_env(key: str, default: str | None = None) -> str | None:
            if refresh_env_on_each_render:
                return _build_filtered_env().get(key, default)
            return _static_env.get(key, default)

        def get_envs() -> Mapping[str, str]:
            if refresh_env_on_each_render:
                return MappingProxyType(_build_filtered_env())
            return _static_env

        self.env.globals[env_key] = get_envs()
        self.env.globals["env_get"] = get_env

        for method_name, method_func in get_registered_methods().items():
            self.env.globals[method_name] = method_func

        for var_name, var_func in get_registered_variables().items():
            self.env.globals[var_name] = var_func()

    @staticmethod
    def _coerce_path(path: Any) -> list[str]:
        if path is None:
            return []
        if isinstance(path, list | tuple):
            return [str(p) for p in path if str(p)]
        if not isinstance(path, str):
            return [str(path)]

        p = path.strip()
        if not p:
            return []

        if p.startswith(("[", "(")) and p.endswith(("]", ")")):
            try:
                seq = ast.literal_eval(p)
                if isinstance(seq, list | tuple):
                    return [str(x) for x in seq]
            except Exception:
                pass

        return [seg for seg in p.split(".") if seg]

    @staticmethod
    def _nest_value(parts: list[str], value: Any) -> Any:
        result = value
        for key in reversed(parts):
            result = {key: result}
        return result

    def _at_path(self, value: Any, path: Any) -> str:
        if isinstance(value, BaseModel):
            value = value.model_dump()
        parts = self._coerce_path(path)
        nested = self._nest_value(parts, value) if parts else value
        try:
            return json.dumps(nested)
        except Exception:
            return str(nested)

    def render(self, template_str: str, scope: dict[str, Any], fail_silently: bool = False) -> Any:
        def has_failed(pipe_id: str) -> bool:
            pipes = scope.get("pipes", {})
            pipe = pipes.get(pipe_id)
            if pipe is None:
                return False
            return pipe.failed or pipe.get("failed")

        def pipe_result(pipe_id: str, data_key: str = "value") -> Any:
            pipes = scope.get("pipes", {})
            pipe = pipes.get(pipe_id)
            if pipe is None:
                return None
            pipe_data = pipe.data if isinstance(pipe, PipeResult) else pipe.get("data")
            return pipe_data.get(data_key)

        self.env.globals["has_failed"] = has_failed
        self.env.globals["pipe_result"] = pipe_result

        try:
            template = self.env.from_string(template_str)
            rendered = template.render(self._normalize_scope(scope))
            return self._parse_rendered_value(rendered)
        except Exception:
            self._logger.warning("Failed to render template '%s'", template_str)
            self._logger.warning("context: %s", scope)
            self._logger.exception("Template rendering failed")
            if fail_silently:
                return template_str
            raise
