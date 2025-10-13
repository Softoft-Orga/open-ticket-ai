from __future__ import annotations

import typing
from pydoc import locate
from typing import Any

from injector import inject, singleton
from pydantic import BaseModel

from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.renderable import EmptyParams, Renderable, RenderableConfig
from open_ticket_ai.core.logging_iface import LoggerFactory
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


def render_base_model[T: BaseModel](
    config: T | dict[str, Any], scope: PipeContext, renderer: TemplateRenderer
) -> T | dict[str, Any]:
    if isinstance(config, dict):
        return renderer.render_recursive(config, scope)  # type: ignore[no-any-return]
    rendered_dict = renderer.render_recursive(config.model_dump(), scope)
    return type(config)(**rendered_dict)


@singleton
class RenderableFactory:
    @inject
    def __init__(
        self,
        template_renderer: TemplateRenderer,
        app_config: AppConfig,
        registerable_configs: list[RenderableConfig[EmptyParams]],
        logger_factory: LoggerFactory,
    ):
        self._logger = logger_factory.get_logger(self.__class__.__name__)
        self._template_renderer = template_renderer
        self._registerable_configs = registerable_configs
        self._app_config = app_config
        self._logger_factory = logger_factory

    def create_pipe(self, pipe_config_raw: PipeConfig[Any], scope: PipeContext) -> Pipe[Any]:
        self._logger.debug(f"Creating pipe with config id: {pipe_config_raw.id}")
        self._logger.info(f"Creating pipe '{pipe_config_raw.id}'")
        rendered_params = render_base_model(pipe_config_raw.params, scope, self._template_renderer)
        pipe_config_raw.params = rendered_params
        registerable = self.__create_renderable_instance(pipe_config_raw, scope)
        if not isinstance(registerable, Pipe):
            raise TypeError(f"Registerable with id '{pipe_config_raw.id}' is not a Pipe")
        return registerable

    def create_trigger(self, trigger_config_raw: RenderableConfig[Any], scope: PipeContext) -> Renderable:
        """Create a trigger instance with rendered config and dependency injection."""
        self._logger.debug(f"Creating trigger with config id: {trigger_config_raw.id}")
        self._logger.info(f"Creating trigger '{trigger_config_raw.id}'")
        # Render only the params like create_pipe does
        rendered_params = render_base_model(trigger_config_raw.params, scope, self._template_renderer)
        trigger_config_raw.params = rendered_params
        return self.__create_renderable_instance(trigger_config_raw, scope)

    def __create_service_instance(
        self, registerable_config_raw: RenderableConfig[Any], scope: PipeContext
    ) -> Renderable:
        rendered_config = render_base_model(registerable_config_raw, scope, self._template_renderer)
        if not isinstance(rendered_config, RenderableConfig):
            raise TypeError("Rendered config must be a RenderableConfig instance")
        return self.__create_renderable_instance(rendered_config, scope)

    def __create_renderable_instance(
        self, registerable_config: RenderableConfig[Any], scope: PipeContext
    ) -> Renderable:
        cls: type = _locate(registerable_config.use)
        if not issubclass(cls, Renderable):
            raise TypeError(f"Class '{registerable_config.use}' is not a Registerable")
        kwargs: dict[str, Any] = {}
        kwargs |= self.__resolve_injects(registerable_config.injects, scope)
        
        # Pass config with the appropriate parameter name based on the class type
        from open_ticket_ai.core.orchestration.trigger import Trigger
        from open_ticket_ai.core.pipeline.pipe import Pipe
        
        if issubclass(cls, Trigger):
            kwargs["config"] = registerable_config
        elif issubclass(cls, Pipe):
            kwargs["pipe_params"] = registerable_config
        else:
            # For other Renderable types, use pipe_config as default
            kwargs["pipe_config"] = registerable_config
            
        kwargs["factory"] = self
        kwargs["app_config"] = self._app_config
        kwargs["logger_factory"] = self._logger_factory
        return cls(**kwargs)

    def __resolve_injects(self, injects: dict[str, Any], scope: PipeContext) -> dict[str, Renderable]:
        out: dict[str, Any] = {}
        for param, ref in injects.items():
            out[param] = self.__resolve_by_id(ref, scope)
        return out

    def __resolve_by_id(self, service_id: str, scope: PipeContext) -> Any:
        for definition_config_raw in self._registerable_configs:
            definition_config: RenderableConfig[Any] = RenderableConfig.model_validate(definition_config_raw)
            if definition_config.id != service_id:
                continue
            return self.__create_service_instance(definition_config_raw, scope)
        raise KeyError(service_id)
