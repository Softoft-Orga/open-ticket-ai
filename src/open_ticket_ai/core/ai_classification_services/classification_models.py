from open_ticket_ai import StrictBaseModel


class ClassificationRequest(StrictBaseModel):
    text: str
    model_name: str
    api_token: str | None = None


class ClassificationResult(StrictBaseModel):
    label: str
    confidence: float
