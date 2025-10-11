import uuid
from typing import Any, Union, get_args, get_origin

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Renderable[ParamsT: BaseModel](BaseModel):
    model_config = ConfigDict(extra="allow")
    uid: str = Field(default_factory=lambda: uuid.uuid4().hex)
    id: str | None = None
    use: str = Field(default="open_ticket_ai.base.CompositePipe")
    injects: dict[str, str] = Field(default_factory=dict)
    params: dict[str, Any] | ParamsT = Field(default_factory=dict)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if self.id is None:
            self.id = self.uid

    @model_validator(mode="before")
    @classmethod
    def _validate_params(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        if "params" in data and isinstance(data["params"], dict):
            # Get the params field annotation
            params_field = cls.__pydantic_fields__.get("params")
            if params_field and params_field.annotation:
                annotation = params_field.annotation
                # Extract the ParamsT type from Union[dict[str, Any], ParamsT]
                if get_origin(annotation) is Union:
                    args = get_args(annotation)
                    # Find the non-dict type
                    for arg in args:
                        if arg is not dict and get_origin(arg) is not dict:
                            # Try to validate as the typed model
                            try:
                                data["params"] = arg.model_validate(data["params"])
                                break
                            except Exception:
                                # Keep as dict for backward compatibility
                                pass

        return data

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Renderable):
            return self.uid == other.uid
        return False

    def __hash__(self) -> int:
        return hash(self.uid)


class Registerable:
    def __init__(self, params: BaseModel | dict[str, Any], *args: Any, **kwargs: Any) -> None:
        pass


class RegisterableConfig(Renderable[BaseModel]):
    pass
