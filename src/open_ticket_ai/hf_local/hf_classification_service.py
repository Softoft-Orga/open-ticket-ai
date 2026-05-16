import inspect
import logging
import os
from collections.abc import Callable
from functools import lru_cache
from typing import Any

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Pipeline,
    pipeline,
)

from open_ticket_ai.core.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from open_ticket_ai.core.ai_classification_services.classification_service import ClassificationService


@lru_cache(maxsize=16)
def _get_hf_pipeline(model: str, token: str | None) -> Pipeline:
    token = token or os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN")
    kw: dict[str, Any] = (
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


class HFClassificationService(ClassificationService):
    def __init__(
        self,
        api_token: str | None = None,
        get_pipeline: GetPipelineFunc = _get_hf_pipeline,
    ) -> None:
        self._api_token = api_token
        self._get_pipeline = get_pipeline
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info("HFClassificationService initialized")

    def classify(self, classification_request: ClassificationRequest) -> ClassificationResult:
        token = classification_request.api_token or self._api_token
        request = classification_request.model_copy(update={"api_token": token})

        self._logger.info(f"Classification started for model {request.model_name}")
        classify_pipeline: Pipeline = self._get_pipeline(request.model_name, request.api_token)

        classifications: Any = classify_pipeline(request.text, truncation=True)

        if not classifications:
            raise ValueError("No classification result returned from HuggingFace pipeline")
        if not isinstance(classifications, list):
            raise TypeError("HuggingFace pipeline returned a non-list result")

        classification = classifications[0]
        result = ClassificationResult(label=classification["label"], confidence=classification["score"])
        self._logger.info(f"Classification complete: {result.label}")
        return result

    async def aclassify(self, req: ClassificationRequest) -> ClassificationResult:
        return self.classify(req)
