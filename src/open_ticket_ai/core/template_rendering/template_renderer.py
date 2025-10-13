import ast
import json
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.logging_iface import LoggerFactory


class TemplateRenderer(ABC):
    def __init__(self, logger_factory: LoggerFactory) -> None:
        self._logger = logger_factory.get_logger(self.__class__.__name__)

    def _to_dict(self, scope: BaseModel | dict[str, Any]) -> dict[str, Any]:
        if isinstance(scope, BaseModel):
            return scope.model_dump()
        return scope

    def _parse_rendered_value(self, s: str) -> Any:
        if not s.strip():
            return s

        stripped = s.strip()

        try:
            return json.loads(s)
        except Exception as e:
            self._logger.debug(f"Failed to parse JSON: {str(e)}")

            if stripped.startswith(("[", "{", "(", '"', "'")):
                try:
                    return ast.literal_eval(s)
                except Exception as e:
                    self._logger.debug(f"Failed to parse literal: {str(e)}")

            return s

    @abstractmethod
    def render(self, template_str: str, scope: dict[str, Any], fail_silently: bool = False) -> Any:
        pass

    def render_recursive(self, obj: Any, scope: BaseModel | dict[str, Any], fail_silently: bool = False) -> Any:
        self._logger.info(f"Rendering {obj}")
        self._logger.info(f"Scope: {scope}")
        scope_dict = self._to_dict(scope)

        if isinstance(obj, BaseModel):
            obj = self._to_dict(obj)
        if isinstance(obj, str):
            return self.render(obj, scope_dict, fail_silently)
        if isinstance(obj, list):
            return [self.render_recursive(item, scope_dict, fail_silently) for item in obj]
        if isinstance(obj, dict):
            return {k: self.render_recursive(v, scope_dict, fail_silently) for k, v in obj.items()}
        return obj
