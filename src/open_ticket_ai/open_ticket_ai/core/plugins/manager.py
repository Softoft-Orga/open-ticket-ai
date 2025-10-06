from __future__ import annotations

import importlib.metadata as md
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from injector import Binder

    from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory

PLUGIN_GROUP = "open_ticket_ai.plugins"
CORE_API_VERSION = "2.0"


class PluginManager:
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        self._plugins: list[Any] = []
        self._loaded = False

    def discover_and_load(self) -> None:
        if self._loaded:
            return

        for ep in md.entry_points(group=PLUGIN_GROUP):
            try:
                plugin = ep.load()
                meta = getattr(plugin, "get_metadata", lambda: {})()

                plugin_name = meta.get("name", ep.name)
                plugin_version = meta.get("version", "unknown")
                core_api = meta.get("core_api")

                if core_api != CORE_API_VERSION:
                    self._logger.warning(
                        f"Plugin '{plugin_name}' v{plugin_version} requires core_api={core_api}, "
                        f"but current core API is {CORE_API_VERSION}. Skipping."
                    )
                    continue

                self._plugins.append(plugin)
                self._logger.info(f"Loaded plugin: {plugin_name} v{plugin_version}")

            except Exception:
                self._logger.exception(f"Failed to load plugin '{ep.name}'")

        self._loaded = True

    def register_services(self, binder: Binder) -> None:
        for plugin in self._plugins:
            if hasattr(plugin, "register_services"):
                try:
                    plugin.register_services(binder)
                except Exception:
                    self._logger.exception("Failed to register services for plugin")

    def register_pipes(self, factory: PipeFactory) -> None:
        for plugin in self._plugins:
            if hasattr(plugin, "register_pipes"):
                try:
                    plugin.register_pipes(factory)
                except Exception:
                    self._logger.exception("Failed to register pipes for plugin")

    @property
    def loaded_plugins(self) -> list[Any]:
        return self._plugins.copy()

    def get_cli_commands(self) -> dict[str, Any]:
        commands = {}
        for plugin in self._plugins:
            if hasattr(plugin, "register_cli_commands"):
                try:
                    plugin_commands = plugin.register_cli_commands()
                    if isinstance(plugin_commands, dict):
                        commands.update(plugin_commands)
                    else:
                        meta = getattr(plugin, "get_metadata", lambda: {})()
                        plugin_name = meta.get("name", "unknown")
                        self._logger.debug(
                            f"Plugin {plugin_name} returned non-dict CLI commands"
                        )
                except Exception:
                    self._logger.exception("Failed to get CLI commands for plugin")
        return commands
