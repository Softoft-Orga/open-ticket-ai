import uuid
import warnings
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Renderable:
    def __init__(self, params: BaseModel, *args: Any, **kwargs: Any) -> None:
        pass


class EmptyParams(BaseModel):
    pass


class RenderableConfig[ParamsT: BaseModel](BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    uid: str = Field(default_factory=lambda: uuid.uuid4().hex)
    id: str | None = None
    use: str = Field(default="open_ticket_ai.base.CompositePipe")
    injects: dict[str, str] = Field(default_factory=dict)
    params: ParamsT = Field(default_factory=EmptyParams)  # type: ignore[assignment]

    @field_validator("params", mode="wrap")
    @classmethod
    def validate_params(cls, v: Any, handler: Any) -> Any:
        if isinstance(v, dict):
            type_args = getattr(cls, "__pydantic_generic_metadata__", {}).get("args", ())
            if type_args and len(type_args) > 0:
                param_type = type_args[0]
                if param_type is not BaseModel and issubclass(param_type, BaseModel):
                    try:
                        return param_type.model_validate(v)
                    except Exception:
                        pass
            return v
        return handler(v)

    @model_validator(mode="before")
    @classmethod
    def migrate_legacy_fields_to_params(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        control_fields = {"uid", "id", "use", "injects", "params", "if", "if_", "depends_on", "steps"}

        params_dict = data.get("params", {})
        if not isinstance(params_dict, dict):
            return data

        legacy_fields = {}
        for key in list(data.keys()):
            if key not in control_fields:
                legacy_fields[key] = data.pop(key)

        if legacy_fields:
            if params_dict:
                warnings.warn(
                    f"Both 'params' dict and top-level fields found. "
                    f"Top-level fields will be ignored: {', '.join(legacy_fields.keys())}",
                    DeprecationWarning,
                    stacklevel=3,
                )
            else:
                warnings.warn(
                    f"Passing parameters as top-level fields is deprecated. "
                    f"Use 'params' dict instead. Found: {', '.join(legacy_fields.keys())}",
                    DeprecationWarning,
                    stacklevel=3,
                )
                data["params"] = legacy_fields

        return data

    @model_validator(mode="after")
    def set_id_from_uid(self) -> "RenderableConfig[ParamsT]":
        if self.id is None:
            self.id = self.uid
        return self

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, RenderableConfig):
            return self.uid == other.uid
        return False

    def __hash__(self) -> int:
        return hash(self.uid)
