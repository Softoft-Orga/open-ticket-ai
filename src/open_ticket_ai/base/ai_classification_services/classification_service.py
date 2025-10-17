from abc import ABC, abstractmethod

import anyio

from open_ticket_ai.base.ai_classification_services.classification_models import ClassificationRequest, \
    ClassificationResult


class ClassificationService(ABC):
    @abstractmethod
    def classify(self, req: ClassificationRequest) -> ClassificationResult: ...

    async def aclassify(self, req: ClassificationRequest) -> ClassificationResult:
        return await anyio.to_thread.run_sync(self.classify, req)
