from typing import ClassVar

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource

from open_ticket_ai.core.config.config_models import OpenTicketAIConfig


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        yaml_file="config.yml",
    )

    PLUGIN_NAME_PREFIX: ClassVar[str] = "otai-"
    REGISTRY_IDENTIFIER_SEPERATOR: ClassVar[str] = ":"
    PLUGIN_ENTRY_POINT_GROUP: ClassVar[str] = "open_ticket_ai.plugins"

    open_ticket_ai: OpenTicketAIConfig = Field(
        default_factory=OpenTicketAIConfig, validation_alias=AliasChoices("cfg", "otai", "open_ticket_ai")
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            init_settings,
            file_secret_settings,
        )
