from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from open_ticket_ai.core.plugins.manager import CORE_API_VERSION, PLUGIN_GROUP, PluginManager


class MockPlugin:
    def __init__(self, name: str, version: str, core_api: str):
        self.name = name
        self.version = version
        self.core_api = core_api
        self.services_registered = False
        self.pipes_registered = False

    def get_metadata(self):
        return {
            "name": self.name,
            "version": self.version,
            "core_api": self.core_api,
        }

    def register_services(self, binder):
        self.services_registered = True

    def register_pipes(self, factory):
        self.pipes_registered = True


@pytest.fixture
def plugin_manager():
    return PluginManager()


def test_plugin_manager_initialization(plugin_manager):
    assert plugin_manager._loaded is False
    assert len(plugin_manager._plugins) == 0


def test_plugin_manager_discover_loads_once(plugin_manager, monkeypatch):

    def mock_entry_points(group):
        if group == PLUGIN_GROUP:
            ep = MagicMock()
            ep.name = "test_plugin"
            ep.load.return_value = MockPlugin("test", "1.0.0", CORE_API_VERSION)
            return [ep]
        return []

    monkeypatch.setattr("importlib.metadata.entry_points", mock_entry_points)

    plugin_manager.discover_and_load()
    assert plugin_manager._loaded is True
    assert len(plugin_manager._plugins) == 1

    plugin_manager.discover_and_load()
    assert len(plugin_manager._plugins) == 1


def test_plugin_manager_skips_incompatible_api(plugin_manager, monkeypatch):
    def mock_entry_points(group):
        if group == PLUGIN_GROUP:
            ep = MagicMock()
            ep.name = "incompatible_plugin"
            ep.load.return_value = MockPlugin("incompatible", "1.0.0", "1.0")
            return [ep]
        return []

    monkeypatch.setattr("importlib.metadata.entry_points", mock_entry_points)

    plugin_manager.discover_and_load()
    assert len(plugin_manager._plugins) == 0


def test_plugin_manager_handles_load_errors(plugin_manager, monkeypatch):
    def mock_entry_points(group):
        if group == PLUGIN_GROUP:
            ep = MagicMock()
            ep.name = "broken_plugin"
            ep.load.side_effect = Exception("Load error")
            return [ep]
        return []

    monkeypatch.setattr("importlib.metadata.entry_points", mock_entry_points)

    plugin_manager.discover_and_load()
    assert len(plugin_manager._plugins) == 0


def test_plugin_manager_register_services(plugin_manager, monkeypatch):
    plugin = MockPlugin("test", "1.0.0", CORE_API_VERSION)

    def mock_entry_points(group):
        if group == PLUGIN_GROUP:
            ep = MagicMock()
            ep.name = "test_plugin"
            ep.load.return_value = plugin
            return [ep]
        return []

    monkeypatch.setattr("importlib.metadata.entry_points", mock_entry_points)

    plugin_manager.discover_and_load()

    mock_binder = MagicMock()
    plugin_manager.register_services(mock_binder)

    assert plugin.services_registered is True


def test_plugin_manager_register_pipes(plugin_manager, monkeypatch):
    plugin = MockPlugin("test", "1.0.0", CORE_API_VERSION)

    def mock_entry_points(group):
        if group == PLUGIN_GROUP:
            ep = MagicMock()
            ep.name = "test_plugin"
            ep.load.return_value = plugin
            return [ep]
        return []

    monkeypatch.setattr("importlib.metadata.entry_points", mock_entry_points)

    plugin_manager.discover_and_load()

    mock_factory = MagicMock()
    plugin_manager.register_pipes(mock_factory)

    assert plugin.pipes_registered is True


def test_plugin_manager_loaded_plugins(plugin_manager, monkeypatch):
    def mock_entry_points(group):
        if group == PLUGIN_GROUP:
            ep = MagicMock()
            ep.name = "test_plugin"
            ep.load.return_value = MockPlugin("test", "1.0.0", CORE_API_VERSION)
            return [ep]
        return []

    monkeypatch.setattr("importlib.metadata.entry_points", mock_entry_points)

    plugin_manager.discover_and_load()
    plugins = plugin_manager.loaded_plugins

    assert len(plugins) == 1
    assert isinstance(plugins, list)
