from unittest.mock import MagicMock

import pytest
from open_ticket_ai import InjectableConfig
from open_ticket_ai.core.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from packages.otai_hf_local.src.otai_hf_local.hf_classification_service import HFClassificationService


def test_classify_forwards_request_token_and_returns_result(logger_factory):
    config = InjectableConfig(id="test-hf-service")
    mock_pipeline = MagicMock()
    mock_get_pipeline = MagicMock(return_value=mock_pipeline)
    mock_pipeline.return_value = [{"label": "test-label", "score": 0.99}]
    service = HFClassificationService(config, logger_factory, get_pipeline=mock_get_pipeline)

    request = ClassificationRequest(
        text="This is a test text",
        model_name="test-model",
        api_token="test-token",
    )

    result = service.classify(request)

    assert isinstance(result, ClassificationResult)
    assert result.label == "test-label"
    assert result.confidence == 0.99  # noqa: PLR2004
    mock_get_pipeline.assert_called_once_with("test-model", "test-token")
    mock_pipeline.assert_called_once_with("This is a test text", truncation=True)


def test_classify_uses_configured_token_when_request_missing(logger_factory):
    config = InjectableConfig(id="test-hf-service", params={"api_token": "configured-token"})
    mock_pipeline = MagicMock(return_value=[{"label": "config-label", "score": 0.75}])
    mock_get_pipeline = MagicMock(return_value=mock_pipeline)
    service = HFClassificationService(config, logger_factory, get_pipeline=mock_get_pipeline)

    request = ClassificationRequest(text="Configured token", model_name="config-model", api_token=None)

    result = service.classify(request)

    assert result.label == "config-label"
    assert result.confidence == 0.75  # noqa: PLR2004
    mock_get_pipeline.assert_called_once_with("config-model", "configured-token")
    mock_pipeline.assert_called_once_with("Configured token", truncation=True)


@pytest.mark.asyncio
async def test_aclassify_returns_correct_result(logger_factory):
    config = InjectableConfig(id="test-hf-service")
    mock_pipeline = MagicMock()
    mock_pipeline.return_value = [{"label": "async-label", "score": 0.95}]
    mock_get_pipeline = MagicMock(return_value=mock_pipeline)

    service = HFClassificationService(config, logger_factory, get_pipeline=mock_get_pipeline)

    request = ClassificationRequest(
        text="This is an async test",
        model_name="async-model",
        api_token=None,
    )

    result = await service.aclassify(request)

    assert isinstance(result, ClassificationResult)
    assert result.label == "async-label"
    assert result.confidence == 0.95  # noqa: PLR2004
    mock_get_pipeline.assert_called_once_with("async-model", None)
    mock_pipeline.assert_called_once_with("This is an async test", truncation=True)


def test_classify_raises_error_when_pipeline_fails(logger_factory):
    config = InjectableConfig(id="test-hf-service")
    mock_pipeline = MagicMock()
    mock_pipeline.side_effect = ValueError("Pipeline error")
    mock_get_pipeline = MagicMock(return_value=mock_pipeline)

    service = HFClassificationService(config, logger_factory, get_pipeline=mock_get_pipeline)

    request = ClassificationRequest(
        text="This will fail",
        model_name="error-model",
        api_token=None,
    )

    with pytest.raises(ValueError, match="Pipeline error"):
        service.classify(request)


def test_classify_raises_error_when_no_result(logger_factory):
    config = InjectableConfig(id="test-hf-service")
    mock_pipeline = MagicMock()
    mock_pipeline.return_value = []
    mock_get_pipeline = MagicMock(return_value=mock_pipeline)

    service = HFClassificationService(config, logger_factory, get_pipeline=mock_get_pipeline)

    request = ClassificationRequest(
        text="This returns empty",
        model_name="empty-model",
        api_token=None,
    )

    with pytest.raises(ValueError, match="No classification result returned from HuggingFace pipeline"):
        service.classify(request)


def test_classify_raises_error_when_non_list_result(logger_factory):
    config = InjectableConfig(id="test-hf-service")
    mock_pipeline = MagicMock()
    mock_pipeline.return_value = {"label": "bad", "score": 0.5}
    mock_get_pipeline = MagicMock(return_value=mock_pipeline)

    service = HFClassificationService(config, logger_factory, get_pipeline=mock_get_pipeline)

    request = ClassificationRequest(
        text="This returns non-list",
        model_name="bad-model",
        api_token=None,
    )

    with pytest.raises(TypeError, match="HuggingFace pipeline returned a non-list result"):
        service.classify(request)
