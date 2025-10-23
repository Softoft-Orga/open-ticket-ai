from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, ValidationError
from pydantic.fields import Field, FieldInfo

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.injectables.injectable import Injectable

RENDER_FIELD_KEY = "render"


class TemplateRenderError(Exception):
    pass


# noinspection PyPep8Naming
def NoRender(field: FieldInfo) -> FieldInfo:
    extra = (field.json_schema_extra or {}) | {RENDER_FIELD_KEY: False}
    field.json_schema_extra = extra
    return field


# noinspection PyPep8Naming
def NoRenderField(**kwargs) -> FieldInfo:
    return NoRender(Field(**kwargs))


class TemplateRenderer[ParamsT: BaseModel = StrictBaseModel](Injectable[ParamsT], ABC):
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

    def render_to_model[T](self, to_model: type[BaseModel], from_raw_dict: dict[str, Any],
                           with_scope: dict[str, Any]) -> T:
        out = dict(from_raw_dict)
        for name, field in to_model.model_fields.items():
            if name in out and self._should_render_field(field):
                out[name] = self.render(out[name], with_scope)
        try:
            return to_model.model_validate(out)
        except ValidationError as e:
            raise TemplateRenderError("Failed to render template to model") from e

    @abstractmethod
    def _render(self, template_str: str, scope: dict[str, Any]) -> Any:
        pass
