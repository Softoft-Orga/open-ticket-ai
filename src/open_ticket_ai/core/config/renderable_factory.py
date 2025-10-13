from __future__ import annotations

import typing
from pydoc import locate
from typing import Any

from injector import inject, singleton

from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.renderable import Renderable, RenderableConfig
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import ParamsModel, Pipe
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


def render_params(params: ParamsModel, scope: PipeContext, renderer: TemplateRenderer) -> dict[str, Any]:
    if isinstance(params, dict):
        return params

    try:
        params_dict = params.model_dump()
    except Exception:
        params_dict = {}
        if hasattr(params, "__dict__"):
            for key, value in params.__dict__.items():
                if not key.startswith("_"):
                    params_dict[key] = value

    return renderer.render_recursive(params_dict, scope)


@singleton
class RenderableFactory:
    @inject
    def __init__(
        self,
        template_renderer: TemplateRenderer,
        app_config: AppConfig,
        registerable_configs: list[RenderableConfig[ParamsModel]],
        logger_factory: LoggerFactory,
    ):
        self._logger = logger_factory.get_logger(self.__class__.__name__)
        self._template_renderer = template_renderer
        self._registerable_configs = registerable_configs
        self._app_config = app_config
        self._logger_factory = logger_factory

    def create_pipe(self, pipe_config_raw: PipeConfig[ParamsModel], scope: PipeContext) -> Pipe[Any]:
        self._logger.debug(f"Creating pipe with config id: {pipe_config_raw.id}")
        self._logger.info(f"Creating pipe '{pipe_config_raw.id}'")
        rendered_params = render_params(pipe_config_raw.params, scope, self._template_renderer)
        pipe_config_raw.params = rendered_params
        registerable = self.__create_renderable_instance(pipe_config_raw, scope)
        if not isinstance(registerable, Pipe):
            raise TypeError(f"Registerable with id '{pipe_config_raw.id}' is not a Pipe")
        return registerable

    def create_trigger(self, trigger_config_raw: RenderableConfig[ParamsModel], scope: PipeContext) -> Renderable:
        self._logger.debug(f"Creating trigger with config id: {trigger_config_raw.id}")
        self._logger.info(f"Creating trigger '{trigger_config_raw.id}'")
        rendered_params = render_params(trigger_config_raw.params, scope, self._template_renderer)
        trigger_config_raw.params = rendered_params
        return self.__create_renderable_instance(trigger_config_raw, scope)

    def __create_service_instance(
        self, registerable_config_raw: RenderableConfig[ParamsModel], scope: PipeContext
    ) -> Renderable:
        rendered_params = render_params(registerable_config_raw.params, scope, self._template_renderer)
        registerable_config_raw.params = rendered_params
        return self.__create_renderable_instance(registerable_config_raw, scope)

    def __create_renderable_instance(
        self, registerable_config: RenderableConfig[ParamsModel], scope: PipeContext
    ) -> Renderable:
        cls: type = _locate(registerable_config.use)
        if not issubclass(cls, Renderable):
            raise TypeError(f"Class '{registerable_config.use}' is not a {Renderable.__class__.__name__}")

        kwargs: dict[str, Any] = {}
        kwargs |= self.__resolve_injects(registerable_config.injects, scope)
        kwargs["factory"] = self
        kwargs["app_config"] = self._app_config
        kwargs["logger_factory"] = self._logger_factory
        kwargs["config"] = registerable_config
        kwargs["pipe_config"] = registerable_config
        kwargs["config"] = registerable_config
        return cls(**kwargs)

    def __resolve_injects(self, injects: dict[str, str], scope: PipeContext) -> dict[str, Renderable]:
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
