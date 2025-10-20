from abc import ABC, abstractmethod
from typing import Any, final

from pydantic import BaseModel

from open_ticket_ai.core.injectables.injectable import Injectable


class TemplateRenderer[ParamsT: BaseModel](Injectable, ABC):
    @final
    def render(self, obj: Any, scope: dict[str, Any]) -> Any:
        if isinstance(obj, str):
            self._logger.debug(f"Rendering template string: {obj} with scope: {scope}")

            return self._render(obj, scope)
        if isinstance(obj, list):
            return [self.render(item, scope) for item in obj]
        if isinstance(obj, dict):
            return {k: self.render(v, scope) for k, v in obj.items()}
        return obj

    @abstractmethod
    def _render(self, template_str: str, scope: dict[str, Any]) -> Any:
        pass
