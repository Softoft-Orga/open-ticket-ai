# FILE_PATH: open_ticket_ai\src\ce\run\pipe_implementations\hf_local_ai_inference_service.py
from __future__ import annotations

import os


from open_ticket_ai.src.core.config.config_models import ProvidableConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class HFLocalAIInferenceService(Pipe):
    """A pipeline component for Hugging Face model inference.

    This class implements a Pipe for running text classification using a pre-trained
    Hugging Face model. It handles model loading, tokenization, and inference execution.

    Attributes:
        ai_inference_config (ProvidableConfig): Configuration for the inference service.
        input_field (str): Key in context data containing input text. Defaults to "prepared_data".
        result_field (str): Key to store inference results in context data. Defaults to "model_result".
        model_name (str): Name of the Hugging Face model to load.
        tokenizer (AutoTokenizer): Tokenizer for the specified model.
        _pipeline (Pipeline): Hugging Face text classification pipeline.
    """

    def __init__(self, config: ProvidableConfig):
        """Initializes the Hugging Face inference service with configuration.

        Loads model and tokenizer, and creates a text-classification pipeline. Authentication
        token is retrieved from environment variables if specified in configuration.

        Args:
            config (ProvidableConfig): Configuration object containing a `params` dictionary
                with the following keys:
                - `hf_model` (str): Required model identifier (e.g., "distilbert-base-uncased").
                - `input_field` (str, optional): Key for input text in context data. Defaults to "prepared_data".
                - `result_field` (str, optional): Key for storing results. Defaults to "model_result".
                - `hf_token_env_var` (str, optional): Environment variable name for Hugging Face token.

        Raises:
            KeyError: If required 'hf_model' parameter is missing.
            EnvironmentError: If token environment variable is specified but not set.
        """
        super().__init__(config)
        self.ai_inference_config = config

        params = config.params
        self.input_field: str = params.get("input_field", "prepared_data")
        self.result_field: str = params.get("result_field", "model_result")
        self.model_name: str = params["hf_model"]
        token_env = params.get("hf_token_env_var")
        token = os.getenv(token_env) if token_env else None

        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            pipeline,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=token)
        model = AutoModelForSequenceClassification.from_pretrained(self.model_name, token=token)
        self._pipeline = pipeline(
            "text-classification",
            model=model,
            tokenizer=self.tokenizer,
        )

    def process(self, context: PipelineContext) -> PipelineContext:
        """Runs model inference on input text and stores results.

        This method retrieves the input text from the context using the key specified by `input_field`,
        runs the text classification pipeline on the text, and stores the result in the context under
        the key specified by `result_field`.

        Args:
            context (PipelineContext): Pipeline context containing data dictionary.

        Returns:
            PipelineContext: Updated context with inference results stored under `result_field`.
        """
        text = context.data.get(self.input_field, "")
        result = self._pipeline(text)
        context.data[self.result_field] = result
        return context

    @staticmethod
    def get_description() -> str:
        """Provides a description of the service.

        Returns:
            str: Description text for the Hugging Face AI model service.
        """
        return "Hugging Face AI Model"

# Backwards compatibility alias
HFAIInferenceService = HFLocalAIInferenceService
import builtins
builtins.HFAIInferenceService = HFLocalAIInferenceService
