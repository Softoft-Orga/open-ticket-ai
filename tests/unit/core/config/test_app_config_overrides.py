from __future__ import annotations

from pathlib import Path

from injector import Injector

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.dependency_injection.container import AppModule


def test_app_config_can_be_overridden_for_tests(tmp_path: Path) -> None:
    """Demonstrate that AppConfig can be overridden for testing purposes."""
    test_config_content = """
test_app:
  plugins: []
  general_config:
    logging:
      version: 1
  services: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "test.yml"
    config_path.write_text(test_config_content.strip(), encoding="utf-8")

    test_app_config = AppConfig(
        config_env_var="TEST_CONFIG_VAR",
        config_yaml_root_key="test_app",
        default_config_filename="test.yml",
    )

    injector = Injector([AppModule(config_path, test_app_config)])
    bound_config = injector.get(AppConfig)

    assert bound_config.config_env_var == "TEST_CONFIG_VAR"
    assert bound_config.config_yaml_root_key == "test_app"
    assert bound_config.default_config_filename == "test.yml"


def test_app_config_supports_plugins_override(tmp_path: Path, monkeypatch) -> None:
    """Demonstrate that AppConfig enables plugin developers to customize configuration."""
    plugin_config_content = """
my_plugin:
  plugins: ["custom-plugin"]
  general_config:
    logging:
      version: 1
  services: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "plugin.yml"
    config_path.write_text(plugin_config_content.strip(), encoding="utf-8")

    plugin_app_config = AppConfig(
        config_env_var="MY_PLUGIN_CONFIG",
        config_yaml_root_key="my_plugin",
        default_config_filename="plugin.yml",
    )

    monkeypatch.setenv("MY_PLUGIN_CONFIG", str(config_path))

    injector = Injector([AppModule(None, plugin_app_config)])

    config = injector.get(RawOpenTicketAIConfig)
    assert config.plugins == ["custom-plugin"]
