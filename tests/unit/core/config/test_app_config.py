from pathlib import Path

import pytest
from pydantic import ValidationError
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings.sources import YamlConfigSettingsSource

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import OpenTicketAIConfig


@pytest.fixture
def simple_config_file() -> Path:
    return Path(__file__).parent / "data" / "simple_config.yml"


@pytest.fixture
def minimal_config_file() -> Path:
    return Path(__file__).parent / "data" / "minimal_config.yml"


def test_app_config_loads_from_yaml_only(simple_config_file: Path) -> None:
    class TestAppConfig(AppConfig):
        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: type[AppConfig],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            return (
                init_settings,
                YamlConfigSettingsSource(settings_cls, yaml_file=simple_config_file),
            )

    config = TestAppConfig()

    assert isinstance(config.open_ticket_ai, OpenTicketAIConfig)
    assert config.open_ticket_ai.api_version == "2"
    assert config.open_ticket_ai.plugins == ["plugin1", "plugin2"]
    assert config.open_ticket_ai.infrastructure.logging.level == "INFO"
    assert config.open_ticket_ai.infrastructure.default_template_renderer == "jinja_default"


def test_app_config_env_var_prefix_correctly_parsed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OTAI_OPEN_TICKET_AI__API_VERSION", "3")

    class TestAppConfig(AppConfig):
        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: type[AppConfig],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            return (
                init_settings,
                env_settings,
            )

    config = TestAppConfig()

    assert config.open_ticket_ai.api_version == "3"


def test_app_config_env_var_nested_delimiter_parses_deep_structure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OTAI_OPEN_TICKET_AI__API_VERSION", "5")
    monkeypatch.setenv("OTAI_OPEN_TICKET_AI__INFRASTRUCTURE__LOGGING__LEVEL", "WARNING")
    monkeypatch.setenv("OTAI_OPEN_TICKET_AI__INFRASTRUCTURE__DEFAULT_TEMPLATE_RENDERER", "jinja2")

    class TestAppConfig(AppConfig):
        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: type[AppConfig],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            return (
                init_settings,
                env_settings,
            )

    config = TestAppConfig()

    assert config.open_ticket_ai.api_version == "5"
    assert config.open_ticket_ai.infrastructure.logging.level == "WARNING"
    assert config.open_ticket_ai.infrastructure.default_template_renderer == "jinja2"


def test_app_config_loads_from_env_only(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OTAI_OPEN_TICKET_AI__API_VERSION", "10")
    monkeypatch.setenv("OTAI_OPEN_TICKET_AI__PLUGINS", '["env_plugin1", "env_plugin2"]')

    class TestAppConfig(AppConfig):
        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: type[AppConfig],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            return (
                init_settings,
                env_settings,
            )

    config = TestAppConfig()

    assert config.open_ticket_ai.api_version == "10"
    assert config.open_ticket_ai.plugins == ["env_plugin1", "env_plugin2"]


def test_app_config_bad_env_var_type_triggers_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OTAI_OPEN_TICKET_AI__PLUGINS", "not_a_list")

    class TestAppConfig(AppConfig):
        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: type[AppConfig],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            return (
                init_settings,
                env_settings,
            )

    with pytest.raises((ValidationError, Exception)) as exc_info:
        TestAppConfig()

    assert "open_ticket_ai" in str(exc_info.value).lower() or "plugins" in str(exc_info.value).lower()


def test_app_config_passes_correct_config_to_downstream(simple_config_file: Path) -> None:
    class TestAppConfig(AppConfig):
        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: type[AppConfig],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            return (
                init_settings,
                YamlConfigSettingsSource(settings_cls, yaml_file=simple_config_file),
            )

    config = TestAppConfig()

    otai_config = config.open_ticket_ai
    assert isinstance(otai_config, OpenTicketAIConfig)
    assert otai_config.api_version == "2"
    assert len(otai_config.plugins) == 2
    assert otai_config.infrastructure.logging.level == "INFO"


def test_app_config_yaml_file_loads_correctly(simple_config_file: Path) -> None:
    class TestAppConfig(AppConfig):
        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: type[AppConfig],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            return (
                init_settings,
                YamlConfigSettingsSource(settings_cls, yaml_file=simple_config_file),
            )

    config = TestAppConfig()

    assert config.open_ticket_ai.api_version == "2"
    assert config.open_ticket_ai.plugins == ["plugin1", "plugin2"]
    assert config.open_ticket_ai.infrastructure.logging.level == "INFO"


def test_app_config_with_minimal_yaml(minimal_config_file: Path) -> None:
    class TestAppConfig(AppConfig):
        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: type[AppConfig],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            return (
                init_settings,
                YamlConfigSettingsSource(settings_cls, yaml_file=minimal_config_file),
            )

    config = TestAppConfig()

    assert config.open_ticket_ai.api_version == "1"
    assert config.open_ticket_ai.plugins == []
    assert config.open_ticket_ai.infrastructure.default_template_renderer == "jinja2"
