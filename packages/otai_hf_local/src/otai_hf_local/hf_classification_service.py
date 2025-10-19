from functools import lru_cache
from typing import Any, Callable

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
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory

type GetPipelineFunc = Callable[[str, str], Pipeline]


@lru_cache(maxsize=16)
def _get_hf_pipeline(model: str, token: str | None) -> Pipeline:
    tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(model, token=token)
    model: PreTrainedModel = AutoModelForSequenceClassification.from_pretrained(model, token=token)
    return pipeline("text-classification", model=model, tokenizer=tokenizer)


class HFClassificationService(Injectable[StrictBaseModel]):
    def __init__(
            self,
            config: InjectableConfig,
            logger_factory: LoggerFactory,
            get_pipeline: GetPipelineFunc = _get_hf_pipeline,
            *args: Any,
            **kwargs: Any
    ):
        super().__init__(config, logger_factory, *args, **kwargs)
        self._get_pipeline = get_pipeline

    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return StrictBaseModel

    def classify(self, req: ClassificationRequest) -> ClassificationResult:
        classify: Pipeline = self._get_pipeline(req.model_name, req.api_token)
        classifications: Any = classify(req.text, truncation=True)
        if not classifications:
            raise ValueError("No classification result returned from HuggingFace pipeline")
        if not isinstance(classifications, list):
            raise TypeError("HuggingFace pipeline returned a non-list result")
        classification = classifications[0]
        return ClassificationResult(label=classification["label"], confidence=classification["score"])

    async def aclassify(self, req: ClassificationRequest) -> ClassificationResult:
        return self.classify(req)
