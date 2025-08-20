from __future__ import annotations

import os
from typing import Optional

from huggingface_hub import get_inference_endpoint

from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class HFCloudInferenceService(Pipe):
    """Run inference on a Hugging Face Inference Endpoint."""

    def __init__(self__(self, config: ProvidableConfig) -> None:
        """Initializes the Hugging Face Inference Endpoint service.

        Args:
            config (ProvidableConfig): Configuration object containing parameters for the service.
                Expected parameters in `config.params`:
                - `input_field` (str, optional): Key in context data containing input text.
                    Defaults to "prepared_data".
                - `result_field` (str, optional): Key to store inference results in context data.
                    Defaults to "model_result".
                - `hf_endpoint_name` (str): Name or identifier of the Hugging Face endpoint.
                - `hf_token_env_var` (str, optional): Environment variable name containing
                    Hugging Face token. If not provided, no token will be used.

        Raises:
            ValueError: If `hf_endpoint_name` is not provided in config params.
        """
        super().__init__(config)
        params = config.params
        self.input_field: str = params.get("input_field", "prepared_data")
        self.result_field: str = params.get("result_field", "model_result")
        endpoint_identifier: str = params["hf_endpoint_name"]
        token_env: Optional[str] = params.get("hf_token_env_var")
        token = os.getenv(token_env) if token_env else None

        namespace: Optional[str] = None
        name = endpoint_identifier
        if "/" in endpoint_identifier:
            namespace, name = endpoint_identifier.split("/", 1)

        endpoint = get_inference_endpoint(name, namespace=namespace, token=token)
        self._client = endpoint.client

    def process(self, context: PipelineContext) -> PipelineContext:
        """Runs text classification on input data and stores results.

        Args:
            context (PipelineContext): Pipeline context containing input data.

        Returns:
            PipelineContext: Updated context with inference results stored under `result_field`.

        Steps:
            1. Extracts text from context using `input_field`
            2. Runs Hugging Face text classification
            3. Stores results in context under `result_field`
        """
        text = context.data.get(self.input_field, "")
        result = self._client.text_classification(text)
        context.data[self.result_field] = result
        return context

    @staticmethod
    def get_description() -> str:
        """Provides a description of this pipeline component.

        Returns:
            str: Fixed description string "Hugging Face Inference Endpoint".
        """
        return "Hugging Face Inference Endpoint"
