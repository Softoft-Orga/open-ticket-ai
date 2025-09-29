from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel

from open_ticket_ai.core.config.raw_config import RawConfig
from open_ticket_ai.core.pipeline.base_pipe_config import RawPipeConfig, RenderedPipeConfig


class RenderedOrchestratorRunnerConfig(BaseModel):
    run_every_milli_seconds: int
    pipe: RenderedPipeConfig


class OrchestratorRunnerConfig(RawConfig[RenderedOrchestratorRunnerConfig]):
    run_every_milli_seconds: int
    pipe: RawPipeConfig


class RenderedSystemConfig(BaseModel):
    id: str
    provider_key: str
    config: dict[str, Any] = {}


class SystemConfig(RawConfig[RenderedSystemConfig]):
    id: str
    provider_key: str
    config: dict[str, Any] = {}


class RenderedOpenTicketAIConfig(BaseModel):
    version: str = "1.0.0"
    plugins: list[str] = []
    general_config: dict[str, Any] = {}
    defs: dict[str, Any] = {}
    orchestrator: list[RenderedOrchestratorRunnerConfig] = []
    system: RenderedSystemConfig | None = None
    pipe: Any | None = None  # Will be RenderedPipeConfig[Any]
    interval_seconds: float = 60.0


class OpenTicketAIConfig(RawConfig[RenderedOpenTicketAIConfig]):
    version: str = "1.0.0"
    plugins: list[str] = []
    general_config: dict[str, Any] = {}
    defs: dict[str, Any] = {}
    orchestrator: list[OrchestratorRunnerConfig] = []
    system: SystemConfig | None = None
    pipe: Any | None = None  # Will be PipeConfig[Any]
    interval_seconds: float = 60.0


def load_config(path: str | Path) -> OpenTicketAIConfig:
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if "open_ticket_ai" not in data:
        raise ValueError("Config file must have 'open_ticket_ai' as root key")
    return OpenTicketAIConfig(**data["open_ticket_ai"])
