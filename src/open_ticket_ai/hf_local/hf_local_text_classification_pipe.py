import logging
from functools import cache
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.configurable_pipe import ConfigurablePipe


class HFLocalTextClassificationPipeConfig(BaseModel):
    model: str
    token: str | None = None
    prompt: str


class HFLocalTextClassificationPipe(ConfigurablePipe):
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.config = HFLocalTextClassificationPipeConfig(**config)
        self.logger = logging.getLogger(self.__class__.__name__)
        self._pipeline = None

    @staticmethod
    @cache
    def _load_pipeline(model_name: str, token: str | None):
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            pipeline,
        )

        tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, token=token)
        return pipeline("text-classification", model=model, tokenizer=tokenizer)

    async def _process(self) -> dict[str, Any]:
        self.logger.info(f"Running {self.__class__.__name__}")
        if self._pipeline is None:
            self._pipeline = self._load_pipeline(self.config.model, self.config.token)

        result = self._pipeline(self.config.prompt, truncation=True)
        top = result[0] if isinstance(result, list) else result

        label = top["label"]
        score = float(top["score"])

        self.logger.info(f"Prediction: label {label} with score {score}")

        return {"label": label, "confidence": score}
