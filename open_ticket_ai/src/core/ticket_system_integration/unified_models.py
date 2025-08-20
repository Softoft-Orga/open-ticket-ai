from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Dict, List

from pydantic import BaseModel

class UnifiedNote(BaseModel):
    id: Optional[str] = None
    subject: Optional[str] = None
    body: str = ""

class UnifiedEntity(BaseModel):
    """Base entity with optional ID and name.

    Attributes:
        id (Optional[int]): Unique identifier for the entity. Defaults to None.
        name (Optional[str]): Display name of the entity. Defaults to None.
    """

    id: Optional[str] = None
    name: Optional[str] = None



class UnifiedQueue(UnifiedEntity):
    """Represents a ticket queue.

    Inherits attributes from `UnifiedEntity`.
    """


class UnifiedPriority(UnifiedEntity):
    """Represents a ticket priority level.

    Inherits attributes from `UnifiedEntity`.
    """

class UnifiedTicketBase(BaseModel):
    """Base class for unified ticket models.

    Attributes:
        id (Optional[str]): Unique identifier for the ticket. Defaults to None.
        subject (Optional[str]): Subject line of the ticket. Defaults to None.
        queue (Optional[UnifiedQueue]): Queue to which the ticket belongs. Defaults to None.
        priority (Optional[UnifiedPriority]): Priority level of the ticket. Defaults to None.
    """

    id: Optional[str] = None
    subject: Optional[str] = None
    queue: Optional[UnifiedQueue] = None
    priority: Optional[UnifiedPriority] = None


class UnifiedTicket(UnifiedTicketBase):
    """
    Attributes:
        id (Optional[str]): Unique identifier for the ticket. Defaults to None.
        subject (Optional[str]): Subject line of the ticket. Defaults to None.
        body (Optional[str]): Main content/description of the ticket. Defaults to None.
        queue (Optional[UnifiedQueue]): Queue to which the ticket belongs. Defaults to None.
        priority (Optional[UnifiedPriority]): Priority level of the ticket. Defaults to None.
        notes (Optional[List[UnifiedNote]]): List of notes associated with the ticket. Defaults
    """

    id: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    queue: Optional[UnifiedQueue] = None
    priority: Optional[UnifiedPriority] = None
    notes: Optional[List[UnifiedNote]] = None

class UnifiedTicketUpdate(UnifiedTicketBase):
    """Represents an update to a ticket.


    Attributes:
        id (Optional[str]): Unique identifier for the ticket. Defaults to None.
        subject (Optional[str]): Subject line of the ticket. Defaults to None.
        queue (Optional[UnifiedQueue]): Queue to which the ticket belongs. Defaults to None.
        priority (Optional[UnifiedPriority]): Priority level of the ticket. Defaults to None.
    """
    pass


class TicketSearchCriteria(BaseModel):
    """Criteria for searching/filtering tickets.

    Attributes:
        id (Optional[str]): Ticket ID to search for. Defaults to None.
        subject (Optional[str]): Text to search in ticket subjects. Defaults to None.
        queue (Optional[UnifiedQueue]): Queue to filter by. Defaults to None.
        user (Optional[UnifiedUser]): User to filter by (e.g., owner). Defaults to None.
    """

    id: Optional[str] = None
    queue: Optional[UnifiedQueue] = None
