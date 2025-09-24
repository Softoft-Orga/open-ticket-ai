from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class UnifiedNote(BaseModel):
    id: Optional[str] = None
    subject: Optional[str] = None
    body: str = ""


class UnifiedEntity(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None


class UnifiedQueue(UnifiedEntity):
    pass


class UnifiedPriority(UnifiedEntity):
    pass


class UnifiedTicketBase(BaseModel):
    id: Optional[str] = None
    subject: Optional[str] = None
    queue: Optional[UnifiedQueue] = None
    priority: Optional[UnifiedPriority] = None


class UnifiedTicket(UnifiedTicketBase):
    body: Optional[str] = None


class TicketSearchCriteria(BaseModel):
    queue: Optional[UnifiedQueue] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
