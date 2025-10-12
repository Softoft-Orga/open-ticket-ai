from __future__ import annotations

import logging
import typing
from pydoc import locate
from typing import Any

from injector import inject, singleton
from pydantic import BaseModel

from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.renderable import Renderable, RenderableConfig
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


def _locate(use: str) -> type:
    if ":" in use:
        m, c = use.split(":", 1)
        use = f"{m}.{c}"
    use_class = locate(use)
    if use_class is None:
        raise ValueError(f"Cannot locate class '{use}'")
    return typing.cast(type, locate(use))


def render_base_model[T: BaseModel](config: T, scope: PipeContext, renderer: TemplateRenderer) -> T:
    rendered_dict = renderer.render_recursive(config.model_dump(), scope)
    return type(config)(**rendered_dict)


@singleton
class RenderableFactory:
    @inject
    def __init__(
        self, template_renderer: TemplateRenderer, app_config: AppConfig, registerable_configs: list[RenderableConfig]
    ):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._template_renderer = template_renderer
        self._registerable_configs = registerable_configs
        self._app_config = app_config

    def create_pipe(self, pipe_config_raw: PipeConfig, scope: PipeContext) -> Pipe:
        self._logger.debug("Creating pipe with config: %s", pipe_config_raw)
        self._logger.info("Creating pipe '%s' with config %s", pipe_config_raw.id, pipe_config_raw)
        rendered_params = render_base_model(pipe_config_raw.params, scope, self._template_renderer)
        pipe_config_raw.params = rendered_params
        registerable = self.__create_renderable_instance(pipe_config_raw, scope)
        if not isinstance(registerable, Pipe):
            raise TypeError(f"Registerable with id '{pipe_config_raw.id}' is not a Pipe")
        return registerable

    def __create_service_instance(self, registerable_config_raw: RenderableConfig, scope: PipeContext) -> Renderable:
        rendered_config = render_base_model(registerable_config_raw, scope, self._template_renderer)
        return self.__create_renderable_instance(rendered_config, scope)

    def __create_renderable_instance(self, registerable_config: RenderableConfig, scope: PipeContext) -> Renderable:
        cls: type = _locate(registerable_config.use)
        if not issubclass(cls, Renderable):
            raise TypeError(f"Class '{registerable_config.use}' is not a Registerable")
        kwargs: dict[str, Any] = {}
        kwargs |= self.__resolve_injects(registerable_config.injects, scope)
        kwargs["config"] = registerable_config
        kwargs["factory"] = self
        kwargs["app_config"] = self._app_config
        return cls(**kwargs)

    def __resolve_injects(self, injects: dict[str, Any], scope: PipeContext) -> dict[str, Renderable]:
        out: dict[str, Any] = {}
        for param, ref in injects.items():
            out[param] = self.__resolve_by_id(ref, scope)
        return out

    def __resolve_by_id(self, service_id: str, scope: PipeContext) -> Any:
        for definition_config_raw in self._registerable_configs:
            definition_config = RenderableConfig.model_validate(definition_config_raw)
            if definition_config.id != service_id:
                continue
            return self.__create_service_instance(definition_config_raw, scope)
        raise KeyError(service_id)
