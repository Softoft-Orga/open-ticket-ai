from abc import ABC, abstractmethod
from collections.abc import Callable
from importlib.metadata import EntryPoint
from typing import final

from injector import inject

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.injectables.injectable import Injectable


class Plugin(ABC):
    @inject
    def __init__(self, app_config: AppConfig | None = None) -> None:
        self._app_config = app_config or AppConfig()

    @final
    def on_load(self, registry: ComponentRegistry) -> None:
        """Register this plugin's injectables into the provided registry.

        Injectables come from ``_get_all_injectables()`` and are registered under
        the name: ``<component_prefix><separator><injectable.get_registry_name()>``.
        Any exceptions raised by ``registry.register`` are propagated.

        Args:
            registry: ComponentRegistry to register components into.
        """
        for injectable in self._get_all_injectables():
            registry_name = self.get_registry_name(injectable)
            registry.register(registry_name, injectable)

    @property
    def _plugin_name(self) -> str:
        module = self.__class__.__module__.split(".")[0]
        return module.replace("_", "-")

    @final
    @property
    def _component_name_prefix(self) -> str:
        """Get component name prefix for this plugin."""
        return self._plugin_name.replace(self._app_config.PLUGIN_NAME_PREFIX, "")

    def get_registry_name(self, injectable: type[Injectable]) -> str:
        """Get the name used to register this plugin's components."""
        return (
            self._component_name_prefix
            + self._app_config.REGISTRY_IDENTIFIER_SEPERATOR
            + injectable.get_registry_name()
        )

    @abstractmethod
    def _get_all_injectables(self) -> list[type[Injectable]]:
        pass


type GetEntryPointsFn = Callable[..., tuple[EntryPoint]]
