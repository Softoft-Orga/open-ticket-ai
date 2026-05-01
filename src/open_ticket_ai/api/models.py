"""Request and response models for the REST API."""

from __future__ import annotations

import datetime
from typing import Any

from pydantic import BaseModel, Field

from open_ticket_ai.workflow_manager import WorkflowStatus

# ── Ticket models ────────────────────────────────────────────────


class EntityBody(BaseModel):
    id: str | None = None
    name: str | None = None


class NoteBody(BaseModel):
    subject: str = ""
    body: str = ""
    content_type: str | None = "text/plain"


class TicketCreateRequest(BaseModel):
    subject: str | None = None
    body: str | None = None
    queue: EntityBody | None = None
    priority: EntityBody | None = None
    customer: EntityBody | None = None


class TicketUpdateRequest(BaseModel):
    subject: str | None = None
    body: str | None = None
    queue: EntityBody | None = None
    priority: EntityBody | None = None
    customer: EntityBody | None = None


class TicketSearchRequest(BaseModel):
    queue: EntityBody | None = None
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class TicketResponse(BaseModel):
    id: str | None = None
    subject: str | None = None
    body: str | None = None
    queue: EntityBody | None = None
    priority: EntityBody | None = None
    customer: EntityBody | None = None
    notes: list[NoteBody] | None = None


# ── Workflow models ──────────────────────────────────────────────


class TemplateParameterSchema(BaseModel):
    name: str
    type: str = "string"
    description: str = ""
    default: Any = None
    required: bool = False


class WorkflowTemplateResponse(BaseModel):
    name: str
    description: str
    parameters: list[TemplateParameterSchema]


class WorkflowStartRequest(BaseModel):
    template_name: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class WorkflowResponse(BaseModel):
    workflow_id: str
    template_name: str
    parameters: dict[str, Any]
    status: WorkflowStatus
    started_at: datetime.datetime
    stopped_at: datetime.datetime | None = None
    error: str | None = None


# ── Pipeline descriptor models ──────────────────────────────────


class PipeDescriptor(BaseModel):
    pipe_id: str
    kind: str
    role: str | None = None
    children: list[PipeDescriptor] = Field(default_factory=list)


PipeDescriptor.model_rebuild()


# ── Classification models ───────────────────────────────────────


class ClassifyRequest(BaseModel):
    text: str = Field(description="Text to classify")
    model_name: str = Field(description="HuggingFace model repo name")


class ClassifyResponse(BaseModel):
    label: str = Field(description="Predicted label")
    confidence: float = Field(description="Prediction confidence (0-1)")


# ── Settings models ─────────────────────────────────────────────


class SettingsFieldInfo(BaseModel):
    type: str
    description: str
    default: Any = None
    restart_required: bool
    category: str
    secret: bool = False


class SettingsResponse(BaseModel):
    settings: dict[str, Any]
    schema_info: dict[str, SettingsFieldInfo]


class SettingsUpdateRequest(BaseModel):
    settings: dict[str, Any]


class SettingsUpdateResponse(BaseModel):
    settings: dict[str, Any]
    updated_fields: list[str]
