from __future__ import annotations

import inspect
from typing import Any, Dict, Iterable, Mapping

from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry


def render_service_config(raw_config: Any, render_scope: Mapping[str, Any], deep_renderer) -> Any:
    return deep_renderer(raw_config, render_scope)  # no mutation


def instantiate_services_from_config(
        *,
        registry: UnifiedRegistry,
        services_spec: Iterable[Mapping[str, Any]],
        render_scope: Mapping[str, Any],
        deep_renderer,
) -> None:
    registry.clear_service_instances()

    for item in services_spec or []:
        service_id: str = str(item["id"])
        service_type_name: str = str(item["use"])
        raw_config: Dict[str, Any] = dict(item.get("config") or {})

        service_class = registry.get_registered_service_class(service_type_name)
        rendered_config = render_service_config(raw_config, render_scope, deep_renderer)

        # Support ctor(config=...) and ctor(**kwargs)
        try:
            instance = service_class(config=rendered_config)
        except TypeError:
            instance = service_class(**rendered_config)

        registry.add_service_instance(service_id, instance)


def validate_pipe_constructor_accepts_services(pipe_class: type, service_bindings: Mapping[str, str]) -> None:
    constructor_signature = inspect.signature(pipe_class.__init__)
    unknown_params = [param_name for param_name in service_bindings.keys() if
                      param_name not in constructor_signature.parameters]
    if unknown_params:
        raise TypeError(
            f"{pipe_class.__name__}.__init__ does not accept service params: {unknown_params}. "
            f"Accepted params: {list(constructor_signature.parameters)}"
        )


def build_pipe_instance(
        *,
        registry: UnifiedRegistry,
        pipe_type_name: str,
        raw_step_config: Any,
        service_bindings: Mapping[str, str],
        extra_kwargs: Dict[str, Any] | None = None,
):
    pipe_class = registry.get_registered_pipe_class(pipe_type_name)
    validate_pipe_constructor_accepts_services(pipe_class, service_bindings)

    injected_kwargs: Dict[str, Any] = {}
    for constructor_param, service_id in (service_bindings or {}).items():
        injected_kwargs[constructor_param] = registry.get_service_instance(service_id)

    if extra_kwargs:
        injected_kwargs.update(extra_kwargs)

    return pipe_class(config=raw_step_config, **injected_kwargs)


def build_pipe_sequence_for_flow(
        *,
        registry: UnifiedRegistry,
        flow_steps: Iterable[Mapping[str, Any]],
) -> list:
    pipe_instances = []
    for step_spec in flow_steps:
        pipe_type_name = str(step_spec["use"])  # required
        raw_step_config = step_spec.get("config")
        service_bindings: Dict[str, str] = dict(step_spec.get("services") or {})
        pipe_instances.append(
            build_pipe_instance(
                registry=registry,
                pipe_type_name=pipe_type_name,
                raw_step_config=raw_step_config,
                service_bindings=service_bindings,
            )
        )
    return pipe_instances
