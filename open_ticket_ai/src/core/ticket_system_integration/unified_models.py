"""Unified data models used across ticket system integrations.

These models provide a normalized representation of ticketing concepts so
that adapters for different ticketing systems can share a common interface.
"""
from __future__ import annotations

from typing import Optional, List
from pydantic import BaseModel


class UnifiedNote(BaseModel):
    """Represents a single note/article on a ticket."""

    id: Optional[str] = None
    subject: Optional[str] = None
    body: str = ""


class UnifiedEntity(BaseModel):
    """Base class for simple named entities (queue, priority, user, ...)."""

    id: Optional[str] = None
    name: Optional[str] = None


class UnifiedQueue(UnifiedEntity):
    """Queue representation in the unified model."""
    pass


class UnifiedPriority(UnifiedEntity):
    """Priority representation in the unified model."""
    pass


class UnifiedUser(UnifiedEntity):
    """User representation used for search criteria."""
    pass


class UnifiedTicketBase(BaseModel):
    """Common fields shared by ticket and ticket update models."""

    id: Optional[str] = None
    subject: Optional[str] = None
    queue: Optional[UnifiedQueue] = None
    priority: Optional[UnifiedPriority] = None


class UnifiedTicket(UnifiedTicketBase):
    """Complete ticket model including body and notes."""

    body: Optional[str] = None
    notes: List[UnifiedNote] = []


class UnifiedTicketUpdate(UnifiedTicketBase):
    """Model used when updating a ticket."""

    body: Optional[str] = None
    notes: List[UnifiedNote] = []


class TicketSearchCriteria(BaseModel):
    """Criteria used when searching for tickets."""

    id: Optional[str] = None
    queue: Optional[UnifiedQueue] = None
    user: Optional[UnifiedUser] = None
