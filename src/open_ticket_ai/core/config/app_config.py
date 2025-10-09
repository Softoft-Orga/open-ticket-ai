import logging
from pathlib import Path

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    config_env_var: str = Field(
        default="OPEN_TICKET_AI_CONFIG",
        description="Environment variable name for configuration file path",
    )
    config_yaml_root_key: str = Field(
        default="open_ticket_ai",
        description="Root key in YAML configuration file",
    )
    default_config_filename: str = Field(
        default="config.yml",
        description="Default configuration filename",
    )

    def get_default_config_path(self) -> Path:
        return Path.cwd() / self.default_config_filename

    def get_logger(self, name: str):
        return logging.getLogger(name)
