from open_ticket_ai.core.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from open_ticket_ai.core.ai_classification_services.classification_service import ClassificationService

SYNC_CONFIDENCE = 0.95
ASYNC_CONFIDENCE = 0.85


class TestClassificationService(ClassificationService):
    def classify(self, _req: ClassificationRequest) -> ClassificationResult:
        return ClassificationResult(label="test_label", confidence=SYNC_CONFIDENCE)

    async def aclassify(self, _req: ClassificationRequest) -> ClassificationResult:
        return ClassificationResult(label="async_test_label", confidence=ASYNC_CONFIDENCE)


def test_classification_service_protocol_compliance(empty_injectable_config, logger_factory):
    service = TestClassificationService(empty_injectable_config, logger_factory)
    assert isinstance(service, ClassificationService)


def test_classification_service_sync_classify(empty_injectable_config, logger_factory):
    service = TestClassificationService(empty_injectable_config, logger_factory)
    request = ClassificationRequest(
        text="This is a test ticket",
        model_name="test_model",
    )

    result = service.classify(request)

    assert isinstance(result, ClassificationResult)
    assert result.label == "test_label"
    assert result.confidence == SYNC_CONFIDENCE


async def test_classification_service_async_aclassify(empty_injectable_config, logger_factory):
    service = TestClassificationService(empty_injectable_config, logger_factory)
    request = ClassificationRequest(
        text="This is an async test ticket",
        model_name="test_model",
    )

    result = await service.aclassify(request)

    assert isinstance(result, ClassificationResult)
    assert result.label == "async_test_label"
    assert result.confidence == ASYNC_CONFIDENCE
