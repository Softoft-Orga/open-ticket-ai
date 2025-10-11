from __future__ import annotations

import os
from pathlib import Path

import pytest

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_loader import ConfigLoader


def test_config_loader_uses_app_config_env_var(tmp_path: Path) -> None:
    config_content = """
custom_root:
  plugins: []
  general_config:
    logging:
      version: 1
  defs: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "test.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    app_config = AppConfig(config_env_var="CUSTOM_CONFIG_VAR", config_yaml_root_key="custom_root")

    os.environ["CUSTOM_CONFIG_VAR"] = str(config_path)
    try:
        loader = ConfigLoader(app_config)
        config = loader.load_config()

        assert config is not None
        assert config.plugins == []
    finally:
        del os.environ["CUSTOM_CONFIG_VAR"]


def test_config_loader_uses_app_config_root_key(tmp_path: Path) -> None:
    config_content = """
my_app:
  plugins: ["test"]
  general_config:
    logging:
      version: 1
  defs: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "test.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    app_config = AppConfig(config_yaml_root_key="my_app")
    loader = ConfigLoader(app_config)
    config = loader.load_config(config_path)

    assert config.plugins == ["test"]


def test_config_loader_with_explicit_path(tmp_path: Path) -> None:
    config_content = """
open_ticket_ai:
  plugins: []
  general_config:
    logging:
      version: 1
  defs: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    app_config = AppConfig()
    loader = ConfigLoader(app_config)
    config = loader.load_config(config_path)

    assert config is not None


def test_config_loader_raises_when_no_path_and_no_env(tmp_path: Path) -> None:
    app_config = AppConfig(config_env_var="NON_EXISTENT_VAR")

    if "NON_EXISTENT_VAR" in os.environ:
        del os.environ["NON_EXISTENT_VAR"]

    with pytest.raises(FileNotFoundError):
        ConfigLoader(app_config).load_config()


def test_config_loader_error_message_includes_custom_env_var(tmp_path: Path) -> None:
    app_config = AppConfig(config_env_var="MY_CUSTOM_VAR")

    if "MY_CUSTOM_VAR" in os.environ:
        del os.environ["MY_CUSTOM_VAR"]

    with pytest.raises(FileNotFoundError):
        ConfigLoader(app_config).load_config()
