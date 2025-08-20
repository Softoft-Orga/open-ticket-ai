"""Main application module for OpenTicketAI.

This module contains the `App` class which serves as the primary entry point
for the OpenTicketAI system. It orchestrates configuration validation, job
scheduling, and continuous execution of scheduled tasks.
"""

import logging
import time

import schedule
from injector import inject
from rich.console import Console

from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.core.config.config_validator import OpenTicketAIConfigValidator
from open_ticket_ai.src.orchestrator import Orchestrator

console = Console()
"""Global console instance for rich text output throughout the application."""

class App:
    """Main application entry point for the OpenTicketAI system.

    This class initializes and runs the core application components including:
    - Configuration management
    - Configuration validation
    - Job orchestration and scheduling

    The application follows a scheduled execution model where jobs are run at
    predefined intervals.

    Attributes:
        config: Loaded application configuration.
        validator: Configuration validator instance.
        orchestrator: Job orchestration manager.
    """

    @inject
    def __init__(
            self,
            config: OpenTicketAIConfig,
            validator: OpenTicketAIConfigValidator,
            orchestrator: Orchestrator
    ):
        """Initialize the application with dependencies.

        Args:
            config: Loaded configuration for the application containing all
                necessary parameters and settings.
            validator: Validator instance used to check the integrity and
                correctness of the configuration.
            orchestrator: Orchestrator instance responsible for setting up and
                managing scheduled jobs and attribute predictors.
        """
        self._logger = logging.getLogger(__name__)
        self.config = config
        self.validator = validator
        self.orchestrator = orchestrator

    def run(self):
        """Main execution method for the application.

        Performs the following operations:
        1. Validates the application configuration
        2. Sets up scheduled jobs using the orchestrator
        3. Enters an infinite loop to execute pending scheduled tasks

        The method first validates the configuration registry. If validation fails,
        an error is logged and the application proceeds to setup schedules without
        valid configuration (which may cause runtime errors). On successful validation,
        a success message is printed.

        After setup, the method enters a continuous loop that:
        - Checks for pending scheduled jobs every second
        - Executes any pending jobs found

        Note:
            This method runs indefinitely until interrupted by the user or an unhandled exception.

        Raises:
            KeyboardInterrupt: If the program is interrupted by the user (e.g., via Ctrl+C).
            Exception: Any unhandled exception occurring during the execution of a scheduled job.
        """
        try:
            self.validator.validate_registry()
        except ValueError as e:
            self._logger.error(f"Configuration validation failed: {e}")
        else:
            console.print("[bold green]Configuration validation passed![/bold green]")


        self.orchestrator.set_schedules()
        while True:
            schedule.run_pending()
            time.sleep(1)
