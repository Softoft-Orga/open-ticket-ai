"""
Pytest tests for HFLocalAiInferencePipe.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.base_extensions.pipe_implementations.hf_local_ai_inference_pipe import HFLocalAiInferencePipe
from open_ticket_ai.base_extensions.pipe_implementations.pipe_configs import HFLocalAiInferencePipeConfig


@pytest.fixture
def sample_config():
    """Create a sample HFLocalAiInferencePipeConfig for testing."""
    return HFLocalAiInferencePipeConfig(
        name="test_hf_inference",
        use="open_ticket_ai.extensions.HFLocalAiInferencePipe",
        prompt="Test prompt for classification",
        hf_model="distilbert-base-uncased-finetuned-sst-2-english",
        hf_token_env_var="HF_TOKEN",
    )


@pytest.fixture
def sample_context():
    """Create a sample PipelineContext for testing."""
    return PipelineContext(pipes={}, config={})


@pytest.fixture
def mock_pipeline():
    """Create a mock transformers pipeline."""
    mock_pipe = MagicMock()
    mock_pipe.return_value = [{"label": "POSITIVE", "score": 0.9998}]
    return mock_pipe


class TestHFLocalAiInferencePipe:
    """Test cases for HFLocalAiInferencePipe."""

    def test_init(self, sample_config):
        """Test pipe initialization."""
        pipe = HFLocalAiInferencePipe(sample_config)
        assert pipe.config == sample_config
        assert pipe._pipeline is None

    def test_get_token_with_valid_env_var(self, sample_config):
        """Test _get_token with valid environment variable."""
        pipe = HFLocalAiInferencePipe(sample_config)

        with patch.dict(os.environ, {"HF_TOKEN": "hf_test_token_123"}):
            token = pipe._get_token()
            assert token == "hf_test_token_123"

    def test_get_token_with_missing_env_var(self, sample_config):
        """Test _get_token with missing environment variable."""
        pipe = HFLocalAiInferencePipe(sample_config)

        with patch.dict(os.environ, {}, clear=True):
            token = pipe._get_token()
            assert token is None

    def test_get_token_with_empty_env_var(self, sample_config):
        """Test _get_token with empty environment variable."""
        pipe = HFLocalAiInferencePipe(sample_config)

        with patch.dict(os.environ, {"HF_TOKEN": ""}):
            token = pipe._get_token()
            assert token is None

    def test_get_token_with_invalid_token_format(self, sample_config):
        """Test _get_token with invalid token format (should still return it)."""
        pipe = HFLocalAiInferencePipe(sample_config)

        with patch.dict(os.environ, {"HF_TOKEN": "invalid_token"}):
            token = pipe._get_token()
            assert token == "invalid_token"

    def test_get_token_no_env_var_configured(self, sample_config):
        """Test _get_token when no env var is configured."""
        config = sample_config.model_copy(update={"hf_token_env_var": ""})
        pipe = HFLocalAiInferencePipe(config)

        token = pipe._get_token()
        assert token is None

    @patch(
        "open_ticket_ai.extensions.pipe_implementations.hf_local_ai_inference_pipe.HFLocalAiInferencePipe._load_pipeline"
    )
    async def test_process_success(self, mock_load_pipeline, sample_config, sample_context, mock_pipeline):
        """Test successful processing."""
        mock_load_pipeline.return_value = mock_pipeline
        pipe = HFLocalAiInferencePipe(sample_config)

        result = await pipe._process(sample_context)

        assert result == {"label": "POSITIVE", "confidence": 0.9998}
        mock_load_pipeline.assert_called_once()
        mock_pipeline.assert_called_once_with("Test prompt for classification", truncation=True)

    @patch(
        "open_ticket_ai.extensions.pipe_implementations.hf_local_ai_inference_pipe.HFLocalAiInferencePipe._load_pipeline"
    )
    async def test_process_with_cached_pipeline(self, mock_load_pipeline, sample_config, sample_context, mock_pipeline):
        """Test processing with already cached pipeline."""
        pipe = HFLocalAiInferencePipe(sample_config)
        pipe._pipeline = mock_pipeline

        result = await pipe._process(sample_context)

        assert result == {"label": "POSITIVE", "confidence": 0.9998}
        mock_load_pipeline.assert_not_called()
        mock_pipeline.assert_called_once_with("Test prompt for classification", truncation=True)

    async def test_process_empty_prompt(self, sample_config, sample_context):
        """Test processing with empty prompt."""
        config = sample_config.model_copy(update={"prompt": ""})
        pipe = HFLocalAiInferencePipe(config)

        with pytest.raises(ValueError, match="No input prompt provided in config"):
            await pipe._process(sample_context)

    async def test_process_none_prompt(self, sample_config, sample_context):
        """Test processing with None prompt."""
        config = sample_config.model_copy(update={"prompt": None})
        pipe = HFLocalAiInferencePipe(config)

        with pytest.raises(ValueError, match="No input prompt provided in config"):
            await pipe._process(sample_context)

    @patch(
        "open_ticket_ai.extensions.pipe_implementations.hf_local_ai_inference_pipe.HFLocalAiInferencePipe._load_pipeline"
    )
    async def test_process_with_list_result(self, mock_load_pipeline, sample_config, sample_context):
        """Test processing when pipeline returns a list."""
        mock_pipeline = MagicMock()
        mock_pipeline.return_value = [{"label": "POSITIVE", "score": 0.9998}, {"label": "NEGATIVE", "score": 0.0002}]
        mock_load_pipeline.return_value = mock_pipeline
        pipe = HFLocalAiInferencePipe(sample_config)

        result = await pipe._process(sample_context)

        assert result == {"label": "POSITIVE", "confidence": 0.9998}

    @patch(
        "open_ticket_ai.extensions.pipe_implementations.hf_local_ai_inference_pipe.HFLocalAiInferencePipe._load_pipeline"
    )
    async def test_process_with_single_result(self, mock_load_pipeline, sample_config, sample_context):
        """Test processing when pipeline returns a single result."""
        mock_pipeline = MagicMock()
        mock_pipeline.return_value = {"label": "NEGATIVE", "score": 0.8765}
        mock_load_pipeline.return_value = mock_pipeline
        pipe = HFLocalAiInferencePipe(sample_config)

        result = await pipe._process(sample_context)

        assert result == {"label": "NEGATIVE", "confidence": 0.8765}

    @patch("transformers.pipeline")
    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForSequenceClassification.from_pretrained")
    def test_load_pipeline(self, mock_model, mock_tokenizer, mock_pipeline):
        """Test _load_pipeline static method."""
        mock_tokenizer_instance = MagicMock()
        mock_model_instance = MagicMock()
        mock_pipeline_instance = MagicMock()

        mock_tokenizer.return_value = mock_tokenizer_instance
        mock_model.return_value = mock_model_instance
        mock_pipeline.return_value = mock_pipeline_instance

        result = HFLocalAiInferencePipe._load_pipeline("test-model", "test-token")

        mock_tokenizer.assert_called_once_with("test-model", token="test-token")
        mock_model.assert_called_once_with("test-model", token="test-token")
        mock_pipeline.assert_called_once_with(
            "text-classification", model=mock_model_instance, tokenizer=mock_tokenizer_instance
        )
        assert result == mock_pipeline_instance

    @patch("transformers.pipeline")
    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForSequenceClassification.from_pretrained")
    def test_load_pipeline_no_token(self, mock_model, mock_tokenizer, mock_pipeline):
        """Test _load_pipeline static method without token."""
        result = HFLocalAiInferencePipe._load_pipeline("test-model", None)

        mock_tokenizer.assert_called_once_with("test-model", token=None)
        mock_model.assert_called_once_with("test-model", token=None)
        mock_pipeline.assert_called_once()
