import logging
import os
from collections.abc import Callable, Mapping
from types import MappingProxyType
from typing import Any

from jinja2.sandbox import SandboxedEnvironment

from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.template_rendering.jinja_registry import (
    get_registered_methods,
    get_registered_variables,
    jinja_template_method,
    jinja_variable,
)
from open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig, TemplateRendererEnvConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class JinjaRenderer(TemplateRenderer):
    def __init__(
        self,
        config: JinjaRendererConfig | None = None,
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

        if config is None:
            config = JinjaRendererConfig(
                env_config=TemplateRendererEnvConfig(
                    prefix=env_prefix,
                    extra_prefixes=env_extra_prefixes,
                    allowlist=env_allowlist,
                    denylist=env_denylist,
                    key=env_key,
                    provider=env_provider,
                    refresh_on_each_render=refresh_env_on_each_render,
                ),
                env=env,
            )

        if config.jinja_template_method is None:
            config.jinja_template_method = jinja_template_method
        if config.jinja_variable is None:
            config.jinja_variable = jinja_variable

        self.config = config
        env_config = config.env_config

        self.env = config.env or SandboxedEnvironment(
            autoescape=config.autoescape, trim_blocks=config.trim_blocks, lstrip_blocks=config.lstrip_blocks
        )

        def _build_filtered_env() -> dict[str, str]:
            src = dict(env_config.provider()) if env_config.provider else dict(os.environ)
            pref_ok = (
                {env_config.prefix, *env_config.extra_prefixes} if env_config.prefix else set(env_config.extra_prefixes)
            )

            def _pref(k: str) -> bool:
                return True if not pref_ok else any(k.startswith(p) for p in pref_ok)

            out = {k: v for k, v in src.items() if _pref(k)}
            if env_config.allowlist is not None:
                out = {k: v for k, v in out.items() if k in env_config.allowlist}
            if env_config.denylist is not None:
                out = {k: v for k, v in out.items() if k not in env_config.denylist}
            return out

        _static_env = MappingProxyType(_build_filtered_env())

        def get_env(key: str, default: str | None = None) -> str | None:
            if env_config.refresh_on_each_render:
                return _build_filtered_env().get(key, default)
            return _static_env.get(key, default)

        def get_envs() -> Mapping[str, str]:
            if env_config.refresh_on_each_render:
                return MappingProxyType(_build_filtered_env())
            return _static_env

        self.env.globals[env_config.key] = get_envs()
        self.env.globals["env_get"] = get_env

        for method_name, method_func in get_registered_methods().items():
            self.env.globals[method_name] = method_func

        for var_name, var_func in get_registered_variables().items():
            self.env.globals[var_name] = var_func()

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
