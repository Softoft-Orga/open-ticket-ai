from functools import cache
from typing import Any

from open_ticket_ai.core.base_model import OpenTicketAIBaseModel
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_models import PipeResult
from pydantic import ConfigDict, Field
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
    pipeline,
)


class HFLocalTextClassificationParams(OpenTicketAIBaseModel):
    model_config = ConfigDict(frozen=False, extra="forbid")

    model: str = Field(
        description="HuggingFace model identifier or local path to the pre-trained text classification model to use."
    )
    token: str | None = Field(
        default=None,
        description="Optional HuggingFace API token for accessing private or gated models from the model hub.",
    )
    prompt: str = Field(description="Input text to classify using the loaded model for prediction and analysis.")


class HFLocalTextClassificationPipe(Pipe):
    _pipeline: Any

    @staticmethod
    def get_params_model() -> type[OpenTicketAIBaseModel]:
        return HFLocalTextClassificationParams

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._params: HFLocalTextClassificationParams = self._params
        self._pipeline = None

    @staticmethod
    @cache
    def _load_pipeline(model_name: str, token: str | None) -> Any:
        tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
        model: PreTrainedModel = AutoModelForSequenceClassification.from_pretrained(model_name, token=token)
        return pipeline("text-classification", model=model, tokenizer=tokenizer)

    async def _process(self) -> PipeResult:
        self._logger.info(f"Running {self.__class__.__name__}")
        if self._pipeline is None:
            self._pipeline = self._load_pipeline(self._params.model, self._params.token)

        result = self._pipeline(self._params.prompt, truncation=True)
        top = result[0] if isinstance(result, list) else result

        label = top["label"]
        score = float(top["score"])

        self._logger.info(f"Prediction: label {label} with score {score}")

        return PipeResult(succeeded=True, data={"label": label, "confidence": score})
