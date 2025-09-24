from pydantic import BaseModel

from open_ticket_ai.src.base.pipe_implementations.models import UnifiedTicketInformation
from open_ticket_ai.src.core.ticket_system_integration.unified_models import UnifiedTicket


class TicketUpdaterOutput(UnifiedTicketInformation):
    ticket: UnifiedTicket
