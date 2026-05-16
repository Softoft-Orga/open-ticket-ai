"""Single-text classification endpoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Request

from open_ticket_ai.api.models import ClassifyRequest, ClassifyResponse
from open_ticket_ai.core.ai_classification_services.classification_models import (
    ClassificationRequest,
)

if TYPE_CHECKING:
    from open_ticket_ai.api.dependencies import AppState

router = APIRouter(prefix="/api", tags=["classification"])


def _state(request: Request) -> AppState:
    return request.app.state.app_state


@router.post("/classify", response_model=ClassifyResponse)
async def classify(request: Request, body: ClassifyRequest) -> ClassifyResponse:
    clf = _state(request).classification_service
    result = await clf.aclassify(
        ClassificationRequest(text=body.text, model_name=body.model_name),
    )
    return ClassifyResponse(label=result.label, confidence=result.confidence)
