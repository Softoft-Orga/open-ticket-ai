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
from open_ticket_ai.src.core.orchestrator import Orchestrator

console = Console()
"""Global console instance for rich text output throughout the application."""


class App:
    @inject
    def __init__(
        self,
        config: OpenTicketAIConfig,
        validator: OpenTicketAIConfigValidator,
        orchestrator: Orchestrator
    ):
        self._logger = logging.getLogger(__name__)
        self.config = config
        self.validator = validator
        self.orchestrator = orchestrator

    def run(self):
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
