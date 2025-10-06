import os

import yaml
from injector import singleton

from open_ticket_ai.open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


@singleton
class ConfigLoader:
    def __init__(self, config_path: str | None = None):
        if config_path is None:
            self.config_path = os.getenv("OPEN_TICKET_AI_CONFIG")
        else:
            self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> RawOpenTicketAIConfig:
        if self.config_path is None:
            raise ValueError("Config path not provided and OPEN_TICKET_AI_CONFIG environment variable not set")
        with open(self.config_path) as file:
            config_dict = yaml.safe_load(file)["open_ticket_ai"]
            return RawOpenTicketAIConfig.model_validate(config_dict)

    def get_config(self):
        return self.config
