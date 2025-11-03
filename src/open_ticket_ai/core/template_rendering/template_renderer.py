from abc import ABC, abstractmethod
from typing import Any, cast

from pydantic import BaseModel, ValidationError
from pydantic.fields import Field, FieldInfo

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.injectables.injectable import Injectable

RENDER_FIELD_KEY = "render"


class TemplateRenderError(Exception):
    pass


# noinspection PyPep8Naming
def NoRender(field: FieldInfo) -> FieldInfo:
    extra = field.json_schema_extra
    extra_dict = dict(extra) if isinstance(extra, dict) else {}
    extra_dict[RENDER_FIELD_KEY] = False
    field.json_schema_extra = extra_dict
    return field


# noinspection PyPep8Naming
def NoRenderField(**kwargs: Any) -> FieldInfo:
    extra = kwargs.get("json_schema_extra")
    extra_dict = dict(extra) if isinstance(extra, dict) else {}
    extra_dict[RENDER_FIELD_KEY] = False
    kwargs["json_schema_extra"] = extra_dict
    return Field(**kwargs)

class TemplateRenderer[ParamsT: BaseModel = StrictBaseModel](Injectable[ParamsT], ABC):
    @classmethod
    def _should_render_field(cls, field: FieldInfo) -> bool:
        extra = field.json_schema_extra
        if isinstance(extra, dict):
            value = extra.get(RENDER_FIELD_KEY, True)
            return bool(value)
        return True

    async def render(self, obj: Any, scope: dict[str, Any]) -> Any:
        if isinstance(obj, str):
            return await self._render(obj, scope)
        if isinstance(obj, list):
            return [await self.render(i, scope) for i in obj]
        if isinstance(obj, dict):
            return {k: await self.render(v, scope) for k, v in obj.items()}
        return obj

    async def render_to_model[T](
        self, to_model: type[BaseModel], from_raw_dict: dict[str, Any], with_scope: dict[str, Any]
    ) -> T:
        self._logger.debug(f"Rendering to model {to_model.__name__} with scope keys: {list(with_scope.keys())}")
        out = dict(from_raw_dict)
        for name, field in to_model.model_fields.items():
            self._logger.debug(f"Checking field {name} should render: {self._should_render_field(field)}")
            if name in out and self._should_render_field(field):
                self._logger.debug(f"Rendering field {name}")
                out[name] = await self.render(out[name], with_scope)
        try:
            return cast(T, to_model.model_validate(out))
        except ValidationError as e:
            raise TemplateRenderError("Failed to render template to model") from e

    @abstractmethod
    async def _render(self, template_str: str, scope: dict[str, Any]) -> Any:
        pass
