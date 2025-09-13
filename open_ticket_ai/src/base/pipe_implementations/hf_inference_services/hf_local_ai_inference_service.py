"""Module for Hugging Face local AI inference service implementation.

This module provides a pipeline component (Pipe) for running Hugging Face models locally
for text classification tasks within a processing pipeline.
"""
from __future__ import annotations

import os


from open_ticket_ai.src.core.config.config_models import ProvidableConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class HFLocalAIInferenceService(Pipe):
    """
    A Hugging Face local AI inference service for text classification.

    This class uses the Hugging Face transformers library to run a local model for text classification.
    It is designed to be used as a pipe in a pipeline.

    Attributes:
        ai_inference_config (ProvidableConfig): The configuration for the service.
        input_field (str): The key in the context data to use as input text. Defaults to "prepared_data".
        result_field (str): The key in the context data to store the result. Defaults to "model_result".
        model_name (str): The name of the Hugging Face model to use.
        tokenizer (AutoTokenizer): The tokenizer for the model.
        _pipeline (Pipeline): The Hugging Face pipeline for text classification.
    """

    def __init__(self, config: ProvidableConfig):
        """
        Initializes the HFLocalAIInferenceService with configuration.

        Sets up the tokenizer and pipeline for the specified Hugging Face model.

        Args:
            config (ProvidableConfig): Configuration instance for the service. Expected to have:
                - params: A dictionary containing:
                    * "input_field": (str, optional) The key in the context data for input text. Defaults to "prepared_data".
                    * "result_field": (str, optional) The key to store the result in the context data. Defaults to "model_result".
                    * "hf_model": (str) The name of the Hugging Face model.
                    * "hf_token_env_var": (str, optional) The environment variable name for the Hugging Face token.

        Raises:
            KeyError: If the required parameter "hf_model" is not provided.
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
        """
        Runs the Hugging Face text classification pipeline on the input text from the context.

        The input text is taken from the context's data using the key specified by `input_field`.
        The result of the pipeline (a list of dictionaries) is stored in the context's data under the key `result_field`.

        Args:
            context (PipelineContext): The pipeline context containing the data to process.

        Returns:
            PipelineContext: The updated context with the model result stored in the data.

        Example of the result format:
            ```python
            [{'label': 'POSITIVE', 'score': 0.9998}]
            ```
        """
        text = context.data.get(self.input_field, "")
        result = self._pipeline(text)
        context.data[self.result_field] = result
        return context

    @staticmethod
    def get_description() -> str:
        """
        Provides a description of the service.

        Returns:
            str: Description text for the Hugging Face AI model service.
        """
        return "Hugging Face AI Model"
