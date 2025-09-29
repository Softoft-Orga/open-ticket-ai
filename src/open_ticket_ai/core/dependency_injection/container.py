# FILE_PATH: open_ticket_ai/src/core/dependency_injection/container.py
import os

from injector import Binder, Module, singleton

from open_ticket_ai.core.config.config_models import (
    RawOpenTicketAIConfig,
    load_config,
)
from open_ticket_ai.core.dependency_injection.instance_creater import InstanceCreator
from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.util.path_util import find_python_code_root_path

CONFIG_PATH = os.getenv("OPEN_TICKET_AI_CONFIG", find_python_code_root_path() / "config.yml")


class AppModule(Module):
    def configure(self, binder: Binder):
        config = load_config(CONFIG_PATH)
        registry = UnifiedRegistry.get_registry_instance()
        binder.bind(RawOpenTicketAIConfig, to=config, scope=singleton)
        binder.bind(UnifiedRegistry, to=registry, scope=singleton)
        binder.bind(InstanceCreator, to=InstanceCreator(config, registry), scope=singleton)
