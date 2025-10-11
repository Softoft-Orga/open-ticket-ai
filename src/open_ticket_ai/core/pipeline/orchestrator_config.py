from __future__ import annotations

import warnings
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from open_ticket_ai.core.pipeline.pipe_config import RawPipeConfig


class TriggerDefinition(BaseModel):
    id: str
    use: str
    params: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True)


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


class RunnerSettings(BaseModel):
    concurrency: ConcurrencySettings | None = None
    retry: RetrySettings | None = None
    timeout: str | None = None
    retry_scope: str = Field(default="pipeline")
    priority: int = Field(default=10)

    model_config = ConfigDict(populate_by_name=True)


class RunnerDefinition(BaseModel):
    id: str | None = None
    triggers: list[TriggerDefinition] = Field(default_factory=list, alias="on")
    pipe: RawPipeConfig = Field(default_factory=RawPipeConfig)
    settings: RunnerSettings = Field(default_factory=RunnerSettings)

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def migrate_legacy_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        if "run_every_milli_seconds" in data:
            warnings.warn(
                "Deprecated: 'run_every_milli_seconds' field is deprecated. "
                "Use 'triggers' or 'on' field with trigger definitions instead. "
                "Auto-migrating for backwards compatibility, but this will be removed in a future version.",
                DeprecationWarning,
                stacklevel=4,
            )

            interval_ms = data.pop("run_every_milli_seconds")
            interval_seconds = interval_ms / 1000.0

            if "triggers" not in data and "on" not in data:
                data["triggers"] = [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": int(interval_seconds)},
                    }
                ]

        return data

    @property
    def pipe_id(self) -> str:
        if self.id:
            return self.id
        pipe_id = self.pipe.id
        if pipe_id:
            return str(pipe_id)
        pipe_dict = self.pipe.model_dump()
        return "pipe-" + hex(hash(frozenset(pipe_dict.items())) & 0xFFFFFFFF)[2:]


class OrchestratorConfig(BaseModel):
    runners: list[RunnerDefinition] = Field(default_factory=list)
