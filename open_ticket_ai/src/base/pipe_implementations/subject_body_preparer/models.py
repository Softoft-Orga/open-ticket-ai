from pydantic import BaseModel

from open_ticket_ai.src.core.ticket_system_integration.unified_models import UnifiedTicket

class SubjectBodyPreparerOutput(BaseModel):
    subject_body_combined: str
    ticket: UnifiedTicket
