from __future__ import annotations

import logging
import typing
from pydoc import locate
from typing import Any

from injector import inject, singleton

from open_ticket_ai.core.config.registerable import RegisterableConfig, Registerable
from open_ticket_ai.core.pipeline import Context
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


def _locate(use: str) -> type:
    if ":" in use:
        m, c = use.split(":", 1)
        use = f"{m}.{c}"
    use_class = locate(use)
    if use_class is None:
        raise ValueError(f"Cannot locate class '{use}'")
    return typing.cast(type, locate(use))


CONTROL_KEYS = {
    "id",
    "uid",
    "use",
    "steps",
    "depends_on",
    "if",
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
    def __init__(self, template_renderer: TemplateRenderer, registerable_configs: list[RegisterableConfig]) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._template_renderer = template_renderer
        self._registerable_configs = registerable_configs

    def render_pipe_config(self, registerable_config_raw: dict[str, Any], scope: Context) -> dict[str, Any]:
        renderable_config = registerable_config_raw.copy()
        renderable_config["steps"] = []
        rendered_step_config = self._template_renderer.render_recursive(renderable_config, scope)
        rendered_step_config["steps"] = registerable_config_raw.get("steps", [])
        return rendered_step_config

    def create_pipe(
            self, parent_config_raw: dict[str, Any], pipe_config_raw: dict[str, Any], scope: Context
    ) -> Pipe:
        pipe_id = pipe_config_raw["id"]
        self._logger.info("Creating pipe '%s' with config %s", pipe_id, pipe_config_raw)
        pipe_config = resolve_config(parent_config_raw, pipe_config_raw)
        config_raw = self.render_pipe_config(pipe_config, scope)
        registerable = self.__create_registerable_instance(config_raw, scope)
        if not isinstance(registerable, Pipe):
            raise ValueError(f"Registerable with id '{pipe_id}' is not a Pipe")
        return registerable

    def __create_service_instance(self, registerable_config_raw: RegisterableConfig, scope: Context) -> Registerable:
        config_raw = self._template_renderer.render_recursive(registerable_config_raw, scope)
        return self.__create_registerable_instance(config_raw, scope)

    def __create_registerable_instance(self, registerable_config_raw: dict[str, Any], scope: Context) -> Registerable:
        registerable_config = RegisterableConfig.model_validate(registerable_config_raw)
        cls: type = _locate(registerable_config.use)
        if not issubclass(cls, Registerable):
            raise ValueError(f"Class '{registerable_config.use}' is not a Registerable")
        kwargs: dict[str, Any] = {}
        kwargs |= self.__resolve_injects(registerable_config.injects, scope)
        kwargs["config_raw"] = registerable_config_raw
        kwargs["factory"] = self
        return cls(**kwargs)

    def __resolve_injects(self, injects: dict[str, Any], scope: Context) -> dict[str, Registerable]:
        out: dict[str, Any] = {}
        for param, ref in injects.items():
            out[param] = self.__resolve_by_id(ref, scope)
        return out

    def __resolve_by_id(self, service_id: str, scope: Context) -> Any:
        for definition_config_raw in self._registerable_configs:
            definition_config = RegisterableConfig.model_validate(definition_config_raw)
            if definition_config.id != service_id:
                continue
            return self.__create_service_instance(definition_config_raw, scope)
        raise KeyError(service_id)
