from __future__ import annotations

from typing import Any, Callable, TypeVar


class NotRegistered(Exception):
    """Raised when attempting to access a class or instance that was not registered."""


T = TypeVar("T")

class UnifiedRegistry:
    """A very small registry to track classes and their instances."""

    _singleton: "UnifiedRegistry | None" = None

    def __init__(self) -> None:
        self._classes: dict[str, type[Any]] = {}
        self._instances: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Singleton helpers
    # ------------------------------------------------------------------
    @classmethod
    def get_instance(cls) -> "UnifiedRegistry":
        if cls._singleton is None:
            cls._singleton = cls()
        return cls._singleton

    # Keep backwards compatibility with previous API that exposed ``instance``
    instance = get_instance

    # ------------------------------------------------------------------
    # Class registration
    # ------------------------------------------------------------------
    @classmethod
    def register(
        cls,
        target: type[Any] | None = None,
        *,
        name: str | None = None,
    ) -> Callable[[type[T]], type[T]] | type[Any]:
        """Register a class either directly or via decorator usage.

        This supports both ``@UnifiedRegistry.register`` and
        ``@UnifiedRegistry.register(name="Alias")`` forms.
        """

        registry = cls.get_instance()

        def decorator(obj: type[T]) -> type[T]:
            registry.register_class(obj, name=name)
            return obj

        if target is None:
            return decorator

        return decorator(target)

    def register_class(self, obj: type[Any], name: str | None = None) -> None:
        key = name or obj.__name__
        self._classes[key] = obj
        # Always allow lookups via the fully-qualified name as well
        fq_name = f"{obj.__module__}.{obj.__name__}"
        self._classes.setdefault(fq_name, obj)

    # ------------------------------------------------------------------
    # Class retrieval / instantiation
    # ------------------------------------------------------------------
    def get_class(self, name: str) -> type[Any]:
        try:
            return self._classes[name]
        except KeyError:
            short_name = name.rsplit(".", 1)[-1]
            try:
                return self._classes[short_name]
            except KeyError as exc:
                raise NotRegistered(f"Class '{name}' is not registered.") from exc

    def create_instance(self, name: str, *args: Any, **kwargs: Any) -> Any:
        cls = self.get_class(name)
        return cls(*args, **kwargs)

    # ------------------------------------------------------------------
    # Instance storage helpers
    # ------------------------------------------------------------------
    def set_instance(self, instance_id: str, instance: Any) -> None:
        self._instances[instance_id] = instance

    def get_instance_by_id(self, instance_id: str) -> Any:
        try:
            return self._instances[instance_id]
        except KeyError as exc:
            raise NotRegistered(f"Instance '{instance_id}' is not registered.") from exc

    # Convenience aliases for older naming used across the project
    add_service_instance = set_instance
    get_service_instance = get_instance_by_id
