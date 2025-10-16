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

    def load_config(self) -> RawOpenTicketAIConfig:
        if not self.app_config.config_file_path.exists():
            raise FileNotFoundError(
                f"Config file not found at {self.app_config.config_file_path}. Create a config file at this path"
            )

        with open(self.app_config.config_file_path) as file:
            yaml_content = yaml.safe_load(file)
            if yaml_content is None or self.app_config.config_yaml_root_key not in yaml_content:
                raise ValueError(f"Config file must contain '{self.app_config.config_yaml_root_key}' root key")
            config_dict = yaml_content[self.app_config.config_yaml_root_key]
            raw_otai_config = RawOpenTicketAIConfig.model_validate(config_dict)
        self._logger.info(f"Loaded config from {self.app_config.config_file_path}")
        return raw_otai_config
