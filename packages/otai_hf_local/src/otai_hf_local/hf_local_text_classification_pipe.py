from functools import cache
from typing import Any

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


class HFLocalTextClassificationPipe(Pipe):
    _pipeline: Any

    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return HFLocalTextClassificationParams

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.model = self._params.model
        self.token = self._params.token
        self.prompt = self._params.prompt
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
