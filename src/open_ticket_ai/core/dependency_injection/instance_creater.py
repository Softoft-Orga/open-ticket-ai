
from pydoc import locate

from injector import inject

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry


class InstanceCreator:

    @inject
    def __init__(self, config: RawOpenTicketAIConfig, registry: UnifiedRegistry):
        self._config = config
        self._registry = registry

    def create_instances(self):
        for instance in self._config.defs:
            instance_type: type = locate(instance.get("use"))
            if instance_type:
                self._registry.register_instance(
                    instance_type(instance)
                )
