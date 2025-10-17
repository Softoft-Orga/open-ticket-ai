from functools import lru_cache
from typing import Any

from transformers import PreTrainedTokenizer, AutoTokenizer, PreTrainedModel, AutoModelForSequenceClassification, \
    pipeline, Pipeline

from open_ticket_ai.base.ai_classification_services.classification_models import ClassificationRequest, \
    ClassificationResult
from open_ticket_ai.base.ai_classification_services.classification_service import ClassificationService


@lru_cache(maxsize=16)
def _get_hf_pipeline(model: str, token: str | None):
    tok: PreTrainedTokenizer = AutoTokenizer.from_pretrained(model, token=token)
    mdl: PreTrainedModel = AutoModelForSequenceClassification.from_pretrained(model, token=token)
    return pipeline("text-classification", model=mdl, tokenizer=tok)


class HFClassificationService(ClassificationService):
    def classify(self, req: ClassificationRequest) -> ClassificationResult:
        classify: Pipeline = _get_hf_pipeline(req.model_name, req.api_token)
        classifications: Any = classify(req.text, truncation=True)
        if not classifications:
            raise ValueError("No classification result returned from HuggingFace pipeline")
        if not isinstance(classifications, list):
            raise TypeError("HuggingFace pipeline returned a non-list result")
        classification = classifications[0]
        return ClassificationResult(label=classification["label"], confidence=classification["score"])
