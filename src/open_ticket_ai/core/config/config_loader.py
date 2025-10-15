import os
from pathlib import Path

import injector
import yaml
from injector import singleton

from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory


@singleton
class ConfigLoader:
    @injector.inject
    def __init__(self, app_config: AppConfig, logger_factory: LoggerFactory):
        self.app_config = app_config
        self._logger = logger_factory.create(self.__class__.__name__)

    def load_config(self, config_path: os.PathLike | None = None) -> RawOpenTicketAIConfig:
        if config_path is None:
            env_path = os.getenv(self.app_config.config_env_var)
            config_path = env_path if env_path else self.app_config.get_default_config_path()

        if not Path(config_path).exists():
            raise FileNotFoundError(
                f"Config file not found at {config_path}. "
                f"Create a config file at this path, provide a valid path, "
                f"or set the {self.app_config.config_env_var} environment variable."
            )

        with open(config_path) as file:
            yaml_content = yaml.safe_load(file)
            if yaml_content is None or self.app_config.config_yaml_root_key not in yaml_content:
                raise ValueError(f"Config file must contain '{self.app_config.config_yaml_root_key}' root key")
            config_dict = yaml_content[self.app_config.config_yaml_root_key]
            raw_otai_config = RawOpenTicketAIConfig.model_validate(config_dict)
        self._logger.info(f"Loaded config from {config_path}")
        return raw_otai_config
