from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.config.renderable import RenderableConfig
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig


class EmptyTriggerDefinitionParams(BaseModel):
    model_config = ConfigDict(extra="allow")

    def __getitem__(self, key: str) -> Any:
        """Allow dict-style access to params for backward compatibility."""
        return getattr(self, key)


class TriggerDefinition[TriggerDefinitionParamsT: BaseModel](RenderableConfig[TriggerDefinitionParamsT]):
    pass


class ConcurrencySettings(BaseModel):
    max_workers: int = Field(default=1, ge=1)
    when_exhausted: str = Field(default="wait")

    model_config = ConfigDict(populate_by_name=True)


class RetrySettings(BaseModel):
    attempts: int = Field(default=3, ge=1)
    delay: str = Field(default="5s")
    backoff_factor: float = Field(default=2.0, ge=1.0)
    max_delay: str = Field(default="30s")
    jitter: bool = Field(default=True)

    model_config = ConfigDict(populate_by_name=True)


class RunnerParams(BaseModel):
    concurrency: ConcurrencySettings | None = None
    retry: RetrySettings | None = None
    timeout: str | None = None
    retry_scope: str = Field(default="pipeline")
    priority: int = Field(default=10)

    model_config = ConfigDict(populate_by_name=True)


class RunnerDefinition(BaseModel):
    id: str | None = None
    on: list[TriggerDefinition[EmptyTriggerDefinitionParams]]
    run: PipeConfig[Any]
    params: RunnerParams = Field(default_factory=RunnerParams)

    model_config = ConfigDict(populate_by_name=True)

    @property
    def pipe_id(self) -> str:
        if self.id is not None:
            return self.id
        if self.run.id is not None:
            return self.run.id
        return ""


class OrchestratorConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    defaults: dict[str, Any] | None = None
    runners: list[RunnerDefinition] = Field(default_factory=list)
