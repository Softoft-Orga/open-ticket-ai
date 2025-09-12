# FILE_PATH: open_ticket_ai\src\ce\core\mixins\registry_providable_instance.py
import logging

from injector import inject
from rich.console import Console

from open_ticket_ai.src.core.config.config_models import ProvidableConfig
from open_ticket_ai.src.core.util.pretty_print_config import pretty_print_config


class Providable:
    """Base class for objects that can be provided by a registry.

    This class provides common functionality for registry-managed objects including
    configuration storage, pretty printing of configuration, and provider registration.

    Attributes:
        console (Console): Rich console instance for output formatting.
        config (ProvidableConfig): Configuration object for this instance.
    """

    @inject
    def __init__(self, config: ProvidableConfig, console: Console | None = None):
        """Initializes the instance with configuration and console.

        Stores the provided configuration and initializes a Rich Console instance if not provided.
        Logs the initialization event and pretty-prints the configuration.

        Args:
            config: Configuration object for this instance.
            console: Optional Rich Console instance for output formatting. If not provided,
                     a new Console instance will be created.
        """
        self.console = console or Console()
        self.config: ProvidableConfig = config
        logger = logging.getLogger(__name__)
        logger.info(f"Initializing {self.__class__.__name__} with config:")
        self._pretty_print()

    def _pretty_print(self):
        """Prints the instance configuration in a human-readable format.

        Uses the `pretty_print_config` utility to display the configuration
        attributes in a structured and visually appealing way using the Rich library.
        """
        if self.config and self.console:
            pretty_print_config(self.config, self.console)

    @classmethod
    def get_provider_key(cls) -> str:
        """
        Return the provider key for the class.

        This key is used to register and retrieve instances from the registry.

        Returns:
            str: The class name used as the registry key.
        """
        return cls.__name__

    @staticmethod
    def get_description() -> str:
        """Return a human readable description for the class.

        This method should be overridden by subclasses to provide specific descriptions.
        The base implementation returns a default placeholder message.

        Returns:
            str: Human-readable description of the class.
        """
        return "No description provided."
