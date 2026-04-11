"""Workflow template management — start, stop, and inspect running workflows."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException, Request

from open_ticket_ai.api.dependencies import WORKFLOW_TEMPLATES
from open_ticket_ai.api.models import (
    WorkflowResponse,
    WorkflowStartRequest,
    WorkflowTemplateResponse,
)
from open_ticket_ai.workflow_manager import WorkflowInstance

if TYPE_CHECKING:
    from open_ticket_ai.api.dependencies import AppState

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


def _state(request: Request) -> AppState:
    return request.app.state.app_state


def _to_response(inst: WorkflowInstance) -> WorkflowResponse:
    return WorkflowResponse(
        workflow_id=inst.workflow_id,
        template_name=inst.template_name,
        parameters=inst.parameters,
        status=inst.status,
        started_at=inst.started_at,
        stopped_at=inst.stopped_at,
        error=inst.error,
    )


@router.get("/templates", response_model=list[WorkflowTemplateResponse])
async def list_templates() -> list[WorkflowTemplateResponse]:
    return list(WORKFLOW_TEMPLATES.values())


@router.get("/templates/{template_name}", response_model=WorkflowTemplateResponse)
async def get_template(template_name: str) -> WorkflowTemplateResponse:
    tpl = WORKFLOW_TEMPLATES.get(template_name)
    if tpl is None:
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")
    return tpl


@router.post("", response_model=WorkflowResponse, status_code=201)
async def start_workflow(request: Request, body: WorkflowStartRequest) -> WorkflowResponse:
    state = _state(request)
    if body.template_name not in WORKFLOW_TEMPLATES:
        raise HTTPException(status_code=404, detail=f"Template '{body.template_name}' not found")
    try:
        pipe = state.build_pipeline_from_template(body.template_name, body.parameters)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    instance = state.workflow_manager.start(body.template_name, body.parameters, pipe)
    return _to_response(instance)


@router.get("", response_model=list[WorkflowResponse])
async def list_workflows(request: Request) -> list[WorkflowResponse]:
    return [_to_response(inst) for inst in _state(request).workflow_manager.list_all()]


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(request: Request, workflow_id: str) -> WorkflowResponse:
    try:
        inst = _state(request).workflow_manager.get(workflow_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")  # noqa: B904
    return _to_response(inst)


@router.delete("/{workflow_id}", response_model=WorkflowResponse)
async def stop_workflow(request: Request, workflow_id: str) -> WorkflowResponse:
    try:
        inst = _state(request).workflow_manager.stop(workflow_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")  # noqa: B904
    return _to_response(inst)
