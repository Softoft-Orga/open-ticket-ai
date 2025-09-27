# FILE_PATH: open_ticket_ai/src/core/dependency_injection/container.py
import importlib
import os

from injector import Binder, Module, provider, singleton

from open_ticket_ai.core.config.config_models import (
    OpenTicketAIConfig,
    load_config,
)
from open_ticket_ai.core.dependency_injection.registry import TicketSystemRegistry
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipeline import Pipeline
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.core.util.path_util import find_python_code_root_path

CONFIG_PATH = os.getenv("OPEN_TICKET_AI_CONFIG", find_python_code_root_path() / "config.yml")


class AppModule(Module):
    def configure(self, binder: Binder):
        config = load_config(CONFIG_PATH)
        binder.bind(OpenTicketAIConfig, to=config, scope=singleton)



    def _import_pipe_class(self, class_path: str):
        module_name, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    # --- Pipeline and Orchestrator ---
    @provider
    @singleton
    def provide_pipeline(
            self,
            config: OpenTicketAIConfig,
            ticket_system_adapter: TicketSystemAdapter,
    ) -> Pipeline:
        pipes = []

        for pipe_config in config.pipelines[0].steps:
            pipe_class: type[Pipe] = self._import_pipe_class(pipe_config.type)

            # Get the ConfigT from the Pipe class
            pipe_instance = pipe_class(config=pipe_config, ticket_system=ticket_system_adapter)

            pipes.append(pipe_instance)

        return Pipeline(pipes=pipes, config=config.pipelines[0].pipeline_config)

    @provider
    @singleton
    def provide_ticket_system_adapter(
            self,
            config: OpenTicketAIConfig,
    ) -> TicketSystemAdapter:
        ticket_system = TicketSystemRegistry.create(
            system_type=config.system.type,
            config=config.system.config
        )
        return ticket_system
