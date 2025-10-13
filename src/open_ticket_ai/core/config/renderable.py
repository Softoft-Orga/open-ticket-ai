import uuid
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic_core import core_schema


class Renderable:
    """Marker interface for renderable configurations."""

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        pass


class EmptyParams(BaseModel):
    model_config = ConfigDict(extra="allow")

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, dict):
            return self.model_dump() == other
        return super().__eq__(other)


class RenderableConfig[ParamsT: BaseModel](BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    uid: str = Field(default_factory=lambda: uuid.uuid4().hex)
    id: str | None = None
    use: str = Field(default="open_ticket_ai.base.CompositePipe")
    injects: dict[str, str] = Field(default_factory=dict)
    params: ParamsT = Field(default_factory=EmptyParams)  # type: ignore[assignment]

    @model_validator(mode="before")
    @classmethod
    def handle_dict_params(cls, values: Any) -> Any:
        import warnings
        
        if not isinstance(values, dict):
            return values
        
        # Convert dict params to EmptyParams immediately
        if "params" in values and isinstance(values["params"], dict):
            values["params"] = EmptyParams(**values["params"])
        
        # Handle backwards compatibility: migrate extra fields to params
        known_fields = {"uid", "id", "use", "injects", "params", "if", "if_", "depends_on", "steps"}
        extra_fields = {k: v for k, v in values.items() if k not in known_fields}
        
        if extra_fields:
            field_names = ", ".join(extra_fields.keys())
            
            # If params already provided, just warn and discard extra fields
            if "params" in values:
                warnings.warn(
                    f"Ignoring fields {field_names} when params is provided. "
                    f"Use params={{...}} instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                # Remove extra fields from top level
                for k in extra_fields:
                    values.pop(k, None)
            else:
                # Warn about deprecated usage and migrate extra fields to params
                warnings.warn(
                    f"Passing fields {field_names} directly to config is deprecated. "
                    f"Use params={{...}} instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                # Migrate extra fields to params as EmptyParams
                values["params"] = EmptyParams(**extra_fields)
                # Remove extra fields from top level
                for k in extra_fields:
                    values.pop(k, None)
        
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
