# FILE_PATH: open_ticket_ai/src/core/dependency_injection/container.py
import importlib
import os

import httpx
from injector import Binder, Module, provider, singleton
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.basic_auth_model import BasicAuth
from otobo_znuny.domain_models.otobo_client_config import ClientConfig
from otobo_znuny.domain_models.ticket_operation import TicketOperation
from pydantic import SecretStr

from open_ticket_ai.base.otobo_integration.otobo_adapter import OTOBOAdapter
from open_ticket_ai.core.config.config_models import (
    OpenTicketAIConfig,
    load_config,
)
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipeline import Pipeline
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.core.util.path_util import find_python_code_root_path

CONFIG_PATH = os.getenv("OPEN_TICKET_AI_CONFIG", find_python_code_root_path() / "config.yml")


class AppModule(Module):
    def configure(self, binder: Binder):
        config = load_config(CONFIG_PATH)
        binder.bind(OpenTicketAIConfig, to=config, scope=singleton)

    @provider
    @singleton
    def provide_basic_auth(self, config: OpenTicketAIConfig) -> BasicAuth:
        password = os.getenv(config.system.password_env_var)
        return BasicAuth(user_login=config.system.username, password=SecretStr(password))

    @provider
    @singleton
    def provide_otobo_client(self, config: OpenTicketAIConfig, basic_auth: BasicAuth) -> OTOBOZnunyClient:
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        client = httpx.AsyncClient(limits=limits, timeout=30.0)
        otobo_znuny_client = OTOBOZnunyClient(
            config=ClientConfig(
                base_url=config.system.server_address,
                webservice_name=config.system.webservice_name,
                operation_url_map={
                    TicketOperation.SEARCH.value: config.system.search_operation_url,
                    TicketOperation.GET.value: config.system.get_operation_url,
                    TicketOperation.UPDATE.value: config.system.update_operation_url,
                },
            ),
            client=client,
        )
        otobo_znuny_client.login(basic_auth)
        return otobo_znuny_client

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
            otobo_client: OTOBOZnunyClient,
    ) -> TicketSystemAdapter:
        return OTOBOAdapter(
            config=config.system,
            otobo_client=otobo_client,
        )
