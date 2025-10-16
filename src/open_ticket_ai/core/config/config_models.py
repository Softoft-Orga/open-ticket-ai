from __future__ import annotations

from pydantic import Field

from open_ticket_ai.core.base_model import OpenTicketAIBaseModel
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.orchestration.orchestrator_models import OrchestratorConfig
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig


class InfrastructureConfig(OpenTicketAIBaseModel):
    logging: LoggingConfig = Field(
        default_factory=LoggingConfig,
        description="Configuration for application logging including level, format, and output destination."
    )
    default_template_renderer: str = Field(
        description="Name of the default template renderer to use for rendering templates across the application."
    )


class RawOpenTicketAIConfig(OpenTicketAIBaseModel):
    plugins: list[str] = Field(
        default_factory=list,
        description="List of plugin module paths to load and enable for extending application functionality."
    )
    infrastructure: InfrastructureConfig = Field(
        default_factory=InfrastructureConfig,
        description="Infrastructure-level configuration including logging and template rendering settings."
    )
    services: list[RenderableConfig] = Field(
        default_factory=list,
        description="List of service configurations defining available ticket system integrations and other services."
    )
    orchestrator: OrchestratorConfig = Field(
        default_factory=OrchestratorConfig,
        description="Orchestrator configuration defining runners, triggers, and pipeline execution workflow."
    )
