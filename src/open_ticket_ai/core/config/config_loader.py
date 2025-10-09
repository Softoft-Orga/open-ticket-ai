import os

import yaml
from injector import singleton

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


@singleton
class ConfigLoader:

    def load_config(self, config_path) -> RawOpenTicketAIConfig:
        if config_path is None:
            config_path = os.getenv("OPEN_TICKET_AI_CONFIG")
        if config_path is None:
            raise ValueError("Config path not provided and OPEN_TICKET_AI_CONFIG environment variable not set")
        with open(config_path) as file:
            config_dict = yaml.safe_load(file)["open_ticket_ai"]
            return RawOpenTicketAIConfig.model_validate(config_dict)
