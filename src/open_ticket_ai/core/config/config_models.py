from pathlib import Path
from typing import Any, Dict, List, Annotated, Union

import yaml
from pydantic import BaseModel, Field

from open_ticket_ai.base.otobo_integration.otobo_adapter_config import OTOBOAdapterConfig
from open_ticket_ai.core.config.pipe_configs import ContextModifierConfig, HFLocalAIInferenceServiceConfig, \
    TicketSystemServiceConfig, SimpleKeyValueMapperConfig


class PipelineStepOutput(BaseModel):
    """Output configuration for a pipeline step."""

    data: Dict[str, Any] = Field(default_factory=dict)


class PipelineConfig(BaseModel):
    """Configuration for a pipeline."""

    id: str
    pipeline_config: Dict[str, Any]
    steps: list[Annotated[
        Union[
            TicketSystemServiceConfig,
            HFLocalAIInferenceServiceConfig,
            ContextModifierConfig,
            SimpleKeyValueMapperConfig,
        ],
        Field(discriminator="type"),
    ]]


class LoggingConfig(BaseModel):
    """Configuration for logging."""

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: Dict[str, Dict[str, str]]
    handlers: Dict[str, Dict[str, Any]]
    loggers: Dict[str, Dict[str, Any]]
    root: Dict[str, Any]


class SystemConfig(OTOBOAdapterConfig):
    """Configuration for the ticket system connection."""


class OrchestratorConfig(BaseModel):
    """Configuration for the main orchestrator."""

    run_every_milli_seconds: int = Field(..., gt=0)


class OpenTicketAIConfig(BaseModel):
    """Root configuration model for Open Ticket AI."""

    logging: LoggingConfig
    system: SystemConfig
    pipelines: List[PipelineConfig]
    orchestrator: OrchestratorConfig


def load_config(path: str | Path) -> OpenTicketAIConfig:
    """Load YAML config with root key 'open_ticket_ai'."""
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if "open_ticket_ai" not in data:
        raise KeyError("Missing 'open_ticket_ai' root key in YAML configuration.")

    return OpenTicketAIConfig(**data["open_ticket_ai"])
