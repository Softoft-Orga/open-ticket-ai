from __future__ import annotations

from typing import Any, ClassVar

from open_ticket_ai import LoggerFactory, Pipe, StrictBaseModel
from open_ticket_ai.core.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from open_ticket_ai.core.ai_classification_services.classification_service import ClassificationService
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult

_TEXT_PREVIEW_LIMIT = 100


class ClassificationPipeParams(StrictBaseModel):
    text: str
    model_name: str
    api_token: str | None = None


class ClassificationPipe(Pipe[ClassificationPipeParams]):
    ParamsModel: ClassVar[type[ClassificationPipeParams]] = ClassificationPipeParams

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
        text_preview = self._preview_text(self._params.text)

        self._logger.info(f"🤖 Classifying text with model: {self._params.model_name}")
        self._logger.debug(f"Text preview: {text_preview}")
        self._logger.debug(f"Text length: {len(self._params.text)} characters")

        classification_result: ClassificationResult = self._classification_service.classify(
            ClassificationRequest(
                text=self._params.text,
                model_name=self._params.model_name,
                api_token=self._params.api_token,
            )
        )

        result_message = (
            f"✅ Classification result: {classification_result.label} "
            f"(confidence: {classification_result.confidence:.4f})"
        )
        self._logger.info(result_message)

        if hasattr(classification_result, "scores") and classification_result.scores:
            self._logger.debug(f"All scores: {classification_result.scores}")

        return PipeResult.success(data=classification_result.model_dump())

    def _preview_text(self, text: str) -> str:
        if len(text) <= _TEXT_PREVIEW_LIMIT:
            return text
        return f"{text[:_TEXT_PREVIEW_LIMIT]}..."
