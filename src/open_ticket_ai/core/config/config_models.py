from pathlib import Path
from typing import Any

import yaml

from open_ticket_ai.core.config.raw_config import RawRegisterableConfig, RenderedConfig


class RenderedOpenTicketAIConfig(RenderedConfig):
    imports: list[str] = []
    general_config: dict[str, dict[str, Any] | str | int | float | bool] = {}
    defs: dict[str, Any] = {}
    orchestrator: dict[str, Any] = {}


class OpenTicketAIConfig(RawRegisterableConfig[RenderedOpenTicketAIConfig]):
    imports: list[str] | str = []
    general_config: dict[str, dict[str, Any] | str | int | float | bool] | str = {}
    defs: dict[str, Any] | str = {}
    orchestrator: dict[str, Any] | str = {}


def load_config(path: str | Path) -> OpenTicketAIConfig:
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if "open_ticket_ai" not in data:
        raise ValueError("Config file must have 'open_ticket_ai' as root key")
    return OpenTicketAIConfig(**data["open_ticket_ai"])
