from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Type, TypeVar, Union

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter

T = TypeVar('T')
PipeType = TypeVar('PipeType', bound=Pipe)
ServiceType = TypeVar('ServiceType', bound=TicketSystemAdapter)


class UnifiedRegistry:
    """Unified registry for pipes, services, and other components from plugins."""
    
    _instance: Optional[UnifiedRegistry] = None
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._pipes: Dict[str, Type[Pipe]] = {}
        self._services: Dict[str, Type[TicketSystemAdapter]] = {}
        self._components: Dict[str, Type[Any]] = {}
    
    def __new__(cls) -> UnifiedRegistry:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> UnifiedRegistry:
        """Get the singleton instance of the registry."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def register_pipe(self, name: str, pipe_class: Type[Pipe]) -> None:
        """Register a pipe class with the given name."""
        if name in self._pipes:
            self.logger.warning(f"Pipe '{name}' is already registered, overwriting")
        self._pipes[name] = pipe_class
        self.logger.debug(f"Registered pipe: {name} -> {pipe_class.__name__}")
    
    def register_service(self, name: str, service_class: Type[TicketSystemAdapter]) -> None:
        """Register a service class with the given name."""
        if name in self._services:
            self.logger.warning(f"Service '{name}' is already registered, overwriting")
        self._services[name] = service_class
        self.logger.debug(f"Registered service: {name} -> {service_class.__name__}")
    
    def register_component(self, name: str, component_class: Type[Any]) -> None:
        """Register a generic component class with the given name."""
        if name in self._components:
            self.logger.warning(f"Component '{name}' is already registered, overwriting")
        self._components[name] = component_class
        self.logger.debug(f"Registered component: {name} -> {component_class.__name__}")
    
    def get_pipe(self, name: str) -> Optional[Type[Pipe]]:
        """Get a pipe class by name."""
        return self._pipes.get(name)
    
    def get_service(self, name: str) -> Optional[Type[TicketSystemAdapter]]:
        """Get a service class by name."""
        return self._services.get(name)
    
    def get_component(self, name: str) -> Optional[Type[Any]]:
        """Get a component class by name."""
        return self._components.get(name)
    
    def get_all_pipes(self) -> Dict[str, Type[Pipe]]:
        """Get all registered pipes."""
        return self._pipes.copy()
    
    def get_all_services(self) -> Dict[str, Type[TicketSystemAdapter]]:
        """Get all registered services."""
        return self._services.copy()
    
    def get_all_components(self) -> Dict[str, Type[Any]]:
        """Get all registered components."""
        return self._components.copy()
    
    def clear_all(self) -> None:
        """Clear all registrations (mainly for testing)."""
        self._pipes.clear()
        self._services.clear()
        self._components.clear()
        self.logger.debug("Cleared all registrations")
    
    def list_registered(self) -> Dict[str, Dict[str, str]]:
        """List all registered components by category."""
        return {
            "pipes": {name: cls.__name__ for name, cls in self._pipes.items()},
            "services": {name: cls.__name__ for name, cls in self._services.items()},
            "components": {name: cls.__name__ for name, cls in self._components.items()},
        }


# Convenience functions for registration
def register_pipe(name: str) -> callable:
    """Decorator to register a pipe class."""
    def decorator(pipe_class: Type[Pipe]) -> Type[Pipe]:
        UnifiedRegistry.get_instance().register_pipe(name, pipe_class)
        return pipe_class
    return decorator


def register_service(name: str) -> callable:
    """Decorator to register a service class."""
    def decorator(service_class: Type[TicketSystemAdapter]) -> Type[TicketSystemAdapter]:
        UnifiedRegistry.get_instance().register_service(name, service_class)
        return service_class
    return decorator


def register_component(name: str) -> callable:
    """Decorator to register a generic component class."""
    def decorator(component_class: Type[Any]) -> Type[Any]:
        UnifiedRegistry.get_instance().register_component(name, component_class)
        return component_class
    return decorator
