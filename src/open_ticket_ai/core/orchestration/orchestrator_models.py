from __future__ import annotations

from pydantic import ConfigDict, Field

from open_ticket_ai.core.base_model import OpenTicketAIBaseModel
from open_ticket_ai.core.pipeline.pipe_models import PipeConfig
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig


class TriggerConfig(RenderableConfig):
    pass


class RunnerDefinition(OpenTicketAIBaseModel):
    model_config = ConfigDict(populate_by_name=True, frozen=True, extra="forbid")

    id: str | None = Field(
        default=None,
        description=(
            "Optional unique identifier for this runner; "
            "if not provided, a default ID will be generated from the pipe configuration."
        ),
    )
    on: list[TriggerConfig] = Field(
        description="List of trigger configurations that determine when this runner should execute its pipeline."
    )
    run: PipeConfig = Field(
        description="Pipeline configuration defining the sequence of operations to execute when triggered."
    )

    def get_id(self) -> str:
        if self.id is not None:
            return self.id
        return f"runner.{self.run.id}"


class OrchestratorConfig(OpenTicketAIBaseModel):
    runners: list[RunnerDefinition] = Field(
        default_factory=list,
        description="List of runner definitions that specify the triggers and pipelines managed by the orchestrator.",
    )
