from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Type, Self


class NotRegistered(Exception):
    pass


class ServiceNotRegistered(NotRegistered):
    pass


class PipeNotRegistered(NotRegistered):
    pass


class ConflictingClassRegistration(Exception):
    pass

class ConflictingInstanceRegistration(Exception):
    pass


class UnifiedRegistry:
    """Holds registered TYPES and per-run service INSTANCES."""
    _singleton: Self | None = None

    def __init__(self) -> None:
        self.class_registry: dict[str, type] = {}
        self.instances: Dict[str, Any] = {}

    @classmethod
    def instance(cls) -> Self:
        if cls._singleton is None:
            cls._singleton = UnifiedRegistry()
        return cls._singleton

    def register(self, name: str, pipe_class: Type) -> None:
        def _register(_cls: type):
            self.class_registry[_cls.__class__.__name__] = _cls

        self.pipe_types[name] = PipeDescriptor(pipe_class)

    def register(self, name: str, service_class: Type) -> None:
        self.service_types[name] = ServiceDescriptor(service_class)

    # ---- TYPE lookup (no dotted-path fallback) ----
    def get_registered_pipe_class(self, name: str) -> Type:
        meta = self.pipe_types.get(name)
        if meta is None:
            raise PipeNotRegistered(f"Unknown pipe '{name}'. Registered pipes: {list(self.pipe_types)}")
        return meta.cls

    def get_registered_service_class(self, name: str) -> Type:
        meta = self.service_types.get(name)
        if meta is None:
            raise ServiceNotRegistered(
                f"Unknown service type '{name}'. Registered service types: {list(self.service_types)}"
            )
        return meta.cls

    # ---- INSTANCE management (built from config.yml) ----
    def clear_service_instances(self) -> None:
        self.service_instances.clear()

    def add_service_instance(self, service_id: str, instance: Any) -> None:
        self.service_instances[service_id] = instance

    def get_service_instance(self, service_id: str) -> Any:
        try:
            return self.service_instances[service_id]
        except KeyError:
            raise KeyError(f"Service instance '{service_id}' not found. Available: {list(self.service_instances)}")
