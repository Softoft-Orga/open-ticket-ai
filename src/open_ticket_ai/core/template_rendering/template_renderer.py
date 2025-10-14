import json
from abc import ABC, abstractmethod
from typing import Any

from open_ticket_ai.core.logging_iface import LoggerFactory


def prettify(obj: Any) -> str:
    return str(json.dumps(obj, indent=2, ensure_ascii=False, default=str))


class TemplateRenderer(ABC):
    def __init__(self, logger_factory: LoggerFactory) -> None:
        self._logger = logger_factory.create(self.__class__.__name__)

    @abstractmethod
    def render(self, template_str: str, scope: dict[str, Any]) -> Any:
        pass

    def render_recursive(self, obj: Any, scope: dict[str, Any]) -> Any:
        self._logger.info(f"Rendering {obj}")
        self._logger.info(f"Scope: {prettify(scope)}")

        if isinstance(obj, str):
            return self.render(obj, scope)
        if isinstance(obj, list):
            return [self.render_recursive(item, scope) for item in obj]
        if isinstance(obj, dict):
            return {k: self.render_recursive(v, scope) for k, v in obj.items()}
        return obj
