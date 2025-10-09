import os
from pathlib import Path

import injector
import yaml
from injector import singleton
from pydantic import ValidationError

from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


@singleton
class ConfigLoader:
    @injector.inject
    def __init__(self, app_config: AppConfig):
        self.app_config = app_config
        self._logger = app_config.get_logger(self.__class__.__name__)

    def load_config(self, config_path: os.PathLike | None = None) -> RawOpenTicketAIConfig:
        if config_path is None and os.getenv(self.app_config.config_env_var) is not None:
            config_path = os.getenv(self.app_config.config_env_var)
        elif config_path is None and os.getenv(self.app_config.config_env_var) is None:
            config_path = self.app_config.get_default_config_path()
            if not config_path.exists():
                raise FileNotFoundError(
                    f"Config file not found at {config_path}."
                    f"To fix this error:"
                    f"Create a confi file at {config_path}"
                    f"or provide a valid config path "
                    f"or set the {self.app_config.config_env_var} environment variable."
                )

        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Config file not found at {config_path}"
                f"you need to create a config file at this path"
                f"or change the environment variable {self.app_config.config_env_var}"
            )

        with open(config_path) as file:
            config_dict = yaml.safe_load(file)[self.app_config.config_yaml_root_key]
            try:
                raw_otai_config = RawOpenTicketAIConfig.model_validate(config_dict)
            except ValidationError as e:
                self._logger.error(f"Validation error while Loading config from {config_path}")
                raise e
        self._logger.info(f"Loaded config from {config_path}")
        return raw_otai_config
