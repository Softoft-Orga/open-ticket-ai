from abc import ABC, abstractmethod
from typing import Any, final

from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.util.formatting import prettify


class TemplateRenderer(ABC):
    def __init__(self, logger_factory: LoggerFactory) -> None:
        self._logger = logger_factory.create(self.__class__.__name__)

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
