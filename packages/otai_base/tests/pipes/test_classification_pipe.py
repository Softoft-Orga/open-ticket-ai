from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest
from open_ticket_ai.core.ai_classification_services.classification_models import ClassificationResult
from open_ticket_ai.core.ai_classification_services.classification_service import ClassificationService
from open_ticket_ai.core.pipes.pipe_models import PipeConfig

from otai_base.pipes.classification_pipe import ClassificationPipe

CONFIDENCE_URGENT = 0.95
CONFIDENCE_NORMAL = 0.85
CONFIDENCE_CRITICAL = 0.99
CONFIDENCE_BASELINE = 0.75
CONFIDENCE_LOW = 0.88


@dataclass(frozen=True)
class ClassificationScenario:
    text: str
    model_name: str
    expected_label: str
    expected_confidence: float


SCENARIOS: tuple[ClassificationScenario, ...] = (
    ClassificationScenario("Critical system failure", "bert-classifier", "critical", CONFIDENCE_CRITICAL),
    ClassificationScenario("Normal operation", "bert-classifier", "normal", CONFIDENCE_BASELINE),
    ClassificationScenario("Low priority task", "gpt-classifier", "low", CONFIDENCE_LOW),
)


@pytest.fixture
def classification_pipe_config():
    def _create_config(pipe_id: str, params: dict) -> PipeConfig:
        return PipeConfig(
            id=pipe_id,
            use="open_ticket_ai.otai_base.pipes.classification_pipe.ClassificationPipe",
            params=params,
        )

    return _create_config


async def test_classification_pipe_successful_classification(
    logger_factory, empty_pipeline_context, classification_pipe_config
):
    mock_service = MagicMock(spec=ClassificationService)
    expected_result = ClassificationResult(label="urgent", confidence=CONFIDENCE_URGENT)
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
    assert result.data["confidence"] == CONFIDENCE_URGENT

    mock_service.classify.assert_called_once()


async def test_classification_pipe_with_null_api_token(
    logger_factory, empty_pipeline_context, classification_pipe_config
):
    mock_service = MagicMock(spec=ClassificationService)
    expected_result = ClassificationResult(label="normal", confidence=CONFIDENCE_NORMAL)
    mock_service.classify.return_value = expected_result

    config = classification_pipe_config(
        "test_classification_pipe_no_token",
        {"text": "Test message", "model_name": "test-model"},
    )

    pipe = ClassificationPipe(config=config, logger_factory=logger_factory, classification_service=mock_service)

    result = await pipe.process(empty_pipeline_context)

    assert result.succeeded is True
    assert result.data["label"] == "normal"
    assert result.data["confidence"] == CONFIDENCE_NORMAL


@pytest.mark.parametrize("scenario", SCENARIOS)
async def test_classification_pipe_different_inputs(
    logger_factory,
    empty_pipeline_context,
    classification_pipe_config,
    scenario: ClassificationScenario,
):
    mock_service = MagicMock(spec=ClassificationService)
    expected_result = ClassificationResult(
        label=scenario.expected_label,
        confidence=scenario.expected_confidence,
    )
    mock_service.classify.return_value = expected_result

    config = classification_pipe_config(
        "test_classification_pipe_parametrized",
        {"text": scenario.text, "model_name": scenario.model_name},
    )

    pipe = ClassificationPipe(config=config, logger_factory=logger_factory, classification_service=mock_service)

    result = await pipe.process(empty_pipeline_context)

    assert result.succeeded is True
    assert result.data["label"] == scenario.expected_label
    assert result.data["confidence"] == scenario.expected_confidence

    mock_service.classify.assert_called_once()
