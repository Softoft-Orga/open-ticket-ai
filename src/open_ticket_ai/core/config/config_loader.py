import os

import injector
import yaml  # type: ignore[import-untyped]
from injector import singleton

from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


@singleton
class ConfigLoader:
    @injector.inject
    def __init__(self, app_config: AppConfig):
        self.app_config = app_config
        self._logger = app_config.get_logger(self.__class__.__name__)

    def load_config(self, config_path: str | os.PathLike[str] | None = None) -> RawOpenTicketAIConfig:
        config_path_resolved: str | os.PathLike[str]
        if config_path is None and os.getenv(self.app_config.config_env_var) is not None:
            config_path_str = os.getenv(self.app_config.config_env_var)
            if config_path_str is None:
                raise ValueError("Config path from environment variable is None")
            config_path_resolved = config_path_str
        elif config_path is None and os.getenv(self.app_config.config_env_var) is None:
            config_path_resolved = self.app_config.get_default_config_path()
            if not config_path_resolved.exists():
                raise FileNotFoundError(
                    f"Config file not found at {config_path_resolved}."
                    f"To fix this error:"
                    f"Create a confi file at {config_path_resolved}"
                    f"or provide a valid config path "
                    f"or set the {self.app_config.config_env_var} environment variable."
                )
        elif config_path is not None:
            config_path_resolved = config_path
        else:
            raise ValueError("Config path is None and no environment variable set")

        if not os.path.exists(config_path_resolved):
            raise FileNotFoundError(
                f"Config file not found at {config_path_resolved}"
                f"you need to create a config file at this path"
                f"or change the environment variable {self.app_config.config_env_var}"
            )

        with open(config_path_resolved) as file:
            yaml_content = yaml.safe_load(file)
            if yaml_content is None or self.app_config.config_yaml_root_key not in yaml_content:
                raise ValueError(f"Config file must contain '{self.app_config.config_yaml_root_key}' root key")
            config_dict = yaml_content[self.app_config.config_yaml_root_key]
            raw_otai_config = RawOpenTicketAIConfig.model_validate(config_dict)
        self._logger.info(f"Loaded config from {config_path}")
        return raw_otai_config


def load_config(
    config_path: str | os.PathLike[str] | None = None, app_config: AppConfig | None = None
) -> RawOpenTicketAIConfig:
    """Standalone helper function to load configuration.

    Args:
        config_path: Path to the configuration file
        app_config: Optional AppConfig instance (uses default if not provided)

    Returns:
        Loaded RawOpenTicketAIConfig instance
    """
    if app_config is None:
        app_config = AppConfig()

    loader = ConfigLoader(app_config)
    return loader.load_config(config_path)
