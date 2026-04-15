"""Pipeline construction for Open Ticket AI runtime."""

from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
)
from open_ticket_ai.hf_local.hf_classification_service import HFClassificationService
from open_ticket_ai.otobo_znuny.models import OTOBOZnunyTSServiceParams
from open_ticket_ai.otobo_znuny.oto_znuny_ts_service import OTOBOZnunyTicketSystemService
from open_ticket_ai.pipes.orchestrators.simple_sequential_orchestrator import SimpleSequentialOrchestrator
from open_ticket_ai.pipes.templates import ClassifyAndRouteConfig, classify_and_route
from open_ticket_ai.pipes.ticket_system_pipes import FetchTicketsPipe
from open_ticket_ai.settings import Settings


def _get_ticket_text(ctx: PipeContext) -> str:
    ticket = ctx.get_result("ticket_fetcher", "fetched_tickets")[0]
    return f"{ticket['subject']} {ticket['body']}"


def _get_ticket_id(ctx: PipeContext) -> str:
    return str(ctx.get_result("ticket_fetcher", "fetched_tickets")[0]["id"])


def create_pipeline(settings: Settings) -> Pipe:
    """Build the complete ticket-routing orchestrator from settings."""

    ts = OTOBOZnunyTicketSystemService(
        params=OTOBOZnunyTSServiceParams(
            base_url=settings.otobo_base_url,
            username=settings.otobo_username,
            password=settings.otobo_password,
            webservice_name=settings.otobo_webservice_name,
        ),
    )
    clf = HFClassificationService(api_token=settings.hf_api_token)

    threshold = settings.classification_confidence_threshold

    queue_steps = classify_and_route(
        ClassifyAndRouteConfig(
            prefix="queue",
            model_name=settings.queue_model,
            ticket_field="queue",
            fallback_value=settings.fallback_queue,
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
            model_name=settings.priority_model,
            ticket_field="priority",
            fallback_value=settings.fallback_priority,
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
        interval_seconds=settings.trigger_interval,
        steps=[
            FetchTicketsPipe(
                pipe_id="ticket_fetcher",
                ticket_system=ts,
                search_criteria=TicketSearchCriteria(
                    queue=UnifiedEntity(name=settings.incoming_queue),
                    limit=1,
                ),
            ),
            *queue_steps,
            *priority_steps,
        ],
        sleep=settings.orchestrator_sleep,
    )
