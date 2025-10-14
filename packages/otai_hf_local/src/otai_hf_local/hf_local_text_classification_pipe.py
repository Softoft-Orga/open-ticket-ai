from functools import cache
from typing import Any

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult
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


class HFLocalTextClassificationPipeConfig(PipeConfig):
    params: HFLocalTextClassificationParams


class HFLocalTextClassificationPipe(Pipe):
    _pipeline: Any

    def __init__(
        self,
        config: HFLocalTextClassificationPipeConfig,
        logger_factory: LoggerFactory,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(config, logger_factory=logger_factory)
        self._config = HFLocalTextClassificationPipeConfig.model_validate(config.model_dump())
        self.model = self._config.params.model
        self.token = self._config.params.token
        self.prompt = self._config.params.prompt
        self._pipeline = None

    @staticmethod
    @cache
    def _load_pipeline(model_name: str, token: str | None) -> Any:
        tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, token=token)
        return pipeline("text-classification", model=model, tokenizer=tokenizer)

    async def _process(self) -> PipeResult:
        self._logger.info(f"Running {self.__class__.__name__}")
        if self._pipeline is None:
            self._pipeline = self._load_pipeline(self.model, self.token)

        result = self._pipeline(self.prompt, truncation=True)
        top = result[0] if isinstance(result, list) else result

        label = top["label"]
        score = float(top["score"])

        self._logger.info(f"Prediction: label {label} with score {score}")

        return PipeResult(success=True, data={"label": label, "confidence": score})
