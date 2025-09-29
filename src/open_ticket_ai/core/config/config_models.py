from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class RawOpenTicketAIConfig(BaseModel):
    plugins: list[str] = []
    general_config: dict[str, dict[str, Any] | Any] = {}
    defs: list[dict[str, Any]] = []
    orchestrator: list[dict[str, Any]] = []


def load_config(path: str | Path) -> RawOpenTicketAIConfig:
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if "open_ticket_ai" not in data:
        raise ValueError("Config file must have 'open_ticket_ai' as root key")
    return RawOpenTicketAIConfig(**data["open_ticket_ai"])
