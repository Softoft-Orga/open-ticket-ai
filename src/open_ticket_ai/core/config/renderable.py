import uuid
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Renderable:
    """Marker interface for renderable configurations."""

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        pass


class EmptyParams(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, dict):
            return self.model_dump() == other
        return super().__eq__(other)

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.model_dump().items())))


class RenderableConfig(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    uid: str = Field(default_factory=lambda: uuid.uuid4().hex)
    id: str | None = None
    use: str = Field(default="open_ticket_ai.base.CompositePipe")
    injects: dict[str, str] = Field(default_factory=dict)
    params: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def handle_dict_params(cls, values: Any) -> Any:
        if not isinstance(values, dict):
            return values

        # Ensure params is always a dict
        if "params" in values:
            if isinstance(values["params"], BaseModel):
                values["params"] = values["params"].model_dump()
            elif not isinstance(values["params"], dict):
                values["params"] = {}

        return values

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
