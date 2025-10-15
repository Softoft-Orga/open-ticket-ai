from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class AppConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
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

    def get_templates_dir(self) -> Path:
        package_root = Path(__file__).parent.parent.parent.parent.parent
        return package_root / "docs" / "raw_en_docs" / "config_examples"
