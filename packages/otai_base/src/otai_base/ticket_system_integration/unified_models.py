from __future__ import annotations

from open_ticket_ai.core.base_model import StrictBaseModel
from pydantic import Field


class UnifiedNote(StrictBaseModel):
    id: str | None = Field(
        default=None, description="Unique identifier for the note if it exists in the ticket system."
    )
    subject: str = Field(
        default="", description="Subject or title of the note providing a brief summary of its content."
    )
    body: str = Field(
        default="", description="Full text content of the note containing the detailed message or comment."
    )


class UnifiedEntity(StrictBaseModel):
    id: str | None = Field(
        default=None, description="Unique identifier for the entity in the ticket system if available."
    )
    name: str | None = Field(
        default=None, description="Human-readable name or label for the entity used for display purposes."
    )


class UnifiedTicketBase(StrictBaseModel):
    id: str | None = Field(
        default=None, description="Unique identifier for the ticket in the ticket system if available."
    )
    subject: str | None = Field(
        default=None, description="Subject or title of the ticket summarizing the main issue or request."
    )
    queue: UnifiedEntity | None = Field(
        default=None,
        description="Queue or category to which this ticket is assigned for organizing and routing tickets.",
    )
    priority: UnifiedEntity | None = Field(
        default=None, description="Priority level of the ticket indicating urgency and importance for handling."
    )
    notes: list[UnifiedNote] | None = Field(
        default=None,
        description="List of notes or comments associated with this ticket providing communication history.",
    )


class UnifiedTicket(UnifiedTicketBase):
    body: str | None = Field(
        default=None, description="Main body text of the ticket containing the detailed description or initial message."
    )


class TicketSearchCriteria(StrictBaseModel):
    queue: UnifiedEntity | None = Field(
        default=None, description="Optional queue filter to limit search results to tickets in a specific queue."
    )
    limit: int = Field(
        default=10, description="Maximum number of tickets to return in the search results for pagination."
    )
    offset: int = Field(
        default=0, description="Number of tickets to skip before returning results for pagination and page navigation."
    )
