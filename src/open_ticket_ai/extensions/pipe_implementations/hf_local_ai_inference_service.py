import logging
import os
from functools import lru_cache
from typing import Optional, Dict, Any

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.extensions.pipe_implementations.pipe_configs import HFLocalAIInferenceServiceConfig


class HFLocalAIInferenceService(Pipe[HFLocalAIInferenceServiceConfig]):
    ConfigModel = HFLocalAIInferenceServiceConfig

    def __init__(self, config: HFLocalAIInferenceServiceConfig, *args, **kwargs):
        super().__init__(config)
        self.logger = logging.getLogger(self.__class__.__name__)
        self._pipeline = None

    def _get_token(self) -> Optional[str]:
        if not self.config.hf_token_env_var:
            self.logger.warning("No hf_token_env_var provided; proceeding without auth token")
            return None

        token = os.getenv(self.config.hf_token_env_var, "").strip()
        if not token:
            self.logger.warning(
                f"Environment variable '{self.config.hf_token_env_var}' is not set or empty; proceeding without auth token"
            )
            return None
        if not token.startswith("hf_"):
            self.logger.warning(
                f"Token from '{self.config.hf_token_env_var}' does not appear to be a valid HuggingFace token"
            )
        return token

    @staticmethod
    @lru_cache(maxsize=None)
    def _load_pipeline(model_name: str, token: Optional[str]):
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            pipeline,
        )

        tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, token=token)
        return pipeline("text-classification", model=model, tokenizer=tokenizer)

    async def _process(self, rendered_config: HFLocalAIInferenceServiceConfig) -> Dict[str, Any]:
        self._logger.info(f"Running {self.__class__.__name__}")
        if self._pipeline is None:
            token = self._get_token()
            self._pipeline = self._load_pipeline(rendered_config.hf_model, token)

        # Get input prompt from config
        prompt = rendered_config.prompt
        if not prompt:
            raise ValueError("No input prompt provided in config")

        result = self._pipeline(prompt, truncation=True)
        top = result[0] if isinstance(result, list) else result

        label = top["label"]
        score = float(top["score"])

        self.logger.info(f"Prediction: label {label} with score {score}")

        # Return just the new state updates
        return {"label": label, "confidence": score}
