from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RunnerDefinition(BaseModel):
    run_every_milli_seconds: int = Field(..., ge=1)
    pipe: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True)

    @property
    def interval_seconds(self) -> float:
        return self.run_every_milli_seconds / 1000.0

    @property
    def pipe_id(self) -> str:
        pipe_id = self.pipe.get("id")
        if pipe_id:
            return str(pipe_id)
        return "pipe-" + hex(hash(frozenset(self.pipe.items())) & 0xFFFFFFFF)[2:]


class OrchestratorConfig(BaseModel):
    runners: list[RunnerDefinition] = Field(default_factory=list)
