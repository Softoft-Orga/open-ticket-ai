from __future__ import annotations

import typing
from pydoc import locate
from typing import Any

from injector import Injector, inject, singleton

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.config.registerable_config import RegisterableConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


def _locate(use: str) -> type:
    if ":" in use:
        m, c = use.split(":", 1)
        return typing.cast(type, locate(f"{m}.{c}"))
    return typing.cast(type, locate(use))


CONTROL_KEYS = {
    "id", "uid", "use", "steps", "when", "run_before_children",
    "on_failure", "on_success", "depends_on", "if"
}


def extract_config_fields(raw: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in raw.items() if k not in CONTROL_KEYS}


def deep_merge(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    out.update(a)
    for k, v in b.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def resolve_config(parent_config: dict[str, Any] | None, node_raw: dict[str, Any]) -> dict[str, Any]:
    parent_cfg = extract_config_fields(parent_config) or {}
    return deep_merge(parent_cfg, node_raw)


@singleton
class PipeFactory:
    @inject
    def __init__(self, injector: Injector, app_config: RawOpenTicketAIConfig, template_renderer: TemplateRenderer):
        self._injector = injector
        self._app_config: RawOpenTicketAIConfig = app_config
        self._template_renderer = template_renderer

    def create_pipe(self, parent_config_raw: dict[str, Any], pipe_config_raw: dict[str, Any],
                    scope: dict[str, Any]) -> Any:
        pipe_config = resolve_config(parent_config_raw, pipe_config_raw)
        return self.create_registerable_instance(pipe_config, scope)

    def create_registerable_instance(self, registerable_config_raw: dict[str, Any], scope: dict[str, Any]) -> Any:
        rendered_step_config = self._template_renderer.render_recursive(registerable_config_raw, scope)
        registerable_config = RegisterableConfig.model_validate(rendered_step_config)
        cls: type = _locate(registerable_config.use)
        kwargs: dict[str, Any] = {}
        kwargs |= self._resolve_injects(registerable_config.injects, scope)
        kwargs["config"] = registerable_config
        return self._injector.create_object(cls, additional_kwargs=kwargs)

    def _resolve_injects(self, injects: dict[str, Any], scope: dict[str, Any]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for param, ref in injects.items():
            out[param] = self._resolve_by_id(ref, scope)
        return out

    def _resolve_by_id(self, service_id: str, scope: dict[str, Any]) -> Any:
        for definition_config_raw in self._app_config.defs:
            definition_config = RegisterableConfig.model_validate(definition_config_raw)
            if definition_config.id != service_id:
                continue
            return self.create_registerable_instance(definition_config_raw, scope)
        raise KeyError(service_id)
