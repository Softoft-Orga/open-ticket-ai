from __future__ import annotations

from typing import Any, Self


class NotRegistered(Exception):
    pass


class ConflictingClassRegistration(Exception):
    pass


class UnifiedRegistry:
    _singleton: Self | None = None

    def __init__(self) -> None:
        self.instances_registry: dict[str, Any] = {}

    @classmethod
    def get_registry_instance(cls) -> Self:
        if cls._singleton is None:
            cls._singleton = UnifiedRegistry()
        return cls._singleton

    def register_instance(self, instance: Any) -> Any:
        instance_id = instance.__class__.__name__
        if instance_id in self.instances_registry:
            raise ConflictingClassRegistration(f"Instance '{instance_id}' is already registered.")
        self.instances_registry[instance_id] = instance
        return instance

    def get_instance(self, instance_id: str) -> Any:
        try:
            return self.instances_registry[instance_id]
        except KeyError:
            raise NotRegistered(
                f"Service instance '{instance_id}' not found. Available: {list(self.instances_registry)}"
            )