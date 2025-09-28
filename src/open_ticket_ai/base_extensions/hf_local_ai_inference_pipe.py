import os
from functools import cache
from typing import Any

from open_ticket_ai.base_extensions.pipe_configs import (
    HFLocalAIInferencePipeConfig,
    HFLocalAIInferencePipeModel,
)
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.pipeline.pipe import Pipe


class HFLocalAiInferencePipe(Pipe[HFLocalAIInferencePipeModel]):
    """
    A pipe that performs inference using Hugging Face models locally.
    """

    def __init__(self, config: HFLocalAIInferencePipeConfig, *args: Any, **kwargs: Any):
        super().__init__(config, *args, **kwargs)
        self._pipeline: Any | None = None

    def _get_token(self, config: HFLocalAIInferencePipeModel) -> str | None:
        if not config.hf_token_env_var:
            self._logger.warning("No hf_token_env_var provided; proceeding without auth token")
            return None

        token = os.getenv(config.hf_token_env_var, "").strip()
        if not token:
            self._logger.warning(
                f"Environment variable '{config.hf_token_env_var}' is not set or empty; "
                f"proceeding without auth token"
            )
            return None
        if not token.startswith("hf_"):
            self._logger.warning(
                f"Token from '{config.hf_token_env_var}' does not appear to be a valid HuggingFace token"
            )
        return token

    @staticmethod
    @cache
    def _load_pipeline(model_name: str, token: str | None) -> Any:
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            pipeline,
        )

        tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, token=token)
        return pipeline("text-classification", model=model, tokenizer=tokenizer)

    async def _process(
        self, context: PipelineContext, config: HFLocalAIInferencePipeModel
    ) -> dict[str, Any]:
        self._logger.info(f"Running {self.__class__.__name__}")

        if self._pipeline is None:
            token = self._get_token(config)
            self._pipeline = self._load_pipeline(config.hf_model, token)

        prompt = config.prompt
        if not prompt:
            raise ValueError("No input prompt provided in config")

        result = self._pipeline(prompt, truncation=True)
        top = result[0] if isinstance(result, list) else result

        label = top["label"]
        score = float(top["score"])

        self._logger.info(f"Prediction: label {label} with score {score}")

        return {"label": label, "confidence": score}
