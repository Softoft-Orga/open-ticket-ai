"""Template: classify a ticket field and apply the result.

Returns three pipes (classify, update ticket, add note) that can be
spliced into any CompositePipe step list.
"""

from __future__ import annotations

from dataclasses import dataclass

from open_ticket_ai.core.ai_classification_services.classification_service import ClassificationService
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)
from open_ticket_ai.pipes.classification_pipe import ClassificationPipe
from open_ticket_ai.pipes.context_resolver import ContextResolver
from open_ticket_ai.pipes.ticket_system_pipes import AddNotePipe, UpdateTicketPipe


@dataclass(frozen=True)
class ClassifyAndRouteConfig:
    """Declarative config for one classification dimension."""

    prefix: str
    """Short identifier used to derive pipe_ids (e.g. "queue", "priority")."""

    model_name: str
    """HuggingFace model repo or local path."""

    ticket_field: str
    """Field name on UnifiedTicket to update (e.g. "queue", "priority")."""

    fallback_value: str
    """Value to use when confidence is below threshold."""

    note_subject: str
    """Subject line for the audit note."""

    note_body_template: str
    """Body template with ``{value}`` and ``{confidence}`` placeholders."""

    threshold: float
    """Minimum confidence to accept the classification."""


def classify_and_route(
    config: ClassifyAndRouteConfig,
    *,
    classification_service: ClassificationService,
    ticket_system: TicketSystemService,
    get_text: ContextResolver[str],
    get_ticket_id: ContextResolver[str],
) -> list[Pipe]:
    """Build [ClassificationPipe, UpdateTicketPipe, AddNotePipe] for one dimension."""

    classify_id = f"{config.prefix}_classify"

    def _resolve_value(ctx: PipeContext) -> tuple[str, float]:
        label = ctx.get_result(classify_id, "label")
        confidence = ctx.get_result(classify_id, "confidence")
        value = label if confidence >= config.threshold else config.fallback_value
        return value, confidence

    def _make_update(ctx: PipeContext) -> UnifiedTicket:
        value, _ = _resolve_value(ctx)
        return UnifiedTicket(**{config.ticket_field: UnifiedEntity(name=value)})

    def _make_note(ctx: PipeContext) -> UnifiedNote:
        value, confidence = _resolve_value(ctx)
        return UnifiedNote(
            subject=config.note_subject,
            body=config.note_body_template.format(value=value, confidence=confidence),
        )

    return [
        ClassificationPipe(
            pipe_id=classify_id,
            classification_service=classification_service,
            model_name=config.model_name,
            get_text=get_text,
        ),
        UpdateTicketPipe(
            pipe_id=f"{config.prefix}_update_ticket",
            ticket_system=ticket_system,
            get_ticket_id=get_ticket_id,
            get_updates=_make_update,
        ),
        AddNotePipe(
            pipe_id=f"{config.prefix}_add_note",
            ticket_system=ticket_system,
            get_ticket_id=get_ticket_id,
            get_note=_make_note,
        ),
    ]
