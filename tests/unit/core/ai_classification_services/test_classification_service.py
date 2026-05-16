import pytest
from open_ticket_ai.core.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from open_ticket_ai.core.ai_classification_services.classification_service import ClassificationService

pytestmark = [pytest.mark.unit]


class EchoClassificationService(ClassificationService):
    def classify(self, req: ClassificationRequest) -> ClassificationResult:
        return ClassificationResult(label=f"sync:{req.text[:8]}", confidence=0.9)

    async def aclassify(self, req: ClassificationRequest) -> ClassificationResult:
        return ClassificationResult(label=f"async:{req.model_name}", confidence=0.8)


def test_concrete_classification_service_classify():
    svc = EchoClassificationService()
    req = ClassificationRequest(text="hello world", model_name="m1")
    out = svc.classify(req)
    assert isinstance(out, ClassificationResult)
    assert out.label == "sync:hello wo"
    assert out.confidence == 0.9


async def test_concrete_classification_service_aclassify():
    svc = EchoClassificationService()
    req = ClassificationRequest(text="x", model_name="my-model")
    out = await svc.aclassify(req)
    assert isinstance(out, ClassificationResult)
    assert out.label == "async:my-model"
    assert out.confidence == 0.8
