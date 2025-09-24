# FILE_PATH: open_ticket_ai\src\ce\core\config\config_models.py
# In open_ticket_ai/src/ce/core/config/config_models.py
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from open_ticket_ai.src.base.otobo_integration.otobo_adapter_config import OTOBOAdapterConfig
from open_ticket_ai.src.core.config.pipe_configs import PipesConfig


class SystemConfig(BaseModel):
    """Configuration for the ticket system connection."""
    server_address: str
    webservice_name: str
    search_operation_url: str
    update_operation_url: str
    get_operation_url: str
    username: str
    password_env_var: str


class OrchestratorConfig(BaseModel):
    """Configuration for the main orchestrator."""
    run_every_milli_seconds: int = Field(..., gt=0)


class PipelineConfig(BaseModel):
    """Defines a single pipeline's execution flow and schedule."""
    id: str
    schedule: dict[str, Any]
    pipes: list[str]


class OpenTicketAIConfig(BaseModel):
    """Root configuration model for Open Ticket AI."""

    system: OTOBOAdapterConfig
    orchestrator: OrchestratorConfig
    pipes: PipesConfig
    logging: dict[str, Any] = Field(default_factory=dict)


def load_config(path: str | Path) -> OpenTicketAIConfig:
    """Load YAML config with root key 'open_ticket_ai'."""
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if "open_ticket_ai" not in data:
        raise KeyError("Missing 'open_ticket_ai' root key in YAML configuration.")

    return OpenTicketAIConfig(**data["open_ticket_ai"])
