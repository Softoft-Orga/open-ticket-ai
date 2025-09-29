"""Public package interface for the OTOBO/Znuny integration."""

from .otobo_znuny_ticket_system_service import OTOBOZnunyTicketSystemService
from .otobo_znuny_ticket_system_service_config import (
    RawOTOBOZnunyTicketsystemServiceConfig,
    RenderedOTOBOZnunyTicketsystemServiceConfig,
)
from .models import TicketAdapter

__all__ = [
    "OTOBOZnunyTicketSystemService",
    "RawOTOBOZnunyTicketsystemServiceConfig",
    "RenderedOTOBOZnunyTicketsystemServiceConfig",
    "TicketAdapter",
]
