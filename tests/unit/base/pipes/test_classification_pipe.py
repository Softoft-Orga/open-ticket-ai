from unittest.mock import MagicMock

import pytest

from open_ticket_ai.base.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from open_ticket_ai.base.ai_classification_services.classification_service import ClassificationService
from open_ticket_ai.base.pipes.classification_pipe import ClassificationPipe
from open_ticket_ai.core.pipes.pipe_models import PipeConfig


async def test_classification_pipe_successful_classification(logger_factory, empty_pipeline_context):
    mock_service = MagicMock(spec=ClassificationService)
    expected_result = ClassificationResult(label="urgent", confidence=0.95)
    mock_service.classify.return_value = expected_result

    config = PipeConfig(
        id="test_classification_pipe",
        use="open_ticket_ai.base.pipes.classification_pipe.ClassificationPipe",
        params={"text": "This is urgent!", "model_name": "test-model", "api_token": "mock-api-key"},
    )

    pipe = ClassificationPipe(config=config, logger_factory=logger_factory, classification_service=mock_service)

    result = await pipe.process(empty_pipeline_context)

    assert result.succeeded is True
    assert not result.was_skipped
    assert result.data["label"] == "urgent"
    assert result.data["confidence"] == 0.95

    mock_service.classify.assert_called_once()
    call_args = mock_service.classify.call_args[0][0]
    assert isinstance(call_args, ClassificationRequest)
    assert call_args.text == "This is urgent!"
    assert call_args.model_name == "test-model"
    assert call_args.api_token == "mock-api-key"


async def test_classification_pipe_with_null_api_token(logger_factory, empty_pipeline_context):
    mock_service = MagicMock(spec=ClassificationService)
    expected_result = ClassificationResult(label="normal", confidence=0.85)
    mock_service.classify.return_value = expected_result

    config = PipeConfig(
        id="test_classification_pipe_no_token",
        use="open_ticket_ai.base.pipes.classification_pipe.ClassificationPipe",
        params={"text": "Test message", "model_name": "test-model"},
    )

    pipe = ClassificationPipe(config=config, logger_factory=logger_factory, classification_service=mock_service)

    result = await pipe.process(empty_pipeline_context)

    assert result.succeeded is True
    assert result.data["label"] == "normal"
    assert result.data["confidence"] == 0.85

    call_args = mock_service.classify.call_args[0][0]
    assert call_args.api_token is None


async def test_classification_pipe_service_raises_exception(logger_factory, empty_pipeline_context):
    mock_service = MagicMock(spec=ClassificationService)
    mock_service.classify.side_effect = RuntimeError("Classification service unavailable")

    config = PipeConfig(
        id="test_classification_pipe_error",
        use="open_ticket_ai.base.pipes.classification_pipe.ClassificationPipe",
        params={"text": "Test", "model_name": "test-model"},
    )

    pipe = ClassificationPipe(config=config, logger_factory=logger_factory, classification_service=mock_service)

    with pytest.raises(RuntimeError, match="Classification service unavailable"):
        await pipe.process(empty_pipeline_context)


@pytest.mark.parametrize(
    "text,model_name,expected_label,expected_confidence",
    [
        ("Critical system failure", "bert-classifier", "critical", 0.99),
        ("Normal operation", "bert-classifier", "normal", 0.75),
        ("Low priority task", "gpt-classifier", "low", 0.88),
    ],
)
async def test_classification_pipe_different_inputs(
    logger_factory, empty_pipeline_context, text, model_name, expected_label, expected_confidence
):
    mock_service = MagicMock(spec=ClassificationService)
    expected_result = ClassificationResult(label=expected_label, confidence=expected_confidence)
    mock_service.classify.return_value = expected_result

    config = PipeConfig(
        id="test_classification_pipe_parametrized",
        use="open_ticket_ai.base.pipes.classification_pipe.ClassificationPipe",
        params={"text": text, "model_name": model_name},
    )

    pipe = ClassificationPipe(config=config, logger_factory=logger_factory, classification_service=mock_service)

    result = await pipe.process(empty_pipeline_context)

    assert result.succeeded is True
    assert result.data["label"] == expected_label
    assert result.data["confidence"] == expected_confidence

    call_args = mock_service.classify.call_args[0][0]
    assert call_args.text == text
    assert call_args.model_name == model_name
