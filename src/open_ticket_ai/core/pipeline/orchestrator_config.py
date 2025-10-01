from __future__ import annotations

from typing import Any, Iterable

from pydantic import BaseModel, ConfigDict, Field


class RunnerDefinition(BaseModel):
    """Configuration for a scheduled pipeline runner."""

    run_every_milli_seconds: int = Field(..., ge=1)
    pipe: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True)

    @property
    def interval_seconds(self) -> float:
        """Return the configured interval as seconds."""
        return self.run_every_milli_seconds / 1000.0

    @property
    def pipe_id(self) -> str:
        """Return the configured pipe identifier if available."""
        pipe_id = self.pipe.get("id")
        if pipe_id:
            return str(pipe_id)
        return "pipe"


class OrchestratorConfig(BaseModel):
    """Typed representation of orchestrator configuration entries."""

    runners: list[RunnerDefinition] = Field(default_factory=list)

    @classmethod
    def from_raw(cls, raw_config: Iterable[dict[str, Any]] | None) -> "OrchestratorConfig":
        if not raw_config:
            return cls()
        runners = [RunnerDefinition.model_validate(entry) for entry in raw_config]
        return cls(runners=runners)
