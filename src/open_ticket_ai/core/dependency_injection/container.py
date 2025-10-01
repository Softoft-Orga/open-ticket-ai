import os

from injector import Binder, Module, singleton

from open_ticket_ai.core.config.config_models import (
    RawOpenTicketAIConfig,
    load_config,
)
from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory
from open_ticket_ai.core.util.path_util import find_python_code_root_path


class AppModule(Module):
    def __init__(self, config_path: str | os.PathLike | None = None):
        """Initialize AppModule with optional config path.
        
        Args:
            config_path: Path to config.yml. If None, uses OPEN_TICKET_AI_CONFIG
                        environment variable or falls back to default location.
        """
        if config_path is None:
            config_path = os.getenv(
                "OPEN_TICKET_AI_CONFIG",
                find_python_code_root_path() / "config.yml"
            )
        self.config_path = config_path

    def configure(self, binder: Binder):
        config = load_config(self.config_path)
        registry = UnifiedRegistry.get_registry_instance()
        binder.bind(RawOpenTicketAIConfig, to=config, scope=singleton)
        binder.bind(UnifiedRegistry, to=registry, scope=singleton)
        binder.bind(PipeFactory, scope=singleton)
