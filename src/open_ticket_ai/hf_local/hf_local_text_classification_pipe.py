import logging
from functools import cache
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult


class HFLocalTextClassificationPipeConfig(BaseModel):
    model: str
    token: str | None = None
    prompt: str


class HFLocalTextClassificationPipe(Pipe):
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        pipe_config = HFLocalTextClassificationPipeConfig(**config)
        self.model = pipe_config.model
        self.token = pipe_config.token
        self.prompt = pipe_config.prompt
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

    async def _process(self) -> PipeResult:
        self.logger.info(f"Running {self.__class__.__name__}")
        if self._pipeline is None:
            self._pipeline = self._load_pipeline(self.model, self.token)

        result = self._pipeline(self.prompt, truncation=True)
        top = result[0] if isinstance(result, list) else result

        label = top["label"]
        score = float(top["score"])

        self.logger.info(f"Prediction: label {label} with score {score}")

        return PipeResult(
            success=True,
            failed=False,
            message="Text classified successfully",
            data={"label": label, "confidence": score},
        )
