from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.config.logging_config_models import LoggingDictConfig
from open_ticket_ai.core.orchestration.orchestrator_models import OrchestratorConfig
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig


class InfrastructureConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    logging: LoggingDictConfig = Field(default_factory=LoggingDictConfig)
    default_template_renderer: str


class RawOpenTicketAIConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    plugins: list[str] = Field(default_factory=list)
    infrastructure: InfrastructureConfig = Field(default_factory=InfrastructureConfig)
    services: list[RenderableConfig] = Field(default_factory=list)
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)
