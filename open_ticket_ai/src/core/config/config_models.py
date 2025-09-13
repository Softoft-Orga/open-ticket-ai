# FILE_PATH: open_ticket_ai\src\ce\core\config\config_models.py
# In open_ticket_ai/src/ce/core/config/config_models.py

from typing import Any, Self, Literal

from pydantic import BaseModel, Field, model_validator

Unit = Literal["seconds", "minutes", "hours", "days", "weeks"]


class ProvidableConfig(BaseModel):
    """Base configuration for registry instances (system, pipe)."""
    id: str = Field(..., min_length=1, description="Unique identifier for the instance.")
    params: dict[str, Any] = Field(default_factory=dict)
    provider_key: str = Field(..., min_length=1, description="Key identifying the provider implementation.")


class SystemConfig(ProvidableConfig):
    """Configuration for the ticket system adapter."""
    pass


class PipeConfig(ProvidableConfig):
    """Generic configuration for any pipe (fetcher, preparer, inference, modifier, etc.)."""
    pass


class ScheduleConfig(BaseModel):
    """Configuration for scheduling pipeline execution."""
    interval: int = Field(..., gt=0, description="Numeric interval for scheduling.")
    unit: Unit = Field(..., description="Time unit for the interval.")

class PipelineConfig(BaseModel):
    """Configuration for a single pipeline workflow."""
    id: str = Field(..., min_length=1, description="Unique identifier for the pipeline.")
    schedule: ScheduleConfig = Field(..., description="Schedule configuration for periodic execution.")
    pipes: list[str] = Field(
        ...,
        min_length=1,
        description="Ordered list of pipe IDs to execute.",
    )

    def validate_pipes_are_registered(self, all_pipe_ids: set[str]) -> None:
        for pid in self.pipes:
            if pid not in all_pipe_ids:
                raise ValueError(f"Pipeline '{self.id}' references unknown pipe '{pid}'")


class OpenTicketAIConfig(BaseModel):
    """Root configuration model for Open Ticket AI."""
    system: SystemConfig
    pipes: list[PipeConfig] = Field(..., min_length=1)
    pipelines: list[PipelineConfig] = Field(..., min_length=1)

    @model_validator(mode="after")
    def cross_validate_references(self) -> Self:
        all_pipe_ids = {p.id for p in self.pipes}
        for pipeline in self.pipelines:
            pipeline.validate_pipes_are_registered(all_pipe_ids)
        return self

    def get_all_register_instance_configs(self) -> list[ProvidableConfig]:
        """Return all registered instances in the configuration.

        Returns:
            list[ProvidableConfig]: A list of all registered instance configurations.
        """
        return (
            [self.system] +
            self.pipes
        )


def load_config(path: str) -> OpenTicketAIConfig:
    """Load YAML config with root key 'open_ticket_ai'."""
    import yaml

    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if "open_ticket_ai" not in data:
        raise KeyError("Missing 'open_ticket_ai' root key")

    return OpenTicketAIConfig(**data["open_ticket_ai"])
