from importlib.metadata import entry_points

from injector import inject

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.plugins.plugin_base import CreatePluginFn, Plugin


class PluginLoadError(Exception):
    """Raised when a plugin fails to load."""


class PluginLoader:
    @inject
    def __init__(self, registry: ComponentRegistry, logger_factory: LoggerFactory, app_config: AppConfig):
        self._registry = registry
        self._logger = logger_factory.create(self.__class__.__name__)
        self._app_config = app_config

    def load_plugins(self):
        for ep in entry_points(group="open_ticket_ai.plugins"):
            create_plugin: CreatePluginFn = ep.load()
            plugin = create_plugin(self._app_config)
            if not isinstance(plugin, Plugin):
                raise PluginLoadError(f"Plugin {ep.name} did not return a valid PluginBase instance.")

            plugin.on_load(self._registry)

            self._logger.info(f"Loaded plugin: {ep.name}")
