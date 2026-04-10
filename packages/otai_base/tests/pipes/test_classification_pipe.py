from unittest.mock import MagicMock

import pytest
from open_ticket_ai.core.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from open_ticket_ai.core.ai_classification_services.classification_service import ClassificationService
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult

from otai_base.pipes.classification_pipe import ClassificationPipe

pytestmark = [pytest.mark.unit]


async def test_classification_pipe_static_text():
    mock_service = MagicMock(spec=ClassificationService)
    expected = ClassificationResult(label="urgent", confidence=0.95)
    mock_service.classify.return_value = expected

    pipe = ClassificationPipe(
        "classify",
        mock_service,
        "test-model",
        "Hello world",
        api_token="tok",
    )
    result = await pipe.process(PipeContext.empty())

    assert result.succeeded
    assert result.data["label"] == "urgent"
    assert result.data["confidence"] == 0.95
    mock_service.classify.assert_called_once()
    req = mock_service.classify.call_args[0][0]
    assert isinstance(req, ClassificationRequest)
    assert req.text == "Hello world"
    assert req.model_name == "test-model"
    assert req.api_token == "tok"


async def test_classification_pipe_callable_get_text():
    mock_service = MagicMock(spec=ClassificationService)
    mock_service.classify.return_value = ClassificationResult(label="low", confidence=0.5)

    ctx = PipeContext.empty().with_pipe_result(
        "upstream",
        PipeResult.success(data={"body": "dynamic text"}),
    )

    pipe = ClassificationPipe(
        "classify",
        mock_service,
        "m",
        lambda c: c.get_result("upstream", "body"),
    )
    result = await pipe.process(ctx)

    assert result.succeeded
    assert result.data["label"] == "low"
    mock_service.classify.assert_called_once()
    req = mock_service.classify.call_args[0][0]
    assert isinstance(req, ClassificationRequest)
    assert req.text == "dynamic text"
    assert req.model_name == "m"
    assert req.api_token is None
