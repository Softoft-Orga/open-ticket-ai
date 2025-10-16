from __future__ import annotations

import typing
from pydoc import locate
from typing import Any

from injector import inject, singleton

from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.trigger import Trigger
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_context_model import PipeContext
from open_ticket_ai.core.pipeline.pipe_models import PipeConfig
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

    def render_pipe(self, pipe_config: PipeConfig, pipe_context: PipeContext) -> Pipe[Any]:
        renderable: Renderable[Any] = self._render(pipe_config, pipe_context.model_dump())
        if not isinstance(renderable, Pipe):
            raise TypeError(f"Renderable with id '{pipe_config.id}' is not a {Pipe.__class__.__name__}")
        return renderable

    def render_trigger(self, trigger_config: RenderableConfig, scope: dict[str, Any]) -> Trigger[Any]:
        renderable: Renderable[Any] = self._render(trigger_config, scope)
        if not isinstance(renderable, Trigger):
            raise TypeError(f"Renderable with id '{trigger_config.id}' is not a {Trigger.__class__.__name__}")
        return renderable

    def _render(self, registerable_config_raw: RenderableConfig, scope: dict[str, Any]) -> Renderable[Any]:
        rendered_params = self._template_renderer.render(registerable_config_raw.params, scope)
        registerable_config_raw.params = rendered_params
        return self.__create_renderable_instance(registerable_config_raw, scope)

    def __create_renderable_instance(self, rendered_config: RenderableConfig, scope: dict[str, Any]) -> Renderable:
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
            }  # type: ignore[arg-type]
        )

    def __resolve_injects(self, injects: dict[str, str], scope: dict[str, Any]) -> dict[str, Renderable]:
        return {param: self.__resolve_by_id(ref, scope) for param, ref in injects.items()}

    def __resolve_by_id(self, service_id: str, scope: dict[str, Any]) -> Any:
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
        return self._render(matching_config, scope)
