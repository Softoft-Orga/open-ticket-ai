from typing import Protocol

from open_ticket_ai.base.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)


class ClassificationService(Protocol):
    def classify(self, req: ClassificationRequest) -> ClassificationResult: ...

    async def aclassify(self, req: ClassificationRequest) -> ClassificationResult: ...
