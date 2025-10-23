from abc import ABC
from typing import Any

from open_ticket_ai.core.pipes.pipe import Pipe
from pydantic import BaseModel

from otai_base.ticket_system_integration.ticket_system_service import TicketSystemService


class TicketSystemPipe[ParamsT: BaseModel](Pipe[ParamsT], ABC):
    def __init__(self, ticket_system: TicketSystemService, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._ticket_system = ticket_system
