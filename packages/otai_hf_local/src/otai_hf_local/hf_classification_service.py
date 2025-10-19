import logging
from collections.abc import Callable
from functools import lru_cache
from typing import Any

from open_ticket_ai.base.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from pydantic import BaseModel
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Pipeline,
    PreTrainedModel,
    PreTrainedTokenizer,
    pipeline,
)

hf_logger = logging.getLogger(__name__)


@lru_cache(maxsize=16)
def _get_hf_pipeline(model: str, token: str | None) -> Pipeline:
    hf_logger.info(f"🤗 Loading HuggingFace model: {model}")
    hf_logger.debug(f"Token provided: {'Yes' if token else 'No'}")

    try:
        tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(model, token=token)
        hf_logger.debug(f"✅ Tokenizer loaded for model: {model}")

        loaded_model: PreTrainedModel = AutoModelForSequenceClassification.from_pretrained(model, token=token)
        hf_logger.debug(f"✅ Model loaded: {model}")

        pipe = pipeline("text-classification", model=loaded_model, tokenizer=tokenizer)
        hf_logger.info(f"✅ HuggingFace pipeline ready for model: {model}")
        return pipe
    except Exception as e:
        hf_logger.error(f"❌ Failed to load HuggingFace model {model}: {e}", exc_info=True)
        raise


type GetPipelineFunc = Callable[[str, str | None], Pipeline]


class HFClassificationService(Injectable[StrictBaseModel]):
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
        self._logger.info("🤗 HFClassificationService initialized")

    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return StrictBaseModel

    def classify(self, req: ClassificationRequest) -> ClassificationResult:
        self._logger.info(f"🤖 Running HuggingFace classification with model: {req.model_name}")
        text_preview = req.text[:100] + "..." if len(req.text) > 100 else req.text
        self._logger.debug(f"Text preview: {text_preview}")

        try:
            classify: Pipeline = self._get_pipeline(req.model_name, req.api_token)
            self._logger.debug("Pipeline obtained, running classification...")

            classifications: Any = classify(req.text, truncation=True)

            if not classifications:
                self._logger.error("❌ No classification result returned from HuggingFace pipeline")
                raise ValueError("No classification result returned from HuggingFace pipeline")

            if not isinstance(classifications, list):
                self._logger.error(f"❌ HuggingFace pipeline returned non-list result: {type(classifications)}")
                raise TypeError("HuggingFace pipeline returned a non-list result")

            classification = classifications[0]
            result = ClassificationResult(label=classification["label"], confidence=classification["score"])

            self._logger.info(f"✅ Classification complete: {result.label} (confidence: {result.confidence:.4f})")
            self._logger.debug(f"Full classification result: {classification}")

            return result

        except Exception as e:
            self._logger.error(f"❌ Classification failed: {e}", exc_info=True)
            raise

    async def aclassify(self, req: ClassificationRequest) -> ClassificationResult:
        self._logger.debug("Async classification requested, delegating to sync classify")
        return self.classify(req)
