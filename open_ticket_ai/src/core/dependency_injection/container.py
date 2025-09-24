# FILE_PATH: open_ticket_ai/src/core/dependency_injection/container.py
import os

import httpx
from injector import Binder, Module, provider, singleton
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.basic_auth_model import BasicAuth
from otobo_znuny.domain_models.otobo_client_config import ClientConfig
from otobo_znuny.domain_models.ticket_operation import TicketOperation
from pydantic import SecretStr

from open_ticket_ai.src.base.otobo_integration.otobo_adapter import OTOBOAdapter
from open_ticket_ai.src.base.pipe_implementations.hf_inference_services.hf_local_ai_inference_service import \
    HFLocalAIInferenceService
from open_ticket_ai.src.base.pipe_implementations.subject_body_preparer import SubjectBodyPreparer
from open_ticket_ai.src.base.pipe_implementations.ticket_fetcher import QueueTicketFetcher
from open_ticket_ai.src.base.pipe_implementations.ticket_modifier.ticket_priority_modifier import TicketPriorityModifier
from open_ticket_ai.src.base.pipe_implementations.ticket_modifier.ticket_queue_modifier import TicketQueueModifier
from open_ticket_ai.src.core.config.config_models import (
    OpenTicketAIConfig,
    load_config,
)
from open_ticket_ai.src.core.pipeline.pipeline import Pipeline
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.util.path_util import find_python_code_root_path

CONFIG_PATH = os.getenv("OPEN_TICKET_AI_CONFIG", find_python_code_root_path() / "config.yml")


class AppModule(Module):
    def configure(self, binder: Binder):
        config = load_config(CONFIG_PATH)
        binder.bind(OpenTicketAIConfig, to=config, scope=singleton)

    @provider
    @singleton
    def provide_basic_auth(self, config: OpenTicketAIConfig) -> BasicAuth:
        return BasicAuth(user_login=config.system.username, password=SecretStr(config.system.password))

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
            client=client
        )
        otobo_znuny_client.login(basic_auth)
        return otobo_znuny_client

    # --- Pipeline and Orchestrator ---
    @provider
    @singleton
    def provide_pipeline(
        self,
        config: OpenTicketAIConfig,
        queue_ticket_fetcher: QueueTicketFetcher,
        subject_body_preparer: SubjectBodyPreparer,
        ticket_queue_modifier: TicketQueueModifier,
        ticket_priority_modifier: TicketPriorityModifier,
    ) -> Pipeline:
        queue_hf = HFLocalAIInferenceService(
            hf_model_name=config.hf_model_queue,
            hf_token_env_var=config.hf_model_queue_token_env_var,
        )

        priority_hf = HFLocalAIInferenceService(
            hf_model_name=config.hf_model_priority,
            hf_token_env_var=config.hf_model_priority_token_env_var
        )
        return Pipeline(pipes=[
            queue_ticket_fetcher,
            subject_body_preparer,
            queue_hf,
            ticket_queue_modifier,
            subject_body_preparer,
            priority_hf,
            ticket_priority_modifier,
        ])

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
