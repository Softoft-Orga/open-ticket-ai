import inspect
import os
from collections.abc import Callable
from functools import lru_cache
from typing import Any, ClassVar

from open_ticket_ai import Injectable, InjectableConfig, LoggerFactory, StrictBaseModel
from open_ticket_ai.core.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from pydantic import BaseModel, Field
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Pipeline,
    pipeline,
)


@lru_cache(maxsize=16)
def _get_hf_pipeline(model: str, token: str | None):
    token = token or os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN")
    kw = (
        {"token": token}
        if "token" in inspect.signature(AutoTokenizer.from_pretrained).parameters
        else {"use_auth_token": token}
    )
    return pipeline(
        "text-classification",
        model=AutoModelForSequenceClassification.from_pretrained(model, **kw),
        tokenizer=AutoTokenizer.from_pretrained(model, **kw),
    )


type GetPipelineFunc = Callable[[str, str | None], Pipeline]


class HFClassificationServiceParams(StrictBaseModel):
    api_token: str | None = Field(
        default=None,
        description="Optional HuggingFace API token for accessing private models or increased rate limits.",
    )


class HFClassificationService(Injectable[HFClassificationServiceParams]):
    ParamsModel: ClassVar[type[BaseModel]] = HFClassificationServiceParams

    def __init__(
        self,
        config: InjectableConfig,
        logger_factory: LoggerFactory,
        get_pipeline: GetPipelineFunc = _get_hf_pipeline,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(config, logger_factory, *args, **kwargs)
        self._get_pipeline = get_pipeline

    def _log_init(self) -> None:
        self._logger.info("HFClassificationService initialized")

    def classify(self, classification_request: ClassificationRequest) -> ClassificationResult:
        classification_request = classification_request.model_copy(
            update={"api_token": classification_request.api_token or self._params.api_token}
        )
        self._logger.info(f"Classification started for model {classification_request.model_name}")
        classify: Pipeline = self._get_pipeline(classification_request.model_name, classification_request.api_token)

        classifications: Any = classify(classification_request.text, truncation=True)

        if not classifications:
            raise ValueError("No classification result returned from HuggingFace pipeline")

        if not isinstance(classifications, list):
            raise TypeError("HuggingFace pipeline returned a non-list result")

        classification = classifications[0]
        result = ClassificationResult(label=classification["label"], confidence=classification["score"])

        self._logger.info(f"Classification complete for label {result.label}")

        return result

    async def aclassify(self, req: ClassificationRequest) -> ClassificationResult:
        return self.classify(req)
