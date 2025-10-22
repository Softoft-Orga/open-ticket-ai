from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from pydantic.fields import FieldInfo

RENDER_FIELD_KEY = "render"


def NoRender(field: FieldInfo) -> FieldInfo:
    extra = (field.json_schema_extra or {}) | {RENDER_FIELD_KEY: False}
    field.json_schema_extra = extra
    return field


class TemplateRenderer[ParamsT: BaseModel](ABC):
    def __init__(self, logger):
        self._logger = logger

    @classmethod
    def _should_render_field(cls, field: FieldInfo) -> bool:
        return (field.json_schema_extra or {}).get(RENDER_FIELD_KEY, True)

    def render(self, obj: Any, scope: dict[str, Any]) -> Any:
        if isinstance(obj, str):
            return self._render(obj, scope)
        if isinstance(obj, list):
            return [self.render(i, scope) for i in obj]
        if isinstance(obj, dict):
            return {k: self.render(v, scope) for k, v in obj.items()}
        return obj

    def render_to_model[T](self, model_cls: type[T], raw: dict[str, Any], scope: dict[str, Any]) -> T:
        out: dict[str, Any] = {}
        for name, field in model_cls.model_fields.items():
            if name in raw:
                v = raw[name]
                out[name] = self.render(v, scope) if self._should_render_field(field) else v
        for k, v in raw.items():
            if k not in out:
                out[k] = v
        return model_cls.model_validate(out)

    @abstractmethod
    def _render(self, template_str: str, scope: dict[str, Any]) -> Any:
        pass
