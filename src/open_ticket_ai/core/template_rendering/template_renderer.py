import ast
import json
import logging
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class TemplateRenderer(ABC):
    @staticmethod
    def _normalize_scope(scope: BaseModel | dict[str, Any]) -> dict[str, Any]:
        if isinstance(scope, BaseModel):
            return scope.model_dump()
        return scope

    @staticmethod
    def _parse_rendered_value(s: str) -> Any:
        if not s.strip():
            return s
        try:
            return json.loads(s)
        except Exception as e:
            logging.debug(f"Failed to parse JSON: {str(e)}")
            try:
                return ast.literal_eval(s)
            except Exception as e:
                logging.debug(f"Failed to parse literal: {str(e)}")
                return s

    @abstractmethod
    def render(self, template_str: str, scope: dict[str, Any], fail_silently: bool = False) -> Any:
        pass

    def render_recursive(self, obj: Any, scope: BaseModel | dict[str, Any], fail_silently: bool = False) -> Any:
        scope_dict = self._normalize_scope(scope)
        if isinstance(obj, str):
            return self.render(obj, scope_dict, fail_silently)
        if isinstance(obj, list):
            return [self.render_recursive(item, scope_dict, fail_silently) for item in obj]
        if isinstance(obj, dict):
            return {k: self.render_recursive(v, scope_dict, fail_silently) for k, v in obj.items()}
        return obj
