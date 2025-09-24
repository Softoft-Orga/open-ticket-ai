import logging
import os
from functools import lru_cache
from typing import Optional

from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class HFLocalAIInferenceService(
    Pipe
):
    def __init__(self, config: dict):
        # No need to call super() with config anymore
        self.config = config

        self.logger = logging.getLogger(self.__class__.__name__)
        self._pipeline = None

    def _get_token(self) -> Optional[str]:
        if "hf_token_env_var" not in self.config:
            self.logger.warning(
                "No hf_token_env_var provided; proceeding without auth token"
            )
            return None

        token = os.getenv(self.config["hf_token_env_var"], "").strip()
        if not token:
            self.logger.warning(
                f"Environment variable '{self.config['hf_token_env_var']}' is not set or empty; proceeding without auth token"
            )
            return None
        if not token.startswith("hf_"):
            self.logger.warning(
                f"Token from '{self.config["hf_token_env_var"]}' does not appear to be a valid HuggingFace token"
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
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name, token=token
        )
        return pipeline("text-classification", model=model, tokenizer=tokenizer)

    async def process(
        self, context: PipelineContext[dict]
    ) -> PipelineContext[dict]:
        if self._pipeline is None:
            token = self._get_token()
            self._pipeline = self._load_pipeline(self.config["hf_model"], token)

        text = context.data[self.config["input_field"]] or ""
        result = self._pipeline(text, truncation=True)
        top = result[0] if isinstance(result, list) else result

        label = top["label"]
        score = float(top["score"])

        self.logger.info(f"Prediction: label {label} with score {score}")
        new_context = PipelineContext(
            meta_info=context.meta_info,
            data=context.data
                 | {
                     self.config["output_structure"]["label_field"]: label,
                     self.config["output_structure"]["confidence_field"]: score
                 }
        )
        return new_context
