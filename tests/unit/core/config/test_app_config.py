from __future__ import annotations

from pathlib import Path

from open_ticket_ai.core.config.app_config import AppConfig


def test_app_config_defaults() -> None:
    config = AppConfig()
    assert config.config_env_var == "OPEN_TICKET_AI_CONFIG"
    assert config.config_yaml_root_key == "open_ticket_ai"
    assert config.default_config_filename == "config.yml"


def test_app_config_customization() -> None:
    config = AppConfig(
        config_env_var="CUSTOM_VAR",
        config_yaml_root_key="custom_root",
        default_config_filename="custom.yml",
    )
    assert config.config_env_var == "CUSTOM_VAR"
    assert config.get_default_config_path() == Path.cwd() / "custom.yml"


def test_app_config_serialization() -> None:
    config = AppConfig(config_env_var="TEST_VAR")
    data = config.model_dump()
    assert data["config_env_var"] == "TEST_VAR"
    restored = AppConfig.model_validate(data)
    assert restored.config_env_var == "TEST_VAR"
