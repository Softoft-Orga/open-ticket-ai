from unittest.mock import MagicMock

import pytest

from open_ticket_ai.base.ai_classification_services.classification_models import ClassificationResult
from open_ticket_ai.base.ai_classification_services.classification_service import ClassificationService
from open_ticket_ai.base.pipes.classification_pipe import ClassificationPipe
from open_ticket_ai.core.pipes.pipe_models import PipeConfig


@pytest.fixture
def classification_pipe_config():
    def _create_config(pipe_id: str, params: dict) -> PipeConfig:
        return PipeConfig(
            id=pipe_id,
            use="open_ticket_ai.base.pipes.classification_pipe.ClassificationPipe",
            params=params,
        )

    return _create_config


async def test_classification_pipe_successful_classification(
        logger_factory, empty_pipeline_context, classification_pipe_config
):
    mock_service = MagicMock(spec=ClassificationService)
    expected_result = ClassificationResult(label="urgent", confidence=0.95)
    mock_service.classify.return_value = expected_result

    config = classification_pipe_config(
        "test_classification_pipe",
        {"text": "This is urgent!", "model_name": "test-model", "api_token": "mock-api-key"},
    )

    pipe = ClassificationPipe(config=config, logger_factory=logger_factory, classification_service=mock_service)

    result = await pipe.process(empty_pipeline_context)

    assert result.succeeded is True
    assert not result.was_skipped
    assert result.data["label"] == "urgent"
    assert result.data["confidence"] == 0.95

    mock_service.classify.assert_called_once()


async def test_classification_pipe_with_null_api_token(
        logger_factory, empty_pipeline_context, classification_pipe_config
):
    mock_service = MagicMock(spec=ClassificationService)
    expected_result = ClassificationResult(label="normal", confidence=0.85)
    mock_service.classify.return_value = expected_result

    config = classification_pipe_config(
        "test_classification_pipe_no_token",
        {"text": "Test message", "model_name": "test-model"},
    )

    pipe = ClassificationPipe(config=config, logger_factory=logger_factory, classification_service=mock_service)

    result = await pipe.process(empty_pipeline_context)

    assert result.succeeded is True
    assert result.data["label"] == "normal"
    assert result.data["confidence"] == 0.85


@pytest.mark.parametrize(
    "text,model_name,expected_label,expected_confidence",
    [
        ("Critical system failure", "bert-classifier", "critical", 0.99),
        ("Normal operation", "bert-classifier", "normal", 0.75),
        ("Low priority task", "gpt-classifier", "low", 0.88),
    ],
)
async def test_classification_pipe_different_inputs(
        logger_factory,
        empty_pipeline_context,
        classification_pipe_config,
        text,
        model_name,
        expected_label,
        expected_confidence,
):
    mock_service = MagicMock(spec=ClassificationService)
    expected_result = ClassificationResult(label=expected_label, confidence=expected_confidence)
    mock_service.classify.return_value = expected_result

    config = classification_pipe_config(
        "test_classification_pipe_parametrized",
        {"text": text, "model_name": model_name},
    )

    pipe = ClassificationPipe(config=config, logger_factory=logger_factory, classification_service=mock_service)

    result = await pipe.process(empty_pipeline_context)

    assert result.succeeded is True
    assert result.data["label"] == expected_label
    assert result.data["confidence"] == expected_confidence

    mock_service.classify.assert_called_once()
