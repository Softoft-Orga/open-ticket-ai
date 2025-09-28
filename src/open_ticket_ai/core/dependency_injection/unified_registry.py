from __future__ import annotations

import inspect
from typing import Type, Self, Callable, Any, Dict, Iterable, Mapping

from open_ticket_ai.core.config.template_configured_class import TemplateConfiguredClass


class NotRegistered(Exception):
    pass


class ConflictingClassRegistration(Exception):
    pass


class UnifiedRegistry:
    """Holds registered TYPES and per-run service INSTANCES."""
    _singleton: Self | None = None

    def __init__(self) -> None:
        self.class_registry: dict[str, type[TemplateConfiguredClass]] = {}
        self.service_instances: dict[str, Any] = {}

    @classmethod
    def instance(cls) -> Self:
        if cls._singleton is None:
            cls._singleton = UnifiedRegistry()
        return cls._singleton

    @classmethod
    def register(cls, _cls: type[TemplateConfiguredClass]) -> type[TemplateConfiguredClass]:
        instance = cls.instance()
        class_name = _cls.__name__
        if class_name in instance.class_registry:
            raise ConflictingClassRegistration(f"Class '{class_name}' is already registered.")
        instance.class_registry[class_name] = _cls
        return _cls

    def get_class(self, name: str) -> type[TemplateConfiguredClass]:
        try:
            return self.class_registry[name]
        except KeyError:
            raise NotRegistered(f"Class '{name}' not found. Available: {list(self.class_registry)}")


    def get_service_instance(self, service_id: str) -> Any:
        try:
            return self.service_instances[service_id]
        except KeyError:
            raise NotRegistered(f"Service instance '{service_id}' not found. Available: {list(self.service_instances)}")

    def instantiate_services_from_config(
            self,
            services_spec: Iterable[dict[str, Any]],
            render_scope: dict[str, Any],
    ) -> None:
        for item in services_spec or []:
            service_id: str = str(item["id"])
            service_type_name: str = str(item["use"])

            service_class = self.get_class(service_type_name)

            config_instance = self._create_config_instance(service_class, item, render_scope)

            try:
                instance = service_class(config=config_instance)
            except TypeError:
                instance = service_class(**item)

            self.add_service_instance(service_id, instance)

    def build_pipe_instance(
            self,
            pipe_type_name: str,
            raw_step_config: dict[str, Any],
            service_bindings: dict[str, str] | None = None,
            extra_kwargs: dict[str, Any] | None = None,
    ):
        pipe_class = self.get_registered_pipe_class(pipe_type_name)
        self._validate_pipe_constructor_accepts_services(pipe_class, service_bindings)

        config_instance = self._create_config_instance(pipe_class, raw_step_config, {})

        injected_kwargs: Dict[str, Any] = {}
        for constructor_param, service_id in (service_bindings or {}).items():
            injected_kwargs[constructor_param] = self.get_service_instance(service_id)

        if extra_kwargs:
            injected_kwargs.update(extra_kwargs)

        return pipe_class(config=config_instance, **injected_kwargs)

    def _create_config_instance(
            self,
            configurable_class: type[TemplateConfiguredClass],
            raw_config: dict[str, Any],
            render_scope: dict[str, Any]
    ) -> Any:
        if configurable_class.needs_raw_config():
            config_model_type = configurable_class.get_raw_config_model_type()
            return config_model_type(**raw_config)
        else:
            rendered_config_type = configurable_class.get_rendered_config_model_type()
            if rendered_config_type is None:
                raise ValueError(f"Class {configurable_class.__name__} needs rendered config but doesn't specify type")

            rendered_config = self._render_recursive(raw_config, render_scope)
            return rendered_config_type(**rendered_config)
