from __future__ import annotations

from injector import Injector

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.dependency_injection import container as container_module
from open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry


class _SentinelRegistry(UnifiedRegistry):
    """A registry subclass used to ensure the container binds the expected instance."""


def test_app_module_binds_singleton_dependencies(monkeypatch) -> None:
    fake_config = RawOpenTicketAIConfig()
    sentinel_registry = _SentinelRegistry()
    load_config_calls: list[object] = []

    def fake_load_config(path):
        load_config_calls.append(path)
        return fake_config

    monkeypatch.setattr(container_module, "load_config", fake_load_config)
    monkeypatch.setattr(
        container_module.UnifiedRegistry,
        "get_registry_instance",
        classmethod(lambda cls: sentinel_registry),
    )

    injector = Injector([AppModule()])

    resolved_config = injector.get(RawOpenTicketAIConfig)
    resolved_registry = injector.get(UnifiedRegistry)

    assert load_config_calls == [container_module.CONFIG_PATH]
    assert resolved_config is fake_config
    assert resolved_registry is sentinel_registry
    assert injector.get(RawOpenTicketAIConfig) is resolved_config
    assert injector.get(UnifiedRegistry) is resolved_registry
