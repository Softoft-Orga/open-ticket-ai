from __future__ import annotations

import logging
from typing import Any, Iterable

from pydantic import BaseModel, ConfigDict, Field


class RunnerDefinition(BaseModel):
    """Configuration for a scheduled pipeline runner."""

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
        return "pipe"


class OrchestratorConfig(BaseModel):
    runners: list[RunnerDefinition] = Field(default_factory=list)
    max_runners: int = Field(default=100, ge=1)

    @classmethod
    def from_raw(cls, raw_config: Iterable[dict[str, Any]] | None) -> OrchestratorConfig:
        logger = logging.getLogger("OrchestratorConfig")
        
        if not raw_config:
            return cls()
        
        raw_list = list(raw_config)
        runners = [RunnerDefinition.model_validate(entry) for entry in raw_list]
        
        pipe_ids = [r.pipe_id for r in runners]
        unique_pipe_ids = set(pipe_ids)
        if len(pipe_ids) != len(unique_pipe_ids):
            duplicates = [pid for pid in unique_pipe_ids if pipe_ids.count(pid) > 1]
            logger.warning(
                "Duplicate pipe IDs detected in orchestrator configuration: %s. "
                "This may result in multiple deployments for the same pipe.",
                duplicates
            )
        
        return cls(runners=runners)
