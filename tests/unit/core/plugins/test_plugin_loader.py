from unittest.mock import MagicMock

import pytest

from open_ticket_ai.core.plugins.plugin_base import Plugin
from open_ticket_ai.core.plugins.plugin_loader import PluginLoader, PluginLoadError


class TestPluginLoaderConstruction:
    def test_accepts_correct_dependencies(
        self, mock_component_registry, logger_factory, mock_app_config
    ):
        mock_entry_points_fn = MagicMock()

        loader = PluginLoader(
            registry=mock_component_registry,
            logger_factory=logger_factory,
            app_config=mock_app_config,
            entry_points_fn=mock_entry_points_fn,
        )

        assert loader._registry == mock_component_registry
        assert loader._app_config == mock_app_config
        assert loader._entry_points_fn == mock_entry_points_fn


class TestLoadPlugins:
    def test_calls_on_load_for_each_plugin(
        self, mock_component_registry, logger_factory, mock_app_config
    ):
        mock_plugin = MagicMock(spec=Plugin)
        mock_plugin.on_load = MagicMock()

        mock_entry_point = MagicMock()
        mock_entry_point.name = "test-plugin"
        mock_entry_point.load.return_value = lambda _: mock_plugin

        mock_entry_points_fn = MagicMock(return_value=[mock_entry_point])

        loader = PluginLoader(
            registry=mock_component_registry,
            logger_factory=logger_factory,
            app_config=mock_app_config,
            entry_points_fn=mock_entry_points_fn,
        )

        loader.load_plugins()

        mock_plugin.on_load.assert_called_once_with(mock_component_registry)

    def test_raises_exception_for_invalid_plugin(
        self, mock_component_registry, logger_factory, mock_app_config
    ):
        class NotAPlugin:
            pass

        mock_entry_point = MagicMock()
        mock_entry_point.name = "invalid-plugin"
        mock_entry_point.load.return_value = lambda _: NotAPlugin()

        mock_entry_points_fn = MagicMock(return_value=[mock_entry_point])

        loader = PluginLoader(
            registry=mock_component_registry,
            logger_factory=logger_factory,
            app_config=mock_app_config,
            entry_points_fn=mock_entry_points_fn,
        )

        with pytest.raises(PluginLoadError):
            loader.load_plugins()
