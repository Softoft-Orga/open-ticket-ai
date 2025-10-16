import uuid
from typing import Any, Self

from pydantic import Field, model_validator

from open_ticket_ai.core.base_model import StrictBaseModel


class RenderableConfig(StrictBaseModel):
    uid: str = Field(
        default_factory=lambda: uuid.uuid4().hex,
        description=(
            "Universally unique identifier for this renderable instance generated automatically if not provided."
        ),
    )
    id: str = Field(
        description=(
            "Human-readable identifier for this renderable used for referencing in configurations and dependencies."
        )
    )
    use: str = Field(
        default="open_ticket_ai.base.CompositePipe",
        description=(
            "Fully qualified class path of the renderable implementation to instantiate for this configuration."
        ),
    )
    injects: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Mapping of parameter names to dependency injection bindings for resolving constructor dependencies."
        ),
    )
    params: dict[str, Any] = Field(
        default_factory=dict,
        description="Dictionary of configuration parameters passed to the renderable instance during initialization.",
    )

    @model_validator(mode="after")
    def set_id_from_uid(self) -> Self:
        if self.id is None:
            self.id = self.uid
        return self

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, RenderableConfig) and self.uid == other.uid

    def __hash__(self) -> int:
        return hash(self.uid)
