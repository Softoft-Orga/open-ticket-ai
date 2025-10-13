import asyncio
import sys
import types
from unittest.mock import MagicMock

import pytest
from open_ticket_ai.base.loggers.stdlib_logging_adapter import StdlibLoggerFactory
from packages.otai_hf_local.src.otai_hf_local import HFLocalTextClassificationPipe
from packages.otai_hf_local.src.otai_hf_local.hf_local_text_classification_pipe import (
    HFLocalTextClassificationParams,
    HFLocalTextClassificationPipeConfig,
)


@pytest.fixture(autouse=True)
def clear_load_pipeline_cache():
    HFLocalTextClassificationPipe._load_pipeline.cache_clear()
    yield
    HFLocalTextClassificationPipe._load_pipeline.cache_clear()


def _install_fake_transformers(monkeypatch, *, pipeline_return="pipeline"):
    mock_tokenizer_instance = MagicMock(name="tokenizer_instance")
    mock_model_instance = MagicMock(name="model_instance")

    mock_auto_tokenizer = MagicMock(name="AutoTokenizer")
    mock_auto_tokenizer.from_pretrained.return_value = mock_tokenizer_instance

    mock_auto_model = MagicMock(name="AutoModelForSequenceClassification")
    mock_auto_model.from_pretrained.return_value = mock_model_instance

    mock_pipeline_factory = MagicMock(name="pipeline", return_value=pipeline_return)

    fake_transformers = types.SimpleNamespace(
        AutoTokenizer=mock_auto_tokenizer,
        AutoModelForSequenceClassification=mock_auto_model,
        pipeline=mock_pipeline_factory,
    )

    monkeypatch.setitem(sys.modules, "transformers", fake_transformers)

    return mock_auto_tokenizer, mock_auto_model, mock_pipeline_factory, pipeline_return


def test_process_runs_pipeline_and_returns_top_result(monkeypatch):
    mock_pipeline = MagicMock(return_value=[{"label": "BUG", "score": 0.87}])
    mock_loader = MagicMock(return_value=mock_pipeline)
    monkeypatch.setattr(HFLocalTextClassificationPipe, "_load_pipeline", mock_loader)

    pipe = HFLocalTextClassificationPipe(
        HFLocalTextClassificationPipeConfig(
            id="test-pipe",
            params=HFLocalTextClassificationParams(model="local-model", token="hf-token", prompt="Explain the issue"),
        ),
        logger_factory=StdlibLoggerFactory(),
    )

    result = asyncio.run(pipe._process())

    mock_loader.assert_called_once_with("local-model", "hf-token")
    mock_pipeline.assert_called_once_with("Explain the issue", truncation=True)
    assert result.data.model_dump() == {"label": "BUG", "confidence": pytest.approx(0.87)}
    assert result.success is True
    assert result.failed is False


def test_process_handles_direct_dict_response(monkeypatch, logger_factory):
    mock_pipeline = MagicMock(return_value={"label": "QUESTION", "score": 0.42})
    monkeypatch.setattr(HFLocalTextClassificationPipe, "_load_pipeline", MagicMock(return_value=mock_pipeline))

    from packages.otai_hf_local.src.otai_hf_local.hf_local_text_classification_pipe import (
        HFLocalTextClassificationPipeConfig,
    )

    pipe_config = HFLocalTextClassificationPipeConfig(
        id="test-pipe",
        params=HFLocalTextClassificationParams(model="local-model", token=None, prompt="Summarise the ticket"),
    )
    pipe = HFLocalTextClassificationPipe(pipe_config, logger_factory)

    result = asyncio.run(pipe._process())

    mock_pipeline.assert_called_once_with("Summarise the ticket", truncation=True)
    assert result.data.model_dump() == {"label": "QUESTION", "confidence": pytest.approx(0.42)}
