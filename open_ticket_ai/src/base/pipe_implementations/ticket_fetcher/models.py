from pydantic import BaseModel

from open_ticket_ai.src.core.config.config_models import ProvidableConfig
from open_ticket_ai.src.core.ticket_system_integration.unified_models import UnifiedTicket


class QueueTicketFetcherOutput(BaseModel):
    ticket: UnifiedTicket

class QueueTicketFetcherConfig(ProvidableConfig):
    filter_by_queue: str
