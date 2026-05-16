from unittest.mock import MagicMock

import pytest
from open_ticket_ai.core.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)

from open_ticket_ai.hf_local.hf_classification_service import HFClassificationService

pytestmark = [pytest.mark.unit]


def test_classify_uses_injected_pipeline():
    mock_pipeline = MagicMock(return_value=[{"label": "test-label", "score": 0.99}])
    get_pipeline = MagicMock(return_value=mock_pipeline)
    service = HFClassificationService(api_token=None, get_pipeline=get_pipeline)

    request = ClassificationRequest(
        text="This is a test text",
        model_name="test-model",
        api_token="test-token",
    )

    result = service.classify(request)

    assert isinstance(result, ClassificationResult)
    assert result.label == "test-label"
    assert result.confidence == 0.99  # noqa: PLR2004
    get_pipeline.assert_called_once_with("test-model", "test-token")
    mock_pipeline.assert_called_once_with("This is a test text", truncation=True)


def test_classify_falls_back_to_service_api_token():
    mock_pipeline = MagicMock(return_value=[{"label": "config-label", "score": 0.75}])
    get_pipeline = MagicMock(return_value=mock_pipeline)
    service = HFClassificationService(api_token="configured-token", get_pipeline=get_pipeline)

    request = ClassificationRequest(text="Configured token", model_name="config-model", api_token=None)

    result = service.classify(request)

    assert result.label == "config-label"
    assert result.confidence == 0.75  # noqa: PLR2004
    get_pipeline.assert_called_once_with("config-model", "configured-token")


async def test_aclassify_delegates_to_classify():
    mock_pipeline = MagicMock(return_value=[{"label": "async-label", "score": 0.95}])
    get_pipeline = MagicMock(return_value=mock_pipeline)
    service = HFClassificationService(api_token=None, get_pipeline=get_pipeline)

    request = ClassificationRequest(
        text="This is an async test",
        model_name="async-model",
        api_token=None,
    )

    result = await service.aclassify(request)

    assert isinstance(result, ClassificationResult)
    assert result.label == "async-label"
    assert result.confidence == 0.95  # noqa: PLR2004
    get_pipeline.assert_called_once_with("async-model", None)


def test_classify_raises_when_pipeline_errors():
    mock_pipeline = MagicMock(side_effect=ValueError("Pipeline error"))
    service = HFClassificationService(get_pipeline=MagicMock(return_value=mock_pipeline))

    request = ClassificationRequest(text="This will fail", model_name="error-model", api_token=None)

    with pytest.raises(ValueError, match="Pipeline error"):
        service.classify(request)


def test_classify_raises_when_pipeline_returns_empty():
    mock_pipeline = MagicMock(return_value=[])
    service = HFClassificationService(get_pipeline=MagicMock(return_value=mock_pipeline))

    request = ClassificationRequest(text="This returns empty", model_name="empty-model", api_token=None)

    with pytest.raises(ValueError, match="No classification result returned from HuggingFace pipeline"):
        service.classify(request)


def test_classify_raises_when_pipeline_returns_non_list():
    mock_pipeline = MagicMock(return_value={"label": "bad", "score": 0.5})
    service = HFClassificationService(get_pipeline=MagicMock(return_value=mock_pipeline))

    request = ClassificationRequest(text="This returns non-list", model_name="bad-model", api_token=None)

    with pytest.raises(TypeError, match="HuggingFace pipeline returned a non-list result"):
        service.classify(request)
