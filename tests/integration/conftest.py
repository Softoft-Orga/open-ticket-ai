from importlib.metadata import entry_points

import pytest
from injector import Injector, Module, provider

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.core.plugins.plugin import GetEntryPointsFn

pytestmark = [pytest.mark.integration]


class TestModule(Module):
    @provider
    def provide_entry_points_fn(self) -> GetEntryPointsFn:
        return entry_points


@pytest.fixture
def integration_container(temp_config_file):
    app_config = AppConfig(_env_file=None)
    app_module = AppModule(app_config)
    container = Injector([app_module, TestModule()])
    return container


@pytest.fixture
def integration_component_registry(temp_config_file):
    app_config = AppConfig(_env_file=None)
    app_module = AppModule(app_config)
    return app_module.component_registry
