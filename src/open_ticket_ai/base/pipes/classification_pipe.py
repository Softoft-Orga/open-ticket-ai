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
        classification_result: ClassificationResult = self._classification_service.classify(
            ClassificationRequest(
                text=self._params.text,
                model_name=self._params.model_name,
                api_token=self._params.api_token,
            )
        )

        return PipeResult.success(data=classification_result.model_dump())
