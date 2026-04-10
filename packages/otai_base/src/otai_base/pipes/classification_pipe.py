from collections.abc import Callable

from open_ticket_ai.core.ai_classification_services.classification_models import (
    ClassificationRequest,
    ClassificationResult,
)
from open_ticket_ai.core.ai_classification_services.classification_service import ClassificationService
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult

type ContextResolver[T] = T | Callable[[PipeContext], T]

_TEXT_PREVIEW_LIMIT = 100


def _resolve[T](value: ContextResolver[T], context: PipeContext) -> T:
    return value(context) if callable(value) else value


class ClassificationPipe(Pipe):
    """Classify text using a ClassificationService.

    ``get_text`` can be a static string or a callable that extracts the text
    from the current PipeContext (for dynamic pipelines).
    """

    def __init__(
        self,
        pipe_id: str,
        classification_service: ClassificationService,
        model_name: str,
        get_text: ContextResolver[str],
        api_token: str | None = None,
    ) -> None:
        super().__init__(pipe_id)
        self._service = classification_service
        self._model_name = model_name
        self._get_text = get_text
        self._api_token = api_token

    async def _process(self, context: PipeContext) -> PipeResult:
        text = _resolve(self._get_text, context)

        preview = text[:_TEXT_PREVIEW_LIMIT] + "..." if len(text) > _TEXT_PREVIEW_LIMIT else text
        self._logger.info(f"Classifying with model {self._model_name} (text: {preview})")

        result: ClassificationResult = self._service.classify(
            ClassificationRequest(
                text=text,
                model_name=self._model_name,
                api_token=self._api_token,
            )
        )

        self._logger.info(f"Result: {result.label} (confidence={result.confidence:.4f})")
        return PipeResult.success(data=result.model_dump())
