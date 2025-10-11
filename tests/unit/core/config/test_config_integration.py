from __future__ import annotations

from pathlib import Path

from injector import Injector

from open_ticket_ai.core import AppConfig, AppModule, ConfigLoader, RawOpenTicketAIConfig


def test_complete_config_flow_with_defaults(tmp_path: Path) -> None:
    """Test the complete config loading flow with default AppConfig."""
    config_content = """
open_ticket_ai:
  plugins: ["default-plugin"]
  general_config:
    logging:
      version: 1
  defs:
    - id: test-def
      use: some.class
  orchestrator:
    runners:
      - run_every_milli_seconds: 5000
        pipe:
          id: test-pipe
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    config_loader = ConfigLoader(AppConfig())
    config = config_loader.load_config(config_path)

    assert config.plugins == ["default-plugin"]
    assert len(config.defs) == 1
    assert config.defs[0].id == "test-def"


def test_complete_config_flow_with_custom_app_config(tmp_path: Path) -> None:
    """Test the complete config loading flow with custom AppConfig."""
    config_content = """
custom_app:
  plugins: ["custom-plugin"]
  general_config:
    logging:
      version: 1
  defs: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "custom.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    app_config = AppConfig(config_yaml_root_key="custom_app")
    config_loader = ConfigLoader(app_config)
    config = config_loader.load_config(config_path)

    assert config.plugins == ["custom-plugin"]


def test_complete_di_flow_with_env_var(tmp_path: Path, monkeypatch) -> None:
    """Test complete DI flow using environment variable."""
    config_content = """
open_ticket_ai:
  plugins: ["env-plugin"]
  general_config:
    logging:
      version: 1
  defs: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    monkeypatch.setenv("OPEN_TICKET_AI_CONFIG", str(config_path))

    injector = Injector([AppModule()])
    config = injector.get(RawOpenTicketAIConfig)
    app_config = injector.get(AppConfig)

    assert config.plugins == ["env-plugin"]
    assert app_config.config_env_var == "OPEN_TICKET_AI_CONFIG"


def test_complete_di_flow_with_custom_env_var(tmp_path: Path, monkeypatch) -> None:
    """Test complete DI flow using custom environment variable."""
    config_content = """
my_app:
  plugins: ["custom-env-plugin"]
  general_config:
    logging:
      version: 1
  defs: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "custom.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    custom_app_config = AppConfig(config_env_var="MY_APP_CONFIG", config_yaml_root_key="my_app")

    monkeypatch.setenv("MY_APP_CONFIG", str(config_path))

    injector = Injector([AppModule(config_path, custom_app_config)])
    config = injector.get(RawOpenTicketAIConfig)
    app_config = injector.get(AppConfig)

    assert config.plugins == ["custom-env-plugin"]
    assert app_config.config_env_var == "MY_APP_CONFIG"
    assert app_config.config_yaml_root_key == "my_app"


def test_app_config_allows_hot_reload_preparation(tmp_path: Path) -> None:
    """Test that AppConfig design supports future hot-reload functionality."""
    config_v1 = """
open_ticket_ai:
  plugins: ["v1"]
  general_config:
    logging:
      version: 1
  defs: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_v1.strip(), encoding="utf-8")

    app_config = AppConfig()
    config_loader = ConfigLoader(app_config)
    config1 = config_loader.load_config(config_path)
    assert config1.plugins == ["v1"]

    config_v2 = """
open_ticket_ai:
  plugins: ["v2"]
  general_config:
    logging:
      version: 1
  defs: []
  orchestrator:
    runners: []
    """
    config_path.write_text(config_v2.strip(), encoding="utf-8")

    config2 = config_loader.load_config(config_path)
    assert config2.plugins == ["v2"]
