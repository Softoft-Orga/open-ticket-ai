from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.pipeline.pipe_models import PipeConfig
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig


class TriggerConfig(RenderableConfig):
    pass


class RunnerDefinition(BaseModel):
    id: str | None = None
    on: list[TriggerConfig]
    run: PipeConfig
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
    runners: list[RunnerDefinition] = Field(default_factory=list)
