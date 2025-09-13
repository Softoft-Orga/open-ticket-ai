# FILE_PATH: open_ticket_ai\src\ce\core\mixins\registry_providable_instance.py
import logging

from injector import inject
from rich.console import Console

from open_ticket_ai.src.core.config.config_models import ProvidableConfig
from open_ticket_ai.src.core.util.pretty_print_config import pretty_print_config


class Providable:
    @inject
    def __init__(self, config: ProvidableConfig, console: Console | None = None):
        self.console = console or Console()
        self.config: ProvidableConfig = config
        logger = logging.getLogger(__name__)
        logger.info(f"Initializing {self.__class__.__name__} with config:")
        self._pretty_print()

    def _pretty_print(self):
        if self.config and self.console:
            pretty_print_config(self.config, self.console)

    @classmethod
    def get_provider_key(cls) -> str:
        return cls.__name__
