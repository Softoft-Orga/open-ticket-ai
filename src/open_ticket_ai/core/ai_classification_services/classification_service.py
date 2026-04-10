from abc import ABC, abstractmethod

from open_ticket_ai.core.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)


class ClassificationService(ABC):
    @abstractmethod
    def classify(self, req: ClassificationRequest) -> ClassificationResult: ...

    @abstractmethod
    async def aclassify(self, req: ClassificationRequest) -> ClassificationResult: ...
