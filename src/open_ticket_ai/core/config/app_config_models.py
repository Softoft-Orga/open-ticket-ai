from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OTAI_")
    config_file_path: Path = Field(
        default=Path.cwd() / "config.yml",
    )
    config_yaml_root_key: str = Field(
        default="open_ticket_ai",
        description="Root key in YAML configuration file",
    )
    templates_dir: Path = Field(
        default_factory=lambda: Path.cwd() / "data" / "templates",
        description="Directory containing configuration templates",
    )
