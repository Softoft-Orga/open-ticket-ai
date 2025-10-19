from typing import ClassVar

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from open_ticket_ai.core.config.config_models import OpenTicketAIConfig


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="OTAI_",
        env_nested_delimiter="__",
        env_file=".env",
        yaml_file="config.yml",
    )

    PLUGIN_NAME_PREFIX: ClassVar[str] = "otai-"
    REGISTRY_IDENTIFIER_SEPERATOR: ClassVar[str] = ":"
    PLUGIN_ENTRY_POINT_GROUP: ClassVar[str] = "open_ticket_ai.plugins"

    open_ticket_ai: OpenTicketAIConfig = Field(
        default_factory=OpenTicketAIConfig, validation_alias=AliasChoices("cfg", "open_ticket_ai")
    )
