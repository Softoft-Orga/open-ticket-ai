from abc import ABC, abstractmethod
from typing import Any, final

from pydantic import BaseModel

from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.util.formatting import prettify


class TemplateRenderer[ParamsT: BaseModel](Injectable, ABC):
    @final
    def render(self, obj: Any, scope: dict[str, Any]) -> Any:
        self._logger.info(f"Rendering {obj}")
        self._logger.info(f"Scope: {prettify(scope)}")

        if isinstance(obj, str):
            return self._render(obj, scope)
        if isinstance(obj, list):
            return [self.render(item, scope) for item in obj]
        if isinstance(obj, dict):
            return {k: self.render(v, scope) for k, v in obj.items()}
        raise ValueError(f"Cannot render object of type {type(obj)}")

    @abstractmethod
    def _render(self, template_str: str, scope: dict[str, Any]) -> Any:
        pass
