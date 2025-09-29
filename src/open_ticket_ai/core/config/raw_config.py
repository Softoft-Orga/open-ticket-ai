from typing import Any, ClassVar, Generic, TypeVar, cast

from pydantic import BaseModel

from open_ticket_ai.core.config.jinja2_env import render_recursive


RenderedConfigT = TypeVar("RenderedConfigT", bound=BaseModel)


class RawConfig(BaseModel, Generic[RenderedConfigT]):
    rendered_model_type: ClassVar[type[RenderedConfigT] | None] = None

    def _render_model_dump(self) -> dict[str, Any]:
        return self.model_dump()

    def _post_render_transform(self, rendered: Any) -> Any:
        return rendered

    def render(self, scope: dict[str, Any] | BaseModel) -> RenderedConfigT:
        rendered_data = self._post_render_transform(render_recursive(self._render_model_dump(), scope))
        rendered_model = self.rendered_model_type

        if rendered_model is not None and not isinstance(rendered_data, rendered_model):
            return rendered_model.model_validate(rendered_data)

        return cast(RenderedConfigT, rendered_data)
