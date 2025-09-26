from __future__ import annotations

from typing import Dict, Type, Optional, Any

from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter


class TicketSystemRegistry[T:TicketSystemAdapter]:
    _instance: Optional[TicketSystemRegistry] = None
    _registry: Dict[str, Type[T]] = {}

    def __new__(cls) -> TicketSystemRegistry:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, system_type: str) -> callable:

        def decorator(adapter_class: Type[T]) -> Type[T]:
            if system_type in cls._registry:
                raise ValueError(f"Ticket system '{system_type}' is already registered")
            cls._registry[system_type] = adapter_class
            return adapter_class

        return decorator

    @classmethod
    def create(cls, system_type: str, **kwargs: Any) -> T:
        if system_type not in cls._registry:
            raise ValueError(
                f"Unknown ticket system type: {system_type}. "
                f"Available types: {list(cls._registry.keys())}"
            )
        return cls._registry[system_type](**kwargs)

    @classmethod
    def get_available_systems(cls) -> Dict[str, Type[T]]:
        """Get a dictionary of all registered ticket system types and their adapter classes."""
        return cls._registry.copy()

    @classmethod
    def clear_registry(cls) -> None:
        """Clear all registered adapters (mainly for testing)."""
        cls._registry.clear()
