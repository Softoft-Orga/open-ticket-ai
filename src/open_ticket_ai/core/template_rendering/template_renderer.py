import ast
import json
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.logging_iface import LoggerFactory

def pretty_print(obj: Any) -> str:
    if isinstance(obj, BaseModel):
        data = obj.model_dump()
    elif isinstance(obj, dict):
        data = obj
    else:
        # Not a dict or BaseModel: do nothing
        return ""

    try:
        return str(json.dumps(data, indent=2, ensure_ascii=False, default=str))
    except Exception:
        # Fallback: best-effort via str() for the whole object
        try:
            return str(json.dumps({k: str(v) for k, v in (data.items() if isinstance(data, dict) else [])}, indent=2))
        except Exception:
            # Last resort: repr
            return repr(data)


class TemplateRenderer(ABC):
    def __init__(self, logger_factory: LoggerFactory) -> None:
        self._logger = logger_factory.get_logger(self.__class__.__name__)

    def _to_dict(self, scope: BaseModel | dict[str, Any]) -> dict[str, Any]:
        if isinstance(scope, BaseModel):
            return scope.model_dump()
        return scope

    def _parse_rendered_value(self, s: Any) -> Any:
        # If it's already a native type (dict, list, int, etc.), return it as-is
        if not isinstance(s, str):
            return s

        if not s.strip():
            return s

        stripped = s.strip()

        try:
            return json.loads(stripped)
        except Exception as e:
            try:
                return ast.literal_eval(stripped)
            except Exception as e:
                self._logger.debug(f"Failed to parse JSON: {str(e)}")
                self._logger.debug(f"Failed to parse literal: {str(e)}")

            return s

    @abstractmethod
    def render(self, template_str: str, scope: dict[str, Any]) -> Any:
        pass

    def render_recursive(self, obj: Any, scope: BaseModel | dict[str, Any]) -> Any:
        self._logger.info(f"Rendering {obj}")
        self._logger.info(f"Scope: {pretty_print(scope)}")
        scope_dict = self._to_dict(scope)

        if isinstance(obj, BaseModel):
            obj = self._to_dict(obj)
        if isinstance(obj, str):
            return self.render(obj, scope_dict)
        if isinstance(obj, list):
            return [self.render_recursive(item, scope_dict) for item in obj]
        if isinstance(obj, dict):
            return {k: self.render_recursive(v, scope_dict) for k, v in obj.items()}
        return obj
