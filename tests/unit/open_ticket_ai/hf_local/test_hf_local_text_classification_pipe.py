"""Unit tests for :mod:`open_ticket_ai.hf_local.hf_local_text_classification_pipe`."""

from __future__ import annotations

import asyncio
import logging
import sys
import types
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))

if "pydantic" not in sys.modules:
    pydantic_stub = types.ModuleType("pydantic")

    class _BaseModel:  # pragma: no cover - simple shim
        def model_dump(self):
            return self.__dict__.copy()

    def _field(*_, default=None, default_factory=None, **__):  # pragma: no cover - simple shim
        if default_factory is not None:
            return default_factory()
        return default

    pydantic_stub.BaseModel = _BaseModel
    pydantic_stub.Field = _field
    sys.modules["pydantic"] = pydantic_stub

if "jinja2" not in sys.modules:
    jinja_stub = types.ModuleType("jinja2")

    class _Undefined:  # pragma: no cover - simple shim
        def __init__(self, *args, **kwargs):
            self._undefined_name = "undefined"

    class _UndefinedError(Exception):
        pass

    class _Template:  # pragma: no cover - simple shim
        def __init__(self, template_str: str):
            self._template_str = template_str

        def render(self, _scope):
            return self._template_str

    class _SandboxedEnvironment:  # pragma: no cover - simple shim
        def __init__(self, *args, **kwargs):
            pass

        def from_string(self, template_str: str):
            return _Template(template_str)

    sandbox_module = types.ModuleType("jinja2.sandbox")
    sandbox_module.SandboxedEnvironment = _SandboxedEnvironment

    jinja_stub.Undefined = _Undefined
    jinja_stub.UndefinedError = _UndefinedError
    jinja_stub.sandbox = sandbox_module

    sys.modules["jinja2"] = jinja_stub
    sys.modules["jinja2.sandbox"] = sandbox_module

pipe_configs_module = sys.modules.get("open_ticket_ai.base_extensions.pipe_configs")
if pipe_configs_module is None:
    import importlib

    pipe_configs_module = importlib.import_module("open_ticket_ai.base_extensions.pipe_configs")

if not hasattr(pipe_configs_module, "HFLocalAIInferenceServiceConfig"):

    class _StubHFLocalConfig:  # pragma: no cover - simple shim
        pass

    pipe_configs_module.HFLocalAIInferenceServiceConfig = _StubHFLocalConfig

from open_ticket_ai.hf_local.hf_local_text_classification_pipe import HFLocalTextClassificationPipe


@dataclass
class _RenderedConfig:
    """Minimal rendered configuration stub used for testing."""

    name: str = "hf_local_service"
    use: str = "open_ticket_ai.hf_local.hf_local_text_classification_pipe.HFLocalAIInferenceService"
    when: bool = True
    prompt: str = "Classify this text"
    hf_model: str = "distilbert-base-uncased-finetuned-sst-2-english"
    hf_token_env_var: str | None = "HF_TOKEN"


@dataclass
class _RawConfig:
    """Raw configuration stub that mimics the behaviour of :class:`RawPipeConfig`."""

    rendered: _RenderedConfig = field(default_factory=_RenderedConfig)
    steps: list[Any] = field(default_factory=list)

    def render(self, _context: Any) -> _RenderedConfig:
        return self.rendered


@pytest.fixture()
def service() -> HFLocalTextClassificationPipe:
    class _TestableHFLocalService(HFLocalTextClassificationPipe):
        @staticmethod
        def get_raw_config_model_type():  # pragma: no cover - testing shim
            return _RawConfig

    return _TestableHFLocalService(_RawConfig())


class TestGetToken:
    def test_returns_none_when_env_var_missing(
        self, service: HFLocalTextClassificationPipe, caplog: pytest.LogCaptureFixture
    ) -> None:
        service.config.hf_token_env_var = None
        with caplog.at_level(logging.WARNING):
            token = service._get_token()
        assert token is None
        assert "No hf_token_env_var provided" in caplog.text

    def test_reads_token_from_environment(self, service: HFLocalTextClassificationPipe) -> None:
        with pytest.MonkeyPatch.context() as monkeypatch:
            monkeypatch.setenv("HF_TOKEN", "hf_secret")
            token = service._get_token()
        assert token == "hf_secret"

    def test_warns_when_token_looks_invalid(
        self, service: HFLocalTextClassificationPipe, caplog: pytest.LogCaptureFixture
    ) -> None:
        with pytest.MonkeyPatch.context() as monkeypatch, caplog.at_level(logging.WARNING):
            monkeypatch.setenv("HF_TOKEN", "not_a_valid_token")
            token = service._get_token()
        assert token == "not_a_valid_token"
        assert "does not appear to be a valid HuggingFace token" in caplog.text

    def test_missing_env_value_triggers_warning(
        self, service: HFLocalTextClassificationPipe, caplog: pytest.LogCaptureFixture
    ) -> None:
        with pytest.MonkeyPatch.context() as monkeypatch, caplog.at_level(logging.WARNING):
            monkeypatch.delenv("HF_TOKEN", raising=False)
            token = service._get_token()
        assert token is None
        assert "is not set or empty" in caplog.text


class TestProcess:
    def test_process_loads_pipeline_when_missing(self, service: HFLocalTextClassificationPipe) -> None:
        rendered = service.config
        rendered.prompt = "Classify this sample"
        mock_pipeline = MagicMock(return_value=[{"label": "POSITIVE", "score": 0.95}])
        service._load_pipeline = MagicMock(return_value=mock_pipeline)  # type: ignore[assignment]

        with pytest.MonkeyPatch.context() as monkeypatch:
            monkeypatch.setenv("HF_TOKEN", "hf_secret")
            result = asyncio.run(service._process(rendered))

        assert result == {"label": "POSITIVE", "confidence": 0.95}
        service._load_pipeline.assert_called_once_with(rendered.hf_model, "hf_secret")  # type: ignore[attr-defined]
        mock_pipeline.assert_called_once_with("Classify this sample", truncation=True)
        assert service._pipeline is mock_pipeline

    def test_process_reuses_cached_pipeline(self, service: HFLocalTextClassificationPipe) -> None:
        rendered = service.config
        rendered.prompt = "Classify cached"
        mock_pipeline = MagicMock(return_value=[{"label": "NEGATIVE", "score": 0.4}])
        service._pipeline = mock_pipeline
        service._load_pipeline = MagicMock()  # type: ignore[assignment]

        result = asyncio.run(service._process(rendered))

        assert result == {"label": "NEGATIVE", "confidence": 0.4}
        service._load_pipeline.assert_not_called()  # type: ignore[attr-defined]
        mock_pipeline.assert_called_once_with("Classify cached", truncation=True)

    def test_process_accepts_dict_response(self, service: HFLocalTextClassificationPipe) -> None:
        rendered = service.config
        rendered.prompt = "Dict response"
        service._pipeline = MagicMock(return_value={"label": "POSITIVE", "score": "0.7"})

        result = asyncio.run(service._process(rendered))

        assert result == {"label": "POSITIVE", "confidence": 0.7}

    def test_process_raises_on_empty_prompt(self, service: HFLocalTextClassificationPipe) -> None:
        rendered = service.config
        rendered.prompt = ""
        service._pipeline = MagicMock()

        with pytest.raises(ValueError, match="No input prompt provided in config"):
            asyncio.run(service._process(rendered))
        service._pipeline.assert_not_called()
