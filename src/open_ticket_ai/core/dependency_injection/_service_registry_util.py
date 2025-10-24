from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig


def find_all_configured_services_of_type(
    services_configs: list[InjectableConfig], component_registry: ComponentRegistry, subclass_of: type[Injectable]
) -> list[InjectableConfig]:
    found_services: list[InjectableConfig] = []
    for service_config in services_configs:
        registry_identifier = service_config.use
        service: type[Injectable] = component_registry.get_injectable(by_identifier=registry_identifier)
        if issubclass(service, subclass_of):
            found_services.append(service_config)
    return found_services
