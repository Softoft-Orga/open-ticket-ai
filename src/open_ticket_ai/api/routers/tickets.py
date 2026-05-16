"""Ticket system CRUD endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException, Request

from open_ticket_ai.api.models import (
    EntityBody,
    NoteBody,
    TicketCreateRequest,
    TicketResponse,
    TicketSearchRequest,
    TicketUpdateRequest,
)
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)

if TYPE_CHECKING:
    from open_ticket_ai.api.dependencies import AppState

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


def _state(request: Request) -> AppState:
    return request.app.state.app_state


def _entity(e: EntityBody | None) -> UnifiedEntity | None:
    if e is None:
        return None
    return UnifiedEntity(id=e.id, name=e.name)


def _entity_resp(e: UnifiedEntity | None) -> EntityBody | None:
    if e is None:
        return None
    return EntityBody(id=e.id, name=e.name)


def _note_resp(n: UnifiedNote) -> NoteBody:
    return NoteBody(subject=n.subject, body=n.body, content_type=n.content_type)


def _ticket_resp(t: UnifiedTicket) -> TicketResponse:
    return TicketResponse(
        id=t.id,
        subject=t.subject,
        body=t.body,
        queue=_entity_resp(t.queue),
        priority=_entity_resp(t.priority),
        customer=_entity_resp(t.customer),
        notes=[_note_resp(n) for n in t.notes] if t.notes else None,
    )


@router.get("", response_model=list[TicketResponse])
async def search_tickets(
    request: Request,
    queue_name: str | None = None,
    queue_id: str | None = None,
    limit: int = 10,
    offset: int = 0,
) -> list[TicketResponse]:
    ts = _state(request).ticket_system
    queue = None
    if queue_name or queue_id:
        queue = UnifiedEntity(id=queue_id, name=queue_name)
    criteria = TicketSearchCriteria(queue=queue, limit=limit, offset=offset)
    tickets = await ts.find_tickets(criteria)
    return [_ticket_resp(t) for t in tickets]


@router.post("/search", response_model=list[TicketResponse])
async def search_tickets_post(
    request: Request,
    body: TicketSearchRequest,
) -> list[TicketResponse]:
    ts = _state(request).ticket_system
    criteria = TicketSearchCriteria(
        queue=_entity(body.queue),
        limit=body.limit,
        offset=body.offset,
    )
    tickets = await ts.find_tickets(criteria)
    return [_ticket_resp(t) for t in tickets]


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(request: Request, ticket_id: str) -> TicketResponse:
    ts = _state(request).ticket_system
    ticket = await ts.get_ticket(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
    return _ticket_resp(ticket)


@router.post("", response_model=TicketResponse, status_code=201)
async def create_ticket(request: Request, body: TicketCreateRequest) -> TicketResponse:
    ts = _state(request).ticket_system
    ticket = UnifiedTicket(
        subject=body.subject,
        body=body.body,
        queue=_entity(body.queue),
        priority=_entity(body.priority),
        customer=_entity(body.customer),
    )
    created = await ts.create_ticket(ticket)
    if isinstance(created, UnifiedTicket):
        return _ticket_resp(created)
    return TicketResponse(id=str(created), subject=body.subject, body=body.body)


@router.patch("/{ticket_id}")
async def update_ticket(
    request: Request,
    ticket_id: str,
    body: TicketUpdateRequest,
) -> dict[str, bool]:
    ts = _state(request).ticket_system
    updates = UnifiedTicket(
        subject=body.subject,
        body=body.body,
        queue=_entity(body.queue),
        priority=_entity(body.priority),
        customer=_entity(body.customer),
    )
    success = await ts.update_ticket(ticket_id, updates)
    return {"success": success}


@router.post("/{ticket_id}/notes", status_code=201)
async def add_note(
    request: Request,
    ticket_id: str,
    body: NoteBody,
) -> dict[str, bool]:
    ts = _state(request).ticket_system
    note = UnifiedNote(subject=body.subject, body=body.body, content_type=body.content_type)
    success = await ts.add_note(ticket_id, note)
    return {"success": success}
