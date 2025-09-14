from inspect import cleandoc

from injector import inject

from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.core.dependency_injection.registry import Registry


class OpenTicketAIConfigValidator:
    @inject
    def __init__(self, config: OpenTicketAIConfig, registry: Registry):
        self.config = config
        self.registry = registry

    def validate_registry(self) -> None:
        configs = self.config.get_all_register_instance_configs()
        for config in configs:
            if not self.registry.contains(config.provider_key):
                raise ValueError(
                    cleandoc(
                        f"""
                        Registry does not contain required provider with key
                        '{config.provider_key}' for config '{config.id}'
                        Registered providers:
                        {self.registry.get_registry_types_descriptions()}
                        """
                    )
                )
