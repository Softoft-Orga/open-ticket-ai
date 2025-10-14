import uuid
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RenderableConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    uid: str = Field(default_factory=lambda: uuid.uuid4().hex)
    id: str
    use: str = Field(default="open_ticket_ai.base.CompositePipe")
    injects: dict[str, str] = Field(default_factory=dict)
    params: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def set_id_from_uid(self) -> Self:
        if self.id is None:
            self.id = self.uid
        return self

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, RenderableConfig) and self.uid == other.uid

    def __hash__(self) -> int:
        return hash(self.uid)
