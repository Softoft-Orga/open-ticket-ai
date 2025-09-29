# FILE_PATH: open_ticket_ai/src/core/dependency_injection/container.py
import importlib
import os

from injector import Binder, Module, provider, singleton

from open_ticket_ai.core.config.config_models import (
    OpenTicketAIConfig,
    load_config,
)
from open_ticket_ai.core.dependency_injection.unified_registry import (
    NotRegistered,
    UnifiedRegistry,
)
from open_ticket_ai.core.orchestrator import Orchestrator
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemService
from open_ticket_ai.core.util.path_util import find_python_code_root_path

CONFIG_PATH = os.getenv("OPEN_TICKET_AI_CONFIG", find_python_code_root_path() / "config.yml")


class AppModule(Module):
    def configure(self, binder: Binder):
        config = load_config(CONFIG_PATH)
        binder.bind(OpenTicketAIConfig, to=config, scope=singleton)
        binder.bind(UnifiedRegistry, to=UnifiedRegistry.get_instance(), scope=singleton)
    # --- Orchestrator Provider ---
    @provider
    @singleton
    def provide_orchestrator(
            self,
            config: OpenTicketAIConfig,
            registry: UnifiedRegistry,
    ) -> Orchestrator:
        """Provide the orchestrator with configured pipes."""
        return Orchestrator(runners=config.orchestrator, registry=registry)

    @provider
    @singleton
    def provide_ticket_system_adapter(
            self,
            config: OpenTicketAIConfig,
            registry: UnifiedRegistry,
    ) -> TicketSystemService:
        """Provide the ticket system adapter from registry."""
        # Get the ticket system adapter from registry
        try:
            adapter_class = registry.get_class(config.system.type)
        except NotRegistered:
            # Fall back to dynamic import if not in registry
            module_name, class_name = config.system.type.rsplit(".", 1)
            module = importlib.import_module(module_name)
            adapter_class = getattr(module, class_name)
            # Register it for future use
            registry.register_class(adapter_class)
            registry.register_class(adapter_class, name=config.system.type)

        # Create instance with configuration
        ticket_system = adapter_class(config=config.system.config)
        registry.set_instance(config.system.type, ticket_system)
        return ticket_system
