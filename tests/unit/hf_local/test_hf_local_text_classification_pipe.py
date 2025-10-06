import asyncio
import sys
import types
from unittest.mock import MagicMock

import pytest
from otai_hf_local.hf_local_text_classification_pipe import (
    HFLocalTextClassificationPipe,
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


def test_load_pipeline_initializes_transformers(monkeypatch):
    tokenizer_mock, model_mock, pipeline_factory_mock, pipeline_return = _install_fake_transformers(monkeypatch)

    pipeline = HFLocalTextClassificationPipe._load_pipeline("model-name", "hf-token")

    assert pipeline is pipeline_return
    tokenizer_mock.from_pretrained.assert_called_once_with("model-name", token="hf-token")
    model_mock.from_pretrained.assert_called_once_with("model-name", token="hf-token")
    pipeline_factory_mock.assert_called_once_with(
        "text-classification",
        model=model_mock.from_pretrained.return_value,
        tokenizer=tokenizer_mock.from_pretrained.return_value,
    )


def test_load_pipeline_caches_transformers_instances(monkeypatch):
    tokenizer_mock, model_mock, pipeline_factory_mock, _ = _install_fake_transformers(monkeypatch)

    first = HFLocalTextClassificationPipe._load_pipeline("cached-model", "secret")
    second = HFLocalTextClassificationPipe._load_pipeline("cached-model", "secret")

    assert first is second
    tokenizer_mock.from_pretrained.assert_called_once()
    model_mock.from_pretrained.assert_called_once()
    pipeline_factory_mock.assert_called_once()


def test_process_runs_pipeline_and_returns_top_result(monkeypatch):
    mock_pipeline = MagicMock(return_value=[{"label": "BUG", "score": 0.87}])
    mock_loader = MagicMock(return_value=mock_pipeline)
    monkeypatch.setattr(HFLocalTextClassificationPipe, "_load_pipeline", mock_loader)

    pipe = HFLocalTextClassificationPipe(
        {
            "id": "test-pipe",
            "model": "local-model",
            "token": "hf-token",
            "prompt": "Explain the issue",
        }
    )

    result = asyncio.run(pipe._process())

    mock_loader.assert_called_once_with("local-model", "hf-token")
    mock_pipeline.assert_called_once_with("Explain the issue", truncation=True)
    assert result.data == {"label": "BUG", "confidence": pytest.approx(0.87)}
    assert result.success is True
    assert result.failed is False


def test_process_handles_direct_dict_response(monkeypatch):
    mock_pipeline = MagicMock(return_value={"label": "QUESTION", "score": 0.42})
    monkeypatch.setattr(HFLocalTextClassificationPipe, "_load_pipeline", MagicMock(return_value=mock_pipeline))

    pipe = HFLocalTextClassificationPipe(
        {
            "id": "test-pipe",
            "model": "local-model",
            "token": None,
            "prompt": "Summarise the ticket",
        }
    )

    result = asyncio.run(pipe._process())

    mock_pipeline.assert_called_once_with("Summarise the ticket", truncation=True)
    assert result.data == {"label": "QUESTION", "confidence": pytest.approx(0.42)}
