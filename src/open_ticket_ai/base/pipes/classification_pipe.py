from typing import Any

from open_ticket_ai.base.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from open_ticket_ai.base.ai_classification_services.classification_service import ClassificationService
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


class ClassificationPipeParams(StrictBaseModel):
    text: str
    model_name: str
    api_token: str | None = None


class ClassificationPipe(Pipe[ClassificationPipeParams]):
    @staticmethod
    def get_params_model() -> type[ClassificationPipeParams]:
        return ClassificationPipeParams

    def __init__(
        self,
        config: PipeConfig,
        logger_factory: LoggerFactory,
        classification_service: ClassificationService,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)
        self._classification_service = classification_service

    async def _process(self, *_: Any, **__: Any) -> PipeResult:
        text_preview = self._params.text[:100] + "..." if len(self._params.text) > 100 else self._params.text

        self._logger.info(f"🤖 Classifying text with model: {self._params.model_name}")
        self._logger.debug(f"Text preview: {text_preview}")
        self._logger.debug(f"Text length: {len(self._params.text)} characters")

        try:
            classification_result: ClassificationResult = self._classification_service.classify(
                ClassificationRequest(
                    text=self._params.text,
                    model_name=self._params.model_name,
                    api_token=self._params.api_token,
                )
            )

            self._logger.info(
                f"✅ Classification result: {classification_result.label} (confidence: {classification_result.confidence:.4f})"
            )

            if hasattr(classification_result, "scores") and classification_result.scores:
                self._logger.debug(f"All scores: {classification_result.scores}")

            return PipeResult.success(data=classification_result.model_dump())

        except Exception as e:
            self._logger.error(f"❌ Classification failed: {e}", exc_info=True)
            raise
