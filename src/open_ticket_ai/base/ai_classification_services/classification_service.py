from abc import ABC, abstractmethod

from open_ticket_ai.base.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)


class ClassificationService(ABC):
    @abstractmethod
    def classify(self, req: ClassificationRequest) -> ClassificationResult: ...

    async def aclassify(self, req: ClassificationRequest) -> ClassificationResult: ...
