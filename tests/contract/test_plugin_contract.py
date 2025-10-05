from __future__ import annotations

import importlib.metadata as md

import pytest

PLUGIN_GROUP = "open_ticket_ai.plugins"
REQUIRED_CORE_API = "2.0"


def discover_plugins():
    for ep in md.entry_points(group=PLUGIN_GROUP):
        plugin = ep.load()
        meta = getattr(plugin, "get_metadata", lambda: {})()
        yield ep.name, plugin, meta


@pytest.mark.contract
@pytest.mark.parametrize("name,plugin,meta", list(discover_plugins()), ids=lambda x: x[0])
def test_core_api_matches(name, plugin, meta):
    assert meta.get("core_api") == REQUIRED_CORE_API


@pytest.mark.contract
@pytest.mark.parametrize("name,plugin,meta", list(discover_plugins()), ids=lambda x: x[0])
def test_register_hooks_exist(name, plugin, meta):
    assert hasattr(plugin, "register_pipes")
    assert hasattr(plugin, "register_services")
    assert "name" in meta and "version" in meta
