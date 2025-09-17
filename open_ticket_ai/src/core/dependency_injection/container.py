# FILE_PATH: open_ticket_ai/src/core/dependency_injection/container.py
import os

import httpx
from injector import Binder, Module, provider, singleton
from otobo.clients.otobo_client import OTOBOClient
from otobo.domain_models.basic_auth_model import BasicAuth
from otobo.domain_models.otobo_client_config import OTOBOClientConfig
from otobo.domain_models.ticket_operation import TicketOperation

from open_ticket_ai.src.base.otobo_integration.otobo_adapter import OTOBOAdapter
from open_ticket_ai.src.base.pipe_implementations import SubjectBodyPreparer, QueueTicketFetcher, TicketQueueUpdater
from open_ticket_ai.src.base.pipe_implementations.hf_inference_services.hf_local_ai_inference_service import \
    HFLocalAIInferenceService
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
    def provide_otobo_client(self, config: OpenTicketAIConfig) -> OTOBOClient:
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        client = httpx.AsyncClient(limits=limits, timeout=30.0)
        return OTOBOClient(
            config=OTOBOClientConfig(
                base_url=config.system.server_address,
                webservice_name=config.system.webservice_name,
                auth=BasicAuth(UserLogin=config.system.username, Password=config.system.password),
                operation_url_map={
                    TicketOperation.SEARCH.value: config.system.search_operation_url,
                    TicketOperation.GET.value: config.system.get_operation_url,
                    TicketOperation.UPDATE.value: config.system.update_operation_url,
                },
            ),
            client=client
        )

    # --- Pipeline and Orchestrator ---
    @provider
    @singleton
    def provide_pipeline(
        self,
        queue_ticket_fetcher: QueueTicketFetcher,
        subject_body_preparer: SubjectBodyPreparer,
        hf_local_ai_inference_service: HFLocalAIInferenceService,
        ticket_queue_updater: TicketQueueUpdater,
    ) -> Pipeline:
        return Pipeline(pipes=[
            queue_ticket_fetcher,
            subject_body_preparer,
            hf_local_ai_inference_service,
            ticket_queue_updater,
        ])

    @provider
    @singleton
    def provide_ticket_system_adapter(
        self,
        config: OpenTicketAIConfig,
        otobo_client: OTOBOClient,
    ) -> TicketSystemAdapter:
        return OTOBOAdapter(
            config=config.system,
            otobo_client=otobo_client,
        )
