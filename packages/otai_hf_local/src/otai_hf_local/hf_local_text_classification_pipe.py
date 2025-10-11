import logging
from functools import cache
from typing import Any

from open_ticket_ai.core.config.registerable import Renderable
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from pydantic import BaseModel
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
)


class HFLocalTextClassificationParams(BaseModel):
    model: str
    token: str | None = None
    prompt: str


class HFLocalTextClassificationPipeConfig(Renderable[HFLocalTextClassificationParams]):
    pass


class HFLocalTextClassificationPipe(Pipe):
    _pipeline: Any

    def __init__(self, pipe_params: HFLocalTextClassificationPipeConfig, *args: Any, **kwargs: Any) -> None:
        super().__init__(pipe_params)
        if isinstance(pipe_params, dict):
            self.config = HFLocalTextClassificationPipeConfig.model_validate(pipe_params)
        elif isinstance(pipe_params, HFLocalTextClassificationPipeConfig):
            self.config = pipe_params
        else:
            self.config = HFLocalTextClassificationPipeConfig.model_validate(pipe_params.model_dump())
        self.logger = logging.getLogger(self.__class__.__name__)
        self._pipeline = None

    @staticmethod
    @cache
    def _load_pipeline(model_name: str, token: str | None) -> Any:
        tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, token=token)
        return pipeline("text-classification", model=model, tokenizer=tokenizer)

    async def _process(self) -> PipeResult:
        self.logger.info(f"Running {self.__class__.__name__}")
        if self._pipeline is None:
            self._pipeline = self._load_pipeline(self.config.params.model, self.config.params.token)

        result = self._pipeline(self.config.params.prompt, truncation=True)
        top = result[0] if isinstance(result, list) else result

        label = top["label"]
        score = float(top["score"])

        self.logger.info(f"Prediction: label {label} with score {score}")

        return PipeResult(success=True, failed=False, data={"label": label, "confidence": score})
