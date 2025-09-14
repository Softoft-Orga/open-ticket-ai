from pydantic import BaseModel

from open_ticket_ai.src.core.ticket_system_integration.unified_models import UnifiedTicket


class HFLocalAIInferenceServiceOutput(BaseModel):
    prediction: str | int
    confidence: float
    ticket: UnifiedTicket
