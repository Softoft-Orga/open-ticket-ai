from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from open_ticket_ai.core.config.renderable import RenderableConfig
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig


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
    on: list[TriggerDefinition] = Field(default_factory=list, alias="on")
    run: PipeConfig
    params: RunnerParams = Field(default_factory=RunnerParams)

    model_config = ConfigDict(populate_by_name=True)

    @property
    def pipe_id(self) -> str:
        if self.id:
            return self.id
        pipe_id = self.run.id
        if pipe_id:
            return str(pipe_id)
        pipe_dict = self.run.model_dump()
        return "pipe-" + hex(hash(frozenset(pipe_dict.items())) & 0xFFFFFFFF)[2:]


class OrchestratorConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    defaults: dict[str, Any] | None = None
    runners: list[RunnerDefinition] = Field(default_factory=list)

    @model_validator(mode="after")
    def merge_defaults(self):
        if self.defaults:
            for runner in self.runners:
                if "run" in self.defaults:
                    run_defaults = self.defaults["run"]
                    runner.run = runner.run.model_copy(update=run_defaults)
                if "params" in self.defaults:
                    params_defaults = self.defaults["params"]
                    if runner.params:
                        runner.params = runner.params.model_copy(update=params_defaults)
                    else:
                        runner.params = RunnerParams.model_validate(params_defaults)
        return self
