from typing import Protocol, runtime_checkable

from open_ticket_ai.base.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)


@runtime_checkable
class ClassificationService(Protocol):
    def classify(self, req: ClassificationRequest) -> ClassificationResult: ...

    async def aclassify(self, req: ClassificationRequest) -> ClassificationResult: ...
