from __future__ import annotations

import importlib.metadata as md

import pytest

PLUGIN_GROUP = "open_ticket_ai.plugins"
REQUIRED_CORE_API = "2.0"
REQUIRED_METADATA_FIELDS = {"name", "version", "core_api", "description"}


def discover_plugins():
    for ep in md.entry_points(group=PLUGIN_GROUP):
        plugin = ep.load()
        meta = getattr(plugin, "get_metadata", lambda: {})()
        yield ep.name, plugin, meta


@pytest.mark.contract
@pytest.mark.parametrize("name,plugin,meta", list(discover_plugins()), ids=lambda x: x[0])
def test_metadata_function_exists(name, plugin, meta):
    assert hasattr(plugin, "get_metadata"), f"Plugin {name} must have get_metadata() function"


@pytest.mark.contract
@pytest.mark.parametrize("name,plugin,meta", list(discover_plugins()), ids=lambda x: x[0])
def test_metadata_fields_present(name, plugin, meta):
    missing_fields = REQUIRED_METADATA_FIELDS - set(meta.keys())
    assert not missing_fields, f"Plugin {name} metadata missing required fields: {missing_fields}"


@pytest.mark.contract
@pytest.mark.parametrize("name,plugin,meta", list(discover_plugins()), ids=lambda x: x[0])
def test_core_api_matches(name, plugin, meta):
    assert meta.get("core_api") == REQUIRED_CORE_API, (
        f"Plugin {name} has incompatible core_api: {meta.get('core_api')} (expected {REQUIRED_CORE_API})"
    )


@pytest.mark.contract
@pytest.mark.parametrize("name,plugin,meta", list(discover_plugins()), ids=lambda x: x[0])
def test_register_hooks_exist(name, plugin, meta):
    assert hasattr(plugin, "register_pipes"), f"Plugin {name} must have register_pipes() function"
    assert hasattr(plugin, "register_services"), f"Plugin {name} must have register_services() function"


@pytest.mark.contract
@pytest.mark.parametrize("name,plugin,meta", list(discover_plugins()), ids=lambda x: x[0])
def test_register_hooks_return_lists(name, plugin, meta):
    pipes = plugin.register_pipes()
    assert isinstance(pipes, list), f"Plugin {name} register_pipes() must return a list, got {type(pipes)}"

    services = plugin.register_services()
    assert isinstance(services, list), f"Plugin {name} register_services() must return a list, got {type(services)}"
