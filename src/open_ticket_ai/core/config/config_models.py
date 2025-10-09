from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.config.registerable import RegisterableConfig
from open_ticket_ai.core.pipeline import OrchestratorConfig
from open_ticket_ai.core.template_rendering import TemplateRendererConfig, JinjaRendererConfig


class GeneralConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    logging: dict[str, Any] = {}
    template_renderer: TemplateRendererConfig = Field(default_factory=JinjaRendererConfig)

class RawOpenTicketAIConfig(BaseModel):
    plugins: list[str] = Field(default_factory=lambda: [])
    general_config: GeneralConfig = Field(default_factory=GeneralConfig)
    defs: list[RegisterableConfig] = Field(default_factory=lambda: [])
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)


def load_config(path: str | Path) -> RawOpenTicketAIConfig:
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if "open_ticket_ai" not in data:
        raise ValueError("Config file must have 'open_ticket_ai' as root key")
    return RawOpenTicketAIConfig(**data["open_ticket_ai"])
