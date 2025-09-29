# FILE_PATH: open_ticket_ai/src/core/dependency_injection/container.py
import importlib
import os

from injector import Binder, Module, provider, singleton

from open_ticket_ai.core.config.config_models import (
    OpenTicketAIConfig,
    load_config,
)
from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.orchestrator import Orchestrator
from open_ticket_ai.core.pipeline.base_pipe import BasePipe
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
            pipes: list[BasePipe],
    ) -> Orchestrator:
        """Provide the orchestrator with configured pipes."""
        # Get interval from pipeline configuration if available
        interval_seconds = 60.0  # default
        if config.pipelines and config.pipelines[0].pipeline_config:
            interval_seconds = config.pipelines[0].pipeline_config.get("interval_seconds", 60.0)

        # Create orchestrator with injected pipes
        return Orchestrator(pipes=pipes, interval_seconds=interval_seconds)

    @provider
    @singleton
    def provide_ticket_system_adapter(
            self,
            config: OpenTicketAIConfig,
            registry: UnifiedRegistry,
    ) -> TicketSystemService:
        """Provide the ticket system adapter from registry."""
        # Get the ticket system adapter from registry
        adapter_class = registry.get_service(config.system.type)

        if not adapter_class:
            # Fall back to dynamic import if not in registry
            module_name, class_name = config.system.type.rsplit(".", 1)
            module = importlib.import_module(module_name)
            adapter_class = getattr(module, class_name)
            # Register it for future use
            registry.register_service(config.system.type, adapter_class)

        # Create instance with configuration
        ticket_system = adapter_class(config=config.system.config)
        return ticket_system
