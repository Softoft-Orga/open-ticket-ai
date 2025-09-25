from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class UnifiedNote(BaseModel):
    id: int | None = None
    subject: str | None = None
    body: str = ""


class UnifiedEntity(BaseModel):
    id: int | None = None
    name: str | None = None


class UnifiedTicketBase(BaseModel):
    id: int | None = None
    subject: str | None = None
    queue: UnifiedEntity | None = None
    priority: UnifiedEntity | None = None
    note: UnifiedNote | None = None


class UnifiedTicket(UnifiedTicketBase):
    body: Optional[str] = None


class TicketSearchCriteria(BaseModel):
    queue: UnifiedEntity | None = None
    limit: int | None = None
    offset: int | None = None
