from typing import TYPE_CHECKING

from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig

if TYPE_CHECKING:
    from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry


class WrongConfigError(Exception):
    """Raised when the configuration provided is incorrect or invalid."""


class RegistryError(Exception):
    """Raised when there is an error related to the component registry."""

    def __init__(self, component_registry: ComponentRegistry, message: str = ""):
        super().__init__(f"{message}.Available injectables: {component_registry.get_available_injectables()}")


class NoServiceConfigurationFoundError(WrongConfigError):
    """Raised when no service configuration is found for a required service."""

    def __init__(self, service_id: str, service_configs: list[InjectableConfig]):
        available_services = [config.id for config in service_configs]
        super().__init__(
            f"No configuration found for required service with id '{service_id}'. "
            f"Available service configurations: {available_services}"
        )


class InjectableNotFoundError(RegistryError):
    def __init__(self, injectable_id: str, component_registry: ComponentRegistry):
        super().__init__(
            component_registry, f"Injectable with id '{injectable_id}' not found in the ComponentRegistry. "
        )


class MissingConfigurationForRequiredServiceError(WrongConfigError):
    """Raised when a required service configuration is missing."""

    def __init__(self, required_service_class: type[Injectable]):
        message = f"""
        Missing configuration for required service type: {required_service_class.__name__}.
        {required_service_class.__name__} is a required Service, which means there needs to be exactly one
        configured entry for it in the services list of the Config.
        """
        super().__init__(message)


class MultipleConfigurationsForSingletonServiceError(WrongConfigError):
    """Raised when multiple configurations are found for a singleton service."""

    def __init__(self, singleton_service_class: type[Injectable]):
        message = f"""
        Multiple configurations found for singleton service type: {singleton_service_class.__name__}.
        {singleton_service_class.__name__} is a singleton Service, which means there needs to be at most one
        configured entry for it in the services list of the Config.
        """
        super().__init__(message)
