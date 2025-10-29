import typing
from importlib.metadata import EntryPoint, entry_points

from injector import inject

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.plugins.plugin import GetEntryPointsFn, Plugin


class PluginLoadError(Exception):
    """Raised when a plugin fails to load."""

    def __init__(self, plugin_name: str):
        super().__init__(f"Failed to load plugin: {plugin_name}")


default_entry_point_function: GetEntryPointsFn = typing.cast(GetEntryPointsFn, entry_points)


class PluginLoader:
    @inject
    def __init__(
        self,
        registry: ComponentRegistry,
        logger_factory: LoggerFactory,
        app_config: AppConfig,
        entry_points_fn: GetEntryPointsFn = default_entry_point_function,
    ):
        self._registry = registry
        self._logger = logger_factory.create(self.__class__.__name__)
        self._app_config = app_config
        self._entry_points_fn = entry_points_fn

    def _load_plugin(self, entry_point: EntryPoint) -> None:
        self._logger.info(f"Loading plugin {entry_point}")
        try:
            create_plugin: type[Plugin] = entry_point.load()
        except ModuleNotFoundError as e:
            self._logger.error(f"Error loading plugin {entry_point.name}: {e}")
            raise PluginLoadError(entry_point.name) from e
        plugin = create_plugin(self._app_config)
        if not isinstance(plugin, Plugin):
            raise PluginLoadError(entry_point.name)

        plugin.on_load(self._registry)

        self._logger.info(f"Loaded plugin: {entry_point.name}")

    def load_plugins(self) -> None:
        for ep in self._entry_points_fn(group=self._app_config.PLUGIN_ENTRY_POINT_GROUP):
            self._load_plugin(ep)
