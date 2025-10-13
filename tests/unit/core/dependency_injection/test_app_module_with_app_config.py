from __future__ import annotations

from pathlib import Path

import pytest
from injector import Injector

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.dependency_injection.container import AppModule


def test_app_module_binds_app_config_as_singleton(tmp_path: Path) -> None:
    config_content = """
open_ticket_ai:
  plugins: []
  services: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    injector = Injector([AppModule(config_path)])

    app_config1 = injector.get(AppConfig)
    app_config2 = injector.get(AppConfig)

    assert app_config1 is app_config2
    assert isinstance(app_config1, AppConfig)


def test_app_module_uses_custom_app_config(tmp_path: Path) -> None:
    config_content = """
my_custom_root:
  plugins: []
  services: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    custom_app_config = AppConfig(config_yaml_root_key="my_custom_root")
    injector = Injector([AppModule(config_path, custom_app_config)])

    bound_app_config = injector.get(AppConfig)

    assert bound_app_config is custom_app_config
    assert bound_app_config.config_yaml_root_key == "my_custom_root"


def test_app_module_config_loader_uses_app_config(tmp_path: Path) -> None:
    config_content = """
open_ticket_ai:
  plugins: ["test-plugin"]
  services: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    injector = Injector([AppModule(config_path)])

    config = injector.get(RawOpenTicketAIConfig)

    assert config.plugins == ["test-plugin"]


def test_app_module_respects_app_config_for_loading(tmp_path: Path) -> None:
    config_content = """
different_key:
  plugins: ["from-different-key"]
  services: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    custom_app_config = AppConfig(config_yaml_root_key="different_key")
    injector = Injector([AppModule(config_path, custom_app_config)])

    config = injector.get(RawOpenTicketAIConfig)

    assert config.plugins == ["from-different-key"]


def test_app_module_without_config_path_uses_app_config_env_var(tmp_path: Path, monkeypatch) -> None:
    config_content = """
open_ticket_ai:
  plugins: []
  services: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    custom_app_config = AppConfig(config_env_var="MY_CUSTOM_ENV_VAR")
    monkeypatch.setenv("MY_CUSTOM_ENV_VAR", str(config_path))

    injector = Injector([AppModule(None, custom_app_config)])

    config = injector.get(RawOpenTicketAIConfig)
    assert config is not None
