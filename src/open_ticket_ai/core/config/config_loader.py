import os

import yaml
from injector import inject, singleton

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


@singleton
class ConfigLoader:
    @inject
    def __init__(self, app_config: AppConfig, config_path: str | None = None):
        self.app_config = app_config
        if config_path is None:
            self.config_path = os.getenv(app_config.config_env_var)
        else:
            self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> RawOpenTicketAIConfig:
        if self.config_path is None:
            raise ValueError(
                f"Config path not provided and {self.app_config.config_env_var} environment variable not set"
            )
        with open(self.config_path) as file:
            config_dict = yaml.safe_load(file)[self.app_config.config_yaml_root_key]
            return RawOpenTicketAIConfig.model_validate(config_dict)

    def get_config(self):
        return self.config
