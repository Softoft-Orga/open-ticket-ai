from __future__ import annotations

import typing
from pydoc import locate
from typing import Any

from injector import inject, singleton

from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.renderable.renderable import Renderable
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


@singleton
class RenderableFactory:
    @inject
    def __init__(
        self,
        template_renderer: TemplateRenderer,
        app_config: AppConfig,
        registerable_configs: list[RenderableConfig],
        logger_factory: LoggerFactory,
    ):
        self._logger = logger_factory.create(self.__class__.__name__)
        self._template_renderer = template_renderer
        self._registerable_configs = registerable_configs
        self._app_config = app_config
        self._logger_factory = logger_factory

    def render(self, registerable_config_raw: RenderableConfig, scope: PipeContext):
        rendered_params = self._template_renderer.render_recursive(registerable_config_raw.params, scope.model_dump())
        registerable_config_raw.params = rendered_params
        return self.__create_renderable_instance(registerable_config_raw, scope)

    def __create_service_instance(self, registerable_config_raw: RenderableConfig, scope: PipeContext) -> Renderable:
        return self.render(registerable_config_raw, scope)

    def __create_renderable_instance(self, rendered_config: RenderableConfig, scope: PipeContext) -> Renderable:
        cls: type = typing.cast("type", locate(rendered_config.use))
        if not issubclass(cls, Renderable):
            raise TypeError(f"Class '{rendered_config.use}' is not a {Renderable.__class__.__name__}")

        return cls(
            **{
                "factory": self,
                "app_config": self._app_config,
                "logger_factory": self._logger_factory,
                "config": rendered_config,
                **self.__resolve_injects(rendered_config.injects, scope),
            }
        )

    def __resolve_injects(self, injects: dict[str, str], scope: PipeContext) -> dict[str, Renderable]:
        return {param: self.__resolve_by_id(ref, scope) for param, ref in injects.items()}

    def __resolve_by_id(self, service_id: str, scope: PipeContext) -> Any:
        matching_config = next(
            (
                config
                for config in self._registerable_configs
                if RenderableConfig.model_validate(config).id == service_id
            ),
            None,
        )
        if matching_config is None:
            raise KeyError(service_id)
        return self.render(matching_config, scope)
