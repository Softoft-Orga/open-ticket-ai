"""Minimal stub of the `otobo` package for test purposes.

The real project depends on the external `otobo` package which provides a
client for interacting with OTOBO/OTRS ticket systems.  For unit testing
purposes we provide lightweight stand-ins that mimic the interfaces required by
our adapters.  Only the small subset of behaviour exercised in the tests is
implemented.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .models.request_models import AuthData
from .models.ticket_models import TicketBase


@dataclass
class OTOBOClientConfig:
    base_url: str
    service: str
    auth: AuthData
    operations: Optional[Dict[str, str]] = None


class OTOBOClient:
    """Very small stub of the real OTOBO client."""

    def __init__(self, config: OTOBOClientConfig):
        self.config = config

    async def search_and_get(self, query: "TicketSearchRequest") -> List[TicketBase]:  # pragma: no cover - overridden in tests
        return []

    async def update_ticket(self, payload: "TicketUpdateRequest") -> None:  # pragma: no cover - overridden in tests
        return None

    async def create_ticket(self, payload: Any) -> Any:  # pragma: no cover - overridden in tests
        return None

    async def add_note(self, ticket_id: str | int, note: Any) -> Any:  # pragma: no cover - overridden in tests
        return None


@dataclass
class TicketSearchRequest:
    TicketID: Optional[str] = None
    QueueIDs: Optional[List[int]] = None
    Queues: Optional[List[str]] = None


@dataclass
class TicketUpdateRequest:
    TicketID: int
    Ticket: TicketBase
