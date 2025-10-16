from __future__ import annotations

from pydantic import BaseModel, Field

from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.orchestration.orchestrator_models import OrchestratorConfig
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig


class InfrastructureConfig(BaseModel):
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    default_template_renderer: str


class RawOpenTicketAIConfig(BaseModel):
    plugins: list[str] = Field(default_factory=list)
    infrastructure: InfrastructureConfig = Field(default_factory=InfrastructureConfig)
    services: list[RenderableConfig] = Field(default_factory=list)
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)
