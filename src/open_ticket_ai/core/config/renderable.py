import uuid
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Registerable:
    def __init__(self, params: BaseModel, *args: Any, **kwargs: Any) -> None:
        pass


class RenderableConfig[ParamsT: BaseModel](BaseModel):
    model_config = ConfigDict(extra="allow")
    uid: str = Field(default_factory=lambda: uuid.uuid4().hex)
    id: str | None = None
    use: str = Field(default="open_ticket_ai.base.CompositePipe")
    injects: dict[str, str] = Field(default_factory=dict)
    params: ParamsT = Field(default_factory=dict)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if self.id is None:
            self.id = self.uid

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, RenderableConfig):
            return self.uid == other.uid
        return False

    def __hash__(self) -> int:
        return hash(self.uid)
