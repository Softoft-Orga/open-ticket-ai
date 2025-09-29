"""
Pytest tests for HFLocalAiInferencePipe.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from open_ticket_ai.basic_pipes.hf_local_ai_inference_pipe import HFLocalAiInferencePipe
from open_ticket_ai.basic_pipes.pipe_configs import (
    HFLocalAIInferencePipeConfig,
    HFLocalAIInferencePipeModel,
)
from open_ticket_ai.core.pipeline.context import PipelineContext


@pytest.fixture
def sample_config() -> HFLocalAIInferencePipeConfig:
    """Create a sample HFLocalAiInferencePipeConfig for testing.""""""Create a sample HFLocalAiInferencePipeConfig for testing."""
    return HFLocalAIInferencePipeConfig(
        name="test_hf_inference",
        use="open_ticket_ai.base_extensions.hf_local_ai_inference_pipe.HFLocalAiInferencePipe",
        config=HFLocalAIInferencePipeModel(
            prompt="Test prompt for classification",
            hf_model="distilbert-base-uncased-finetuned-sst-2-english",
            hf_token_env_var="HF_TOKEN",
        ),
    )


@pytest.fixture
def sample_context() -> PipelineContext:
    """Create a sample PipelineContext for testing."""
    return PipelineContext()


@pytest.fixture
def mock_pipeline() -> MagicMock:
    """Create a mock transformers pipeline."""
    mock_pipe = MagicMock()
    mock_pipe.return_value = [{"label": "POSITIVE", "score": 0.9998}]
    return mock_pipe


class TestHFLocalAiInferencePipe:
    """Test cases for HFLocalAiInferencePipe."""

    def test_init(self, sample_config: HFLocalAIInferencePipeConfig) -> None:
        """Test pipe initialization."""
        pipe = HFLocalAiInferencePipe(sample_config)
        assert pipe.config == sample_config
        assert pipe._pipeline is None

    @patch("open_ticket_ai.base_extensions.hf_local_ai_inference_pipe.HFLocalAiInferencePipe._load_pipeline")
    async def test_process_success(
        self, mock_load_pipeline: MagicMock, sample_config: HFLocalAIInferencePipeConfig, sample_context: PipelineContext, mock_pipeline: MagicMock
    ) -> None:
        """Test successful processing."""
        mock_load_pipeline.return_value = mock_pipeline
        pipe = HFLocalAiInferencePipe(sample_config)

        with patch.dict(os.environ, {"HF_TOKEN": "hf_test_token_123"}):
            result_context = await pipe.process(sample_context)

        result = result_context.pipes["test_hf_inference"]
        assert result == {"label": "POSITIVE", "confidence": 0.9998}
        mock_load_pipeline.assert_called_once_with(
            "distilbert-base-uncased-finetuned-sst-2-english", "hf_test_token_123"
        )
        mock_pipeline.assert_called_once_with("Test prompt for classification", truncation=True)

    @patch("open_ticket_ai.base_extensions.hf_local_ai_inference_pipe.HFLocalAiInferencePipe._load_pipeline")
    async def test_process_with_cached_pipeline(
        self, mock_load_pipeline: MagicMock, sample_config: HFLocalAIInferencePipeConfig, sample_context: PipelineContext, mock_pipeline: MagicMock
    ) -> None:
        """Test processing with already cached pipeline."""
        pipe = HFLocalAiInferencePipe(sample_config)
        pipe._pipeline = mock_pipeline  # Pre-set the pipeline

        result_context = await pipe.process(sample_context)
        result = result_context.pipes["test_hf_inference"]

        assert result == {"label": "POSITIVE", "confidence": 0.9998}
        mock_load_pipeline.assert_not_called()
        mock_pipeline.assert_called_once_with("Test prompt for classification", truncation=True)

    async def test_process_empty_prompt(self, sample_config: HFLocalAIInferencePipeConfig, sample_context: PipelineContext) -> None:
        """Test processing with empty prompt."""
        sample_config.config.prompt = ""
        pipe = HFLocalAiInferencePipe(sample_config)

        with pytest.raises(ValueError, match="No input prompt provided in config"):
            await pipe.process(sample_context)

    @patch("transformers.pipeline")
    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForSequenceClassification.from_pretrained")
    def test_load_pipeline(self, mock_model: MagicMock, mock_tokenizer: MagicMock, mock_pipeline: MagicMock) -> None:
        """Test _load_pipeline static method."""
        mock_tokenizer_instance = MagicMock()
        mock_model_instance = MagicMock()
        # This is needed to fool the transformers.pipeline's framework inference
        mock_model_instance.__class__.__module__ = "transformers.modeling_utils"
        mock_model_instance.__class__.__name__ = "PreTrainedModel"
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
