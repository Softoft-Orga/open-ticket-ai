import pytest
from pydantic import ValidationError

from open_ticket_ai.base.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)


class TestClassificationService:
    def classify(self, _req: ClassificationRequest) -> ClassificationResult:
        return ClassificationResult(label="test_label", confidence=0.95)

    async def aclassify(self, _req: ClassificationRequest) -> ClassificationResult:
        return ClassificationResult(label="async_test_label", confidence=0.85)


def test_classification_service_sync_classify():
    service = TestClassificationService()
    request = ClassificationRequest(
        text="This is a test ticket",
        model_name="test_model",
        api_token=None,
    )

    result = service.classify(request)

    assert isinstance(result, ClassificationResult)
    assert result.label == "test_label"
    assert result.confidence == 0.95


async def test_classification_service_async_aclassify():
    service = TestClassificationService()
    request = ClassificationRequest(
        text="This is an async test ticket",
        model_name="test_model",
        api_token="fake-token-for-testing",  # noqa: S106
    )

    result = await service.aclassify(request)

    assert isinstance(result, ClassificationResult)
    assert result.label == "async_test_label"
    assert result.confidence == 0.85


def test_classification_service_protocol_compliance():
    service = TestClassificationService()

    assert hasattr(service, "classify")
    assert hasattr(service, "aclassify")
    assert callable(service.classify)
    assert callable(service.aclassify)


def test_classification_request_invalid_text_type():
    with pytest.raises(ValidationError):
        ClassificationRequest(
            text=123,  # type: ignore[arg-type]
            model_name="test_model",
        )


def test_classification_request_missing_required_fields():
    with pytest.raises(ValidationError):
        ClassificationRequest(text="test")  # type: ignore[call-arg]


def test_classification_result_invalid_confidence_type():
    with pytest.raises(ValidationError):
        ClassificationResult(label="test", confidence="invalid")  # type: ignore[arg-type]


def test_classification_result_missing_required_fields():
    with pytest.raises(ValidationError):
        ClassificationResult(label="test")  # type: ignore[call-arg]
