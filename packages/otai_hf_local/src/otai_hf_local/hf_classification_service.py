from collections.abc import Callable
from functools import lru_cache
from typing import Any

from open_ticket_ai.base.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.injectables.injectable import Injectable
from pydantic import BaseModel
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Pipeline,
    PreTrainedModel,
    PreTrainedTokenizer,
    pipeline,
)


@lru_cache(maxsize=16)
def _get_hf_pipeline(model: str, token: str | None) -> Pipeline:
    tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(model, token=token)
    loaded_model: PreTrainedModel = AutoModelForSequenceClassification.from_pretrained(model, token=token)
    return pipeline("text-classification", model=loaded_model, tokenizer=tokenizer)


type GetPipelineFunc = Callable[[str, str | None], Pipeline]


class HFClassificationService(Injectable[StrictBaseModel]):
    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return StrictBaseModel

    def classify(
        self, req: ClassificationRequest, get_pipeline: GetPipelineFunc = _get_hf_pipeline
    ) -> ClassificationResult:
        classify: Pipeline = get_pipeline(req.model_name, req.api_token)
        classifications: Any = classify(req.text, truncation=True)
        if not classifications:
            raise ValueError("No classification result returned from HuggingFace pipeline")
        if not isinstance(classifications, list):
            raise TypeError("HuggingFace pipeline returned a non-list result")
        classification = classifications[0]
        return ClassificationResult(label=classification["label"], confidence=classification["score"])

    async def aclassify(
        self, req: ClassificationRequest, get_pipeline: GetPipelineFunc = _get_hf_pipeline
    ) -> ClassificationResult:
        return self.classify(req, get_pipeline)
