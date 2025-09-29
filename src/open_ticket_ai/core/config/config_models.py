from pathlib import Path
from typing import Any

import yaml

from open_ticket_ai.core.config.raw_config import RawRegisterableConfig, RenderedConfig, RawConfig, RenderableConfig, \
    RenderedRegistrableConfig


class RenderedOpenTicketAIConfig(RenderedConfig):
    imports: list[str] = []
    general_config: dict[str, dict[str, Any] | str | int | float | bool] = {}
    defs: list[RenderedRegistrableConfig] = []
    orchestrator: dict[str, Any] = {}


class RawOpenTicketAIConfig(RawConfig):
    imports: list[str] | str = []
    general_config: dict[str, dict[str, Any] | str | int | float | bool] | str = {}
    defs: dict[str, list[dict | str]] | str = {}
    orchestrator: dict[str, Any] | str = {}


class OpenTicketAIConfig(RenderableConfig[RawOpenTicketAIConfig, RenderedOpenTicketAIConfig]):
    pass

def load_config(path: str | Path) -> RawOpenTicketAIConfig:
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if "open_ticket_ai" not in data:
        raise ValueError("Config file must have 'open_ticket_ai' as root key")
    return RawOpenTicketAIConfig(**data["open_ticket_ai"])
