"""Settings configuration for the flow editor API using pydantic-settings."""

import os
from pathlib import Path
from typing import List

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    # Fallback for environments without pydantic-settings
    from pydantic import BaseSettings  # type: ignore
    
    class SettingsConfigDict:  # type: ignore
        """Dummy SettingsConfigDict for environments without pydantic-settings."""
        pass


class Settings(BaseSettings):
    """Application settings."""

    config_path: Path = Path("src/config.yml")
    cors_origins: List[str] = ["http://localhost:5173"]

    if hasattr(BaseSettings, "model_config"):
        # pydantic-settings v2 style
        model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)
    else:
        # pydantic v1 style
        class Config:
            env_prefix = ""
            case_sensitive = False

    def __init__(self, **kwargs):
        """Initialize settings, respecting CONFIG_PATH environment variable."""
        if "config_path" not in kwargs and "CONFIG_PATH" in os.environ:
            kwargs["config_path"] = Path(os.environ["CONFIG_PATH"])
        super().__init__(**kwargs)


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()
