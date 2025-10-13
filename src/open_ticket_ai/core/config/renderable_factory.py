from __future__ import annotations

import inspect
import typing
from pydoc import locate
from typing import Any, get_type_hints

from injector import Injector, inject, singleton
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


def render_base_model[T: BaseModel](config: T, scope: PipeContext, renderer: TemplateRenderer) -> T | dict[str, Any]:
    if type(config) is BaseModel:
        return config
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
        injector: Injector,
    ):
        self._logger = logger_factory.get_logger(self.__class__.__name__)
        self._template_renderer = template_renderer
        self._registerable_configs = registerable_configs
        self._app_config = app_config
        self._logger_factory = logger_factory
        self._injector = injector

    def create_pipe(self, pipe_config_raw: PipeConfig[BaseModel], scope: PipeContext) -> Pipe[Any]:
        self._logger.debug(f"Creating pipe with config id: {pipe_config_raw.id}")
        self._logger.info(f"Creating pipe '{pipe_config_raw.id}'")
        rendered_params = render_base_model(pipe_config_raw.params, scope, self._template_renderer)
        pipe_config_raw.params = rendered_params
        registerable = self.__create_renderable_instance(pipe_config_raw, scope)
        if not isinstance(registerable, Pipe):
            raise TypeError(f"Registerable with id '{pipe_config_raw.id}' is not a Pipe")
        return registerable

    def create_trigger(self, trigger_config_raw: RenderableConfig[BaseModel], scope: PipeContext) -> Renderable:
        self._logger.debug(f"Creating trigger with config id: {trigger_config_raw.id}")
        self._logger.info(f"Creating trigger '{trigger_config_raw.id}'")
        rendered_params = render_base_model(trigger_config_raw.params, scope, self._template_renderer)
        trigger_config_raw.params = rendered_params
        return self.__create_renderable_instance(trigger_config_raw, scope)

    def __create_service_instance(
        self, registerable_config_raw: RenderableConfig[BaseModel], scope: PipeContext
    ) -> Renderable:
        rendered_config = render_base_model(registerable_config_raw, scope, self._template_renderer)
        if not isinstance(rendered_config, RenderableConfig):
            raise TypeError("Rendered config must be a RenderableConfig instance")
        return self.__create_renderable_instance(rendered_config, scope)

    def __create_renderable_instance(
        self, registerable_config: RenderableConfig[BaseModel], scope: PipeContext
    ) -> Renderable:
        cls: type = _locate(registerable_config.use)
        if not issubclass(cls, Renderable):
            raise TypeError(f"Class '{registerable_config.use}' is not a Registerable")

        resolved_injects = self.__resolve_injects(registerable_config.injects, scope)
        
        if resolved_injects:
            child_injector = self.__create_child_injector_with_explicit_bindings(cls, resolved_injects)
            return self.__instantiate_with_injector(cls, registerable_config, child_injector)
        else:
            return self.__instantiate_with_injector(cls, registerable_config, self._injector)

    def __create_child_injector_with_explicit_bindings(
        self, cls: type, explicit_deps: dict[str, Any]
    ) -> Injector:
        try:
            type_hints = get_type_hints(cls.__init__)
        except Exception:
            type_hints = {}
        
        def configure_explicit_bindings(binder: Any) -> None:
            for param_name, instance in explicit_deps.items():
                if param_name in type_hints:
                    param_type = type_hints[param_name]
                    binder.bind(param_type, to=instance)
        
        return self._injector.create_child_injector([configure_explicit_bindings])

    def __instantiate_with_injector(
        self, cls: type, registerable_config: RenderableConfig[BaseModel], inj: Injector
    ) -> Renderable:
        sig = inspect.signature(cls.__init__)
        try:
            type_hints = get_type_hints(cls.__init__)
        except Exception:
            type_hints = {}
        
        kwargs: dict[str, Any] = {}
        first_config_param: str | None = None
        has_var_kwargs = False
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                has_var_kwargs = True
            
            param_type = type_hints.get(param_name, param.annotation)
            if param_type != inspect.Parameter.empty and param_type not in (str, int, float, bool, dict, list):
                try:
                    kwargs[param_name] = inj.get(param_type)
                except Exception:
                    pass
            
            if param_name in ('config', 'trigger_config') and first_config_param is None:
                first_config_param = param_name
        
        if 'params' in sig.parameters:
            kwargs["params"] = registerable_config.params
        if 'factory' in sig.parameters or has_var_kwargs:
            kwargs["factory"] = self
        if 'app_config' in sig.parameters or has_var_kwargs:
            kwargs["app_config"] = self._app_config
        if 'logger_factory' in sig.parameters or has_var_kwargs:
            kwargs["logger_factory"] = self._logger_factory
        if 'pipe_config' in sig.parameters or has_var_kwargs:
            kwargs["pipe_config"] = registerable_config
        if first_config_param and first_config_param not in kwargs:
            kwargs[first_config_param] = registerable_config
        
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
