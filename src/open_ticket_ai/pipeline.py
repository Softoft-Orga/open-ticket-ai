"""Pipeline construction for Open Ticket AI runtime.

This replaces the YAML pipeline DSL with direct Python construction.
"""

from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)
from open_ticket_ai.settings import Settings
from otai_base.pipes.classification_pipe import ClassificationPipe
from otai_base.pipes.composite_pipe import CompositePipe
from otai_base.pipes.interval_trigger_pipe import IntervalTrigger
from otai_base.pipes.orchestrators.simple_sequential_orchestrator import SimpleSequentialOrchestrator
from otai_base.pipes.pipe_runners.simple_sequential_runner import SimpleSequentialRunner
from otai_base.pipes.ticket_system_pipes import AddNotePipe, FetchTicketsPipe, UpdateTicketPipe
from otai_hf_local.hf_classification_service import HFClassificationService
from otai_otobo_znuny.models import OTOBOZnunyTSServiceParams
from otai_otobo_znuny.oto_znuny_ts_service import OTOBOZnunyTicketSystemService


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

    def _queue_update(ctx: PipeContext) -> UnifiedTicket:
        label = ctx.get_result("queue_classify", "label")
        confidence = ctx.get_result("queue_classify", "confidence")
        queue = label if confidence >= threshold else settings.fallback_queue
        return UnifiedTicket(queue=UnifiedEntity(name=queue))

    def _queue_note(ctx: PipeContext) -> UnifiedNote:
        label = ctx.get_result("queue_classify", "label")
        confidence = ctx.get_result("queue_classify", "confidence")
        queue = label if confidence >= threshold else settings.fallback_queue
        return UnifiedNote(
            subject="Automatische Queue-Klassifizierung",
            body=f"Das Ticket wurde der Queue {queue} zugeordnet (Konfidenz: {confidence:.2f}).",
        )

    def _priority_update(ctx: PipeContext) -> UnifiedTicket:
        label = ctx.get_result("priority_classify", "label")
        confidence = ctx.get_result("priority_classify", "confidence")
        priority = label if confidence >= threshold else settings.fallback_priority
        return UnifiedTicket(priority=UnifiedEntity(name=priority))

    def _priority_note(ctx: PipeContext) -> UnifiedNote:
        label = ctx.get_result("priority_classify", "label")
        confidence = ctx.get_result("priority_classify", "confidence")
        priority = label if confidence >= threshold else settings.fallback_priority
        return UnifiedNote(
            subject="Automatische Priorisierung",
            body=f"Das Ticket wurde der Priorität {priority} zugeordnet (Konfidenz: {confidence:.2f}).",
        )

    return SimpleSequentialOrchestrator(
        pipe_id="orchestrator",
        steps=[
            SimpleSequentialRunner(
                pipe_id="ticket-routing-runner",
                trigger=IntervalTrigger(
                    pipe_id="every_interval",
                    interval_seconds=settings.trigger_interval,
                ),
                run_pipe=CompositePipe(
                    pipe_id="ticket-routing",
                    steps=[
                        FetchTicketsPipe(
                            pipe_id="ticket_fetcher",
                            ticket_system=ts,
                            search_criteria=TicketSearchCriteria(
                                queue=UnifiedEntity(name=settings.incoming_queue),
                                limit=1,
                            ),
                        ),
                        # --- Queue classification ---
                        ClassificationPipe(
                            pipe_id="queue_classify",
                            classification_service=clf,
                            model_name=settings.queue_model,
                            get_text=_get_ticket_text,
                        ),
                        UpdateTicketPipe(
                            pipe_id="queue_update_ticket",
                            ticket_system=ts,
                            get_ticket_id=_get_ticket_id,
                            get_updates=_queue_update,
                        ),
                        AddNotePipe(
                            pipe_id="queue_add_note",
                            ticket_system=ts,
                            get_ticket_id=_get_ticket_id,
                            get_note=_queue_note,
                        ),
                        # --- Priority classification ---
                        ClassificationPipe(
                            pipe_id="priority_classify",
                            classification_service=clf,
                            model_name=settings.priority_model,
                            get_text=_get_ticket_text,
                        ),
                        UpdateTicketPipe(
                            pipe_id="priority_update_ticket",
                            ticket_system=ts,
                            get_ticket_id=_get_ticket_id,
                            get_updates=_priority_update,
                        ),
                        AddNotePipe(
                            pipe_id="priority_add_note",
                            ticket_system=ts,
                            get_ticket_id=_get_ticket_id,
                            get_note=_priority_note,
                        ),
                    ],
                ),
            ),
        ],
        sleep=settings.orchestrator_sleep,
    )
