"""Shared application state and FastAPI dependency helpers."""

from __future__ import annotations

import logging
from typing import Any

from open_ticket_ai.api.models import SettingsFieldInfo, TemplateParameterSchema, WorkflowTemplateResponse
from open_ticket_ai.core.ai_classification_services.classification_service import ClassificationService
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
)
from open_ticket_ai.settings import OtoboTicketSystemSettings, Settings, ZammadTicketSystemSettings
from open_ticket_ai.workflow_manager import WorkflowManager

logger = logging.getLogger(__name__)

_TEMPLATE_CLASSIFY_AND_ROUTE = "classify_and_route_polling"

WORKFLOW_TEMPLATES: dict[str, WorkflowTemplateResponse] = {
    _TEMPLATE_CLASSIFY_AND_ROUTE: WorkflowTemplateResponse(
        name=_TEMPLATE_CLASSIFY_AND_ROUTE,
        description=(
            "Polls incoming tickets from a queue, classifies queue and priority "
            "using HuggingFace models, updates the ticket, and adds an audit note."
        ),
        parameters=[
            TemplateParameterSchema(
                name="incoming_queue", type="string",
                description="Queue to poll for new tickets",
            ),
            TemplateParameterSchema(
                name="queue_model", type="string",
                description="HuggingFace model for queue classification",
            ),
            TemplateParameterSchema(
                name="priority_model", type="string",
                description="HuggingFace model for priority classification",
            ),
            TemplateParameterSchema(
                name="fallback_queue", type="string",
                description="Queue assigned when confidence is below threshold",
            ),
            TemplateParameterSchema(
                name="fallback_priority", type="string",
                description="Priority assigned when confidence is below threshold",
            ),
            TemplateParameterSchema(
                name="classification_confidence_threshold", type="number",
                description="Minimum confidence to accept a classification (0-1)",
                default=0.8,
            ),
            TemplateParameterSchema(
                name="trigger_interval", type="number",
                description="Seconds between polling cycles",
                default=30.0,
            ),
            TemplateParameterSchema(
                name="orchestrator_sleep", type="number",
                description="Seconds between orchestrator loop iterations",
                default=0.01,
            ),
        ],
    ),
}


def build_ticket_system(
    ts_settings: OtoboTicketSystemSettings | ZammadTicketSystemSettings,
) -> TicketSystemService:
    """Construct a TicketSystemService from source-agnostic settings."""
    # TODO This is a mess and needs to be refactored to handle more ticket systems properly.
    match ts_settings:
        case ZammadTicketSystemSettings():
            from open_ticket_ai.zammad.models import ZammadTSServiceParams
            from open_ticket_ai.zammad.zammad_ticket_system_service import ZammadTicketsystemService

            return ZammadTicketsystemService(
                params=ZammadTSServiceParams(
                    base_url=ts_settings.base_url,
                    access_token=ts_settings.access_token,
                ),
            )
        case OtoboTicketSystemSettings():
            from open_ticket_ai.otobo_znuny.models import OTOBOZnunyTSServiceParams
            from open_ticket_ai.otobo_znuny.oto_znuny_ts_service import OTOBOZnunyTicketSystemService

            return OTOBOZnunyTicketSystemService(
                params=OTOBOZnunyTSServiceParams(
                    base_url=ts_settings.base_url,
                    username=ts_settings.username,
                    password=ts_settings.password,
                    webservice_name=ts_settings.webservice_name,
                ),
            )


_OPERATIONAL_FIELDS: set[str] = {
    name
    for name, info in Settings.model_fields.items()
    if (info.json_schema_extra or {}).get("category") == "operational"
}


class AppState:
    """Holds shared runtime objects, initialised once at startup."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.ticket_system: TicketSystemService = build_ticket_system(settings.ticket_system)
        self.classification_service: ClassificationService = self._build_classification_service(settings)
        self.workflow_manager = WorkflowManager()

    # ── Settings management ───────────────────────────────────────

    def get_settings_masked(self) -> dict[str, Any]:
        """Return current settings with secret fields replaced by a mask."""
        result: dict[str, Any] = {}
        for name, info in Settings.model_fields.items():
            extra = info.json_schema_extra or {}
            value = getattr(self.settings, name)
            if extra.get("secret"):
                result[name] = "***" if value else None
            else:
                result[name] = value
        return result

    @staticmethod
    def get_settings_schema() -> dict[str, SettingsFieldInfo]:
        """Build schema metadata for every Settings field."""
        schema: dict[str, SettingsFieldInfo] = {}
        for name, info in Settings.model_fields.items():
            extra = info.json_schema_extra or {}
            annotation = info.annotation
            type_str = "string"
            if annotation is float:
                type_str = "number"
            elif annotation is int:
                type_str = "integer"
            elif annotation is bool:
                type_str = "boolean"
            schema[name] = SettingsFieldInfo(
                type=type_str,
                description=info.description or "",
                default=info.default,
                restart_required=extra.get("restart_required", True),
                category=extra.get("category", "infrastructure"),
                secret=extra.get("secret", False),
            )
        return schema

    def update_settings(self, updates: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
        """Apply partial updates to operational settings. Returns (masked settings, updated field names)."""
        rejected = [k for k in updates if k not in _OPERATIONAL_FIELDS]
        if rejected:
            msg = f"Cannot update non-operational fields: {', '.join(rejected)}"
            raise ValueError(msg)
        current = self.settings.model_dump()
        current.update(updates)
        self.settings = Settings.model_construct(**current)
        return self.get_settings_masked(), list(updates.keys())

    def build_pipeline_from_template(self, template_name: str, params: dict[str, Any]) -> Pipe:
        if template_name == _TEMPLATE_CLASSIFY_AND_ROUTE:
            return self._build_classify_and_route(params)
        msg = f"Unknown template: {template_name}"
        raise ValueError(msg)

    # ── private helpers ──────────────────────────────────────────

    def _build_classify_and_route(self, params: dict[str, Any]) -> Pipe:
        from open_ticket_ai.pipes.orchestrators.simple_sequential_orchestrator import SimpleSequentialOrchestrator
        from open_ticket_ai.pipes.templates import ClassifyAndRouteConfig, classify_and_route
        from open_ticket_ai.pipes.ticket_system_pipes import FetchTicketsPipe

        s = self.settings
        incoming_queue = params.get("incoming_queue", s.incoming_queue)
        queue_model = params.get("queue_model", s.queue_model)
        priority_model = params.get("priority_model", s.priority_model)
        fallback_queue = params.get("fallback_queue", s.fallback_queue)
        fallback_priority = params.get("fallback_priority", s.fallback_priority)
        threshold = float(params.get("classification_confidence_threshold", s.classification_confidence_threshold))
        trigger_interval = float(params.get("trigger_interval", s.trigger_interval))
        orch_sleep = float(params.get("orchestrator_sleep", s.orchestrator_sleep))

        ts = self.ticket_system
        clf = self.classification_service

        def _get_ticket_text(ctx: PipeContext) -> str:
            ticket = ctx.get_result("ticket_fetcher", "fetched_tickets")[0]
            return f"{ticket['subject']} {ticket['body']}"

        def _get_ticket_id(ctx: PipeContext) -> str:
            return str(ctx.get_result("ticket_fetcher", "fetched_tickets")[0]["id"])

        queue_steps = classify_and_route(
            ClassifyAndRouteConfig(
                prefix="queue",
                model_name=queue_model,
                ticket_field="queue",
                fallback_value=fallback_queue,
                note_subject="Automatische Queue-Klassifizierung",
                note_body_template="Das Ticket wurde der Queue {value} zugeordnet (Konfidenz: {confidence:.2f}).",
                threshold=threshold,
            ),
            classification_service=clf,
            ticket_system=ts,
            get_text=_get_ticket_text,
            get_ticket_id=_get_ticket_id,
        )

        priority_steps = classify_and_route(
            ClassifyAndRouteConfig(
                prefix="priority",
                model_name=priority_model,
                ticket_field="priority",
                fallback_value=fallback_priority,
                note_subject="Automatische Priorisierung",
                note_body_template="Das Ticket wurde der Priorität {value} zugeordnet (Konfidenz: {confidence:.2f}).",
                threshold=threshold,
            ),
            classification_service=clf,
            ticket_system=ts,
            get_text=_get_ticket_text,
            get_ticket_id=_get_ticket_id,
        )

        return SimpleSequentialOrchestrator.polling(
            pipe_id="orchestrator",
            interval_seconds=trigger_interval,
            steps=[
                FetchTicketsPipe(
                    pipe_id="ticket_fetcher",
                    ticket_system=ts,
                    search_criteria=TicketSearchCriteria(
                        queue=UnifiedEntity(name=incoming_queue),
                        limit=1,
                    ),
                ),
                *queue_steps,
                *priority_steps,
            ],
            sleep=orch_sleep,
        )

    @staticmethod
    def _build_classification_service(settings: Settings) -> ClassificationService:
        from open_ticket_ai.hf_local.hf_classification_service import HFClassificationService

        return HFClassificationService(api_token=settings.hf_api_token)
