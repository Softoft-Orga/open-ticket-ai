from functools import lru_cache
from typing import Any

from pydantic import BaseModel
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Pipeline,
    PreTrainedModel,
    PreTrainedTokenizer,
    pipeline,
)

from open_ticket_ai.base.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.injectables.injectable import Injectable


@lru_cache(maxsize=16)
def _get_hf_pipeline(model: str, token: str | None):
    tok: PreTrainedTokenizer = AutoTokenizer.from_pretrained(model, token=token)
    mdl: PreTrainedModel = AutoModelForSequenceClassification.from_pretrained(model, token=token)
    return pipeline("text-classification", model=mdl, tokenizer=tok)


class HFClassificationService(Injectable[StrictBaseModel]):
    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return StrictBaseModel

    def classify(self, req: ClassificationRequest) -> ClassificationResult:
        classify: Pipeline = _get_hf_pipeline(req.model_name, req.api_token)
        classifications: Any = classify(req.text, truncation=True)
        if not classifications:
            raise ValueError("No classification result returned from HuggingFace pipeline")
        if not isinstance(classifications, list):
            raise TypeError("HuggingFace pipeline returned a non-list result")
        classification = classifications[0]
        return ClassificationResult(label=classification["label"], confidence=classification["score"])
