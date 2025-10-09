from __future__ import annotations

from pathlib import Path

from open_ticket_ai.core.config.app_config import AppConfig


def test_app_config_has_default_values() -> None:
    config = AppConfig()

    assert config.config_env_var == "OPEN_TICKET_AI_CONFIG"
    assert config.config_yaml_root_key == "open_ticket_ai"
    assert config.default_config_filename == "config.yml"


def test_app_config_can_be_customized() -> None:
    config = AppConfig(
        config_env_var="CUSTOM_CONFIG_VAR",
        config_yaml_root_key="custom_root",
        default_config_filename="custom.yml",
    )

    assert config.config_env_var == "CUSTOM_CONFIG_VAR"
    assert config.config_yaml_root_key == "custom_root"
    assert config.default_config_filename == "custom.yml"


def test_app_config_get_default_config_path() -> None:
    config = AppConfig()
    expected = Path.cwd() / "config.yml"

    assert config.get_default_config_path() == expected


def test_app_config_get_default_config_path_with_custom_filename() -> None:
    config = AppConfig(default_config_filename="my_config.yaml")
    expected = Path.cwd() / "my_config.yaml"

    assert config.get_default_config_path() == expected


def test_app_config_is_pydantic_model() -> None:
    config = AppConfig()

    assert hasattr(config, "model_dump")
    assert hasattr(config, "model_validate")


def test_app_config_can_be_serialized() -> None:
    config = AppConfig(
        config_env_var="TEST_VAR",
        config_yaml_root_key="test_root",
        default_config_filename="test.yml",
    )

    data = config.model_dump()

    assert data == {
        "config_env_var": "TEST_VAR",
        "config_yaml_root_key": "test_root",
        "default_config_filename": "test.yml",
    }


def test_app_config_can_be_deserialized() -> None:
    data = {
        "config_env_var": "TEST_VAR",
        "config_yaml_root_key": "test_root",
        "default_config_filename": "test.yml",
    }

    config = AppConfig.model_validate(data)

    assert config.config_env_var == "TEST_VAR"
    assert config.config_yaml_root_key == "test_root"
    assert config.default_config_filename == "test.yml"
