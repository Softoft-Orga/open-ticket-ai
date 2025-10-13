import uuid
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Renderable:
    """Marker interface for renderable configurations."""
    pass


class EmptyParams(BaseModel):
    model_config = ConfigDict(extra="allow")
    pass


class RenderableConfig[ParamsT: BaseModel](BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    uid: str = Field(default_factory=lambda: uuid.uuid4().hex)
    id: str | None = None
    use: str = Field(default="open_ticket_ai.base.CompositePipe")
    injects: dict[str, str] = Field(default_factory=dict)
    params: ParamsT = Field(default_factory=EmptyParams)  # type: ignore[assignment]

    @model_validator(mode="after")
    def set_id_from_uid(self) -> Self:
        if self.id is None:
            self.id = self.uid
        return self

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, RenderableConfig):
            return self.uid == other.uid
        return False

    def __hash__(self) -> int:
        return hash(self.uid)
