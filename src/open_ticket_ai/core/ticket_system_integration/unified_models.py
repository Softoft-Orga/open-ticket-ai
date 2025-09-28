from __future__ import annotations

from pydantic import BaseModel


class UnifiedNote(BaseModel):
    id: int | None = None
    subject: str = ""
    body: str = ""


class UnifiedEntity(BaseModel):
    id: int | str | None = None
    name: str | None = None


class UnifiedTicketBase(BaseModel):
    id: int | str | None = None
    subject: str | None = None
    queue: UnifiedEntity | None = None
    priority: UnifiedEntity | None = None
    note: UnifiedNote | None = None


class UnifiedTicket(UnifiedTicketBase):
    body: str | None = None


class TicketSearchCriteria(BaseModel):
    queue: UnifiedEntity | None = None
    limit: int | None = 10
    offset: int | None = 0
