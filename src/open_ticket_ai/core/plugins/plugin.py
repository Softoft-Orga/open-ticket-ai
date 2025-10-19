from abc import ABC, abstractmethod
from collections.abc import Callable
from importlib.metadata import EntryPoints
from typing import final

from injector import inject

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.injectables.injectable import Injectable


class Plugin(ABC):
    @inject
    def __init__(self, app_config: AppConfig):
        self._app_config = app_config

    @property
    def _plugin_name(self) -> str:
        module = self.__class__.__module__.split(".")[0]
        return module.replace("_", "-")

    @final
    @property
    def _component_name_prefix(self) -> str:
        """Get component name prefix for this plugin."""
        return self._plugin_name.replace(self._app_config.PLUGIN_NAME_PREFIX, "")

    @final
    def _get_registry_name(self, injectable: type[Injectable]) -> str:
        """Get the name used to register this plugin's components."""
        return (
            self._component_name_prefix
            + self._app_config.REGISTRY_IDENTIFIER_SEPERATOR
            + injectable.get_registry_name()
        )

    @abstractmethod
    def _get_all_injectables(self) -> list[type[Injectable]]:
        pass

    @final
    def on_load(self, registry: ComponentRegistry) -> None:
        for injectable in self._get_all_injectables():
            registry_name = self._get_registry_name(injectable)
            registry.register(registry_name, injectable)


type CreatePluginFn = Callable[[AppConfig], Plugin]
type GetEntryPointsFn = Callable[..., EntryPoints]
