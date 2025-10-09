from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.config.registerable import RegisterableConfig
from open_ticket_ai.core.pipeline import OrchestratorConfig
from open_ticket_ai.core.template_rendering import TemplateRendererConfig


class GeneralConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    logging: dict[str, Any] = {}
    template_renderer: TemplateRendererConfig = {}

class RawOpenTicketAIConfig(BaseModel):
    plugins: list[str] = Field(default_factory=lambda: [])
    general_config: GeneralConfig = Field(default_factory=GeneralConfig)
    defs: list[RegisterableConfig] = Field(default_factory=lambda: [])
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)


def load_config(path: str | Path, app_config: "AppConfig | None" = None) -> RawOpenTicketAIConfig:
    from open_ticket_ai.core.config.app_config import AppConfig

    if app_config is None:
        app_config = AppConfig()

    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if app_config.config_yaml_root_key not in data:
        raise ValueError(f"Config file must have '{app_config.config_yaml_root_key}' as root key")
    return RawOpenTicketAIConfig(**data[app_config.config_yaml_root_key])
