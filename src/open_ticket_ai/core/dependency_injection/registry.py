from __future__ import annotations

from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar

from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.core.pipeline.pipe import Pipe


T = TypeVar("T")


class Registry(Generic[T]):
    """Generic registry that maps string identifiers to implementation classes."""

    _instance: Optional["Registry[T]"] = None
    _registry: Dict[str, T] = {}

    def __new__(cls) -> "Registry[T]":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, identifier: str) -> Callable[[T], T]:
        """Decorator used to register an implementation in the registry."""

        def decorator(implementation: T) -> T:
            if identifier in cls._registry:
                raise ValueError(f"'{identifier}' is already registered")
            cls._registry[identifier] = implementation
            return implementation

        return decorator

    @classmethod
    def get(cls, identifier: str) -> T:
        if identifier not in cls._registry:
            raise ValueError(
                f"Unknown identifier: {identifier}. Available: {list(cls._registry.keys())}"
            )
        return cls._registry[identifier]

    @classmethod
    def get_available(cls) -> Dict[str, T]:
        """Get a dictionary of all registered identifiers and their implementations."""
        return cls._registry.copy()

    @classmethod
    def clear_registry(cls) -> None:
        """Clear all registered adapters (mainly for testing)."""
        cls._registry.clear()


AdapterType = TypeVar("AdapterType", bound=TicketSystemAdapter)


class TicketSystemRegistry(Registry[Type[AdapterType]]):
    _instance: Optional["TicketSystemRegistry[AdapterType]"] = None
    _registry: Dict[str, Type[AdapterType]] = {}

    @classmethod
    def create(cls, system_type: str, **kwargs: Any) -> AdapterType:
        adapter_class = cls.get(system_type)
        return adapter_class(**kwargs)

    @classmethod
    def get_available_systems(cls) -> Dict[str, Type[AdapterType]]:
        return cls.get_available()


PipeType = TypeVar("PipeType", bound=Pipe)


class PipeRegistry(Registry[Type[PipeType]]):
    _instance: Optional["PipeRegistry[PipeType]"] = None
    _registry: Dict[str, Type[PipeType]] = {}

    @classmethod
    def get_available_pipes(cls) -> Dict[str, Type[PipeType]]:
        return cls.get_available()
