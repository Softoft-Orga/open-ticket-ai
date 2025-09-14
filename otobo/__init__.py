from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Any

from .models.ticket_models import TicketBase, ArticleDetail


class TicketOperation(Enum):
    SEARCH = "search"
    UPDATE = "update"
    GET = "get"


@dataclass
class OTOBOClientConfig:
    base_url: str
    service: str
    auth: Optional[Any]
    operations: Dict['TicketOperation', str]


@dataclass
class TicketSearchRequest:
    TicketID: Optional[str] = None
    QueueIDs: Optional[List[int]] = None
    Queues: Optional[List[str]] = None


@dataclass
class TicketUpdateRequest:
    TicketID: int
    Ticket: TicketBase


class OTOBOClient:
    def __init__(self, config: OTOBOClientConfig):
        self.config = config
        self.last_payload: Optional[TicketUpdateRequest] = None

    async def search_and_get(self, query: TicketSearchRequest):
        raise NotImplementedError

    async def update_ticket(self, payload: TicketUpdateRequest):
        self.last_payload = payload
        return True


__all__ = [
    "TicketOperation",
    "OTOBOClientConfig",
    "TicketSearchRequest",
    "TicketUpdateRequest",
    "OTOBOClient",
    "TicketBase",
    "ArticleDetail",
]
