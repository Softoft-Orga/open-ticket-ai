from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel


class PipeConfig(BaseModel):
    id: str
    use: str
    config: dict[str, Any] = {}
    when: str = "True"
    on_failure: Literal["continue", "finish_container", "fail_container"] = "fail_container"
    on_success: Literal["continue", "finish_container", "fail_container"] = "continue"
    steps: list["PipeConfig"] = []


class SystemConfig(BaseModel):
    id: str
    provider_key: str
    config: dict[str, Any] = {}


class OpenTicketAIConfig(BaseModel):
    version: str = "1.0.0"
    plugins: list[str] = []
    general_config: dict[str, Any] = {}
    defs: dict[str, Any] = {}
    orchestrator: dict[str, Any] = {}
    system: SystemConfig | None = None
    pipe: PipeConfig | None = None
    interval_seconds: float = 60.0


def load_config(path: str | Path) -> OpenTicketAIConfig:
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if "open_ticket_ai" not in data:
        raise ValueError("Config file must have 'open_ticket_ai' as root key")
    return OpenTicketAIConfig(**data["open_ticket_ai"])
