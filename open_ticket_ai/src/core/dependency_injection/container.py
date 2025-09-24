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
from open_ticket_ai.src.base.pipe_implementations.base_ticket_modifier import TicketModifier
from open_ticket_ai.src.base.pipe_implementations.hf_local_ai_inference_service import \
    HFLocalAIInferenceService
from open_ticket_ai.src.base.pipe_implementations.list_value_mapper import ListValueMapper
from open_ticket_ai.src.base.pipe_implementations.low_confidence_handler import LowConfidenceHandler
from open_ticket_ai.src.base.pipe_implementations.subject_body_preparer import SubjectBodyPreparer
from open_ticket_ai.src.base.pipe_implementations.ticket_fetcher import TicketFetcher
from open_ticket_ai.src.core.config.config_models import (
    OpenTicketAIConfig,
    load_config,
)
from open_ticket_ai.src.core.pipeline.pipeline import Pipeline
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.util.path_util import find_python_code_root_path

CONFIG_PATH = os.getenv("OPEN_TICKET_AI_CONFIG", find_python_code_root_path() / "config.yml")

PIPE_REGISTRY = {
    "TicketFetcher": TicketFetcher,
    "SubjectBodyPreparer": SubjectBodyPreparer,
    "HFLocalAIInferenceService": HFLocalAIInferenceService,
    "ListValueMapper": ListValueMapper,
    "LowConfidenceHandler": LowConfidenceHandler,
    "TicketModifier": TicketModifier,
}


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
        ticket_system_adapter: TicketSystemAdapter,
    ) -> Pipeline:
        ticket_fetcher = TicketFetcher(
            config=config.pipes['ticket_fetcher'],
            ticket_system=ticket_system_adapter
        )

        subject_body_preparer = SubjectBodyPreparer(
            config=config.pipes['subject_body_preparer']
        )

        queue_ai_model = HFLocalAIInferenceService(
            config=config.pipes['queue_ai_model']
        )

        priority_ai_model = HFLocalAIInferenceService(
            config=config.pipes['priority_ai_model']
        )

        queue_mapper = ListValueMapper(
            config=config.pipes['queue_mapper']
        )

        priority_mapper = ListValueMapper(
            config=config.pipes['priority_mapper']
        )

        queue_low_confidence_handler = LowConfidenceHandler(
            config=config.pipes['queue_low_confidence_handler']
        )

        priority_low_confidence_handler = LowConfidenceHandler(
            config=config.pipes['priority_low_confidence_handler']
        )

        queue_updater = TicketModifier(
            config=config.pipes['queue_updater'],
            ticket_system=ticket_system_adapter
        )

        queue_note_adder = TicketModifier(
            config=config.pipes['queue_note_adder'],
            ticket_system=ticket_system_adapter
        )

        priority_updater = TicketModifier(
            config=config.pipes['priority_updater'],
            ticket_system=ticket_system_adapter
        )

        priority_note_adder = TicketModifier(
            config=config.pipes['priority_note_adder'],
            ticket_system=ticket_system_adapter
        )

        # --- 2. Assemble the single pipeline in the correct order ---

        return Pipeline(pipes=[
            ticket_fetcher,
            subject_body_preparer,

            # Queue classification branch
            queue_ai_model,
            queue_mapper,
            queue_low_confidence_handler,
            queue_updater,
            queue_note_adder,

            # Priority classification branch
            priority_ai_model,
            priority_mapper,
            priority_low_confidence_handler,
            priority_updater,
            priority_note_adder,
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
