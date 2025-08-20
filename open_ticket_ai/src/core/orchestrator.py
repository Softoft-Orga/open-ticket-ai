"""Top level orchestration utilities."""

from __future__ import annotations

import logging

import schedule

from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.core.dependency_injection.abstract_container import (
    AbstractContainer,
)
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipeline import Pipeline


class Orchestrator:
    """Orchestrates the execution of ticket processing pipelines.

    This class manages the lifecycle of pipelines including:
    - Pipeline instantiation via dependency injection
    - Individual ticket processing
    - Scheduled execution of pipelines

    Attributes:
        config: Configuration settings for the orchestrator
        container: Dependency injection container providing pipeline instances
        _logger: Logger instance for orchestration operations
        _pipelines: Dictionary mapping pipeline IDs to pipeline instances
    """

    def __init__(self, config: OpenTicketAIConfig, container: AbstractContainer):
        """Initialize the Orchestrator with configuration and DI container.

        Args:
            config: Configuration settings for the orchestrator.
            container: Dependency injection container providing pipeline instances.
        """
        self.config = config
        self.container = container
        self._logger = logging.getLogger(__name__)
        self._pipelines: dict[str, Pipeline] = {}

    def process_ticket(self, ticket_id: str, pipeline: Pipeline) -> PipelineContext:
        """Executes a pipeline for a specific ticket.

        Creates a processing context and runs the specified pipeline to process
        the given ticket. This is the core method for individual ticket processing.

        Args:
            ticket_id: Unique identifier of the ticket to process.
            pipeline: Pipeline instance to execute.

        Returns:
            PipelineContext: The execution context containing results and state
                after pipeline execution.
        """
        return pipeline.execute(PipelineContext(ticket_id=ticket_id))

    def build_pipelines(self) -> None:
        """Instantiates all configured pipeline objects.

        Uses the dependency injection container to create pipeline instances
        based on the configuration. Populates the internal pipeline registry
        with pipeline ID to instance mappings.
        """
        for pipeline_cfg in self.config.pipelines:
            self._pipelines[pipeline_cfg.id] = self.container.get_pipeline(pipeline_cfg.id)

    def set_schedules(self) -> None:
        """Configures scheduled execution for all pipelines.

        Performs the following operations:
        1. Builds pipelines if not already instantiated
        2. Configures periodic execution for each pipeline according to its
           schedule configuration using the `schedule` library

        The scheduling uses the following configuration parameters:
        - interval: Numeric interval value
        - unit: Time unit (e.g., minutes, hours, days)

        Note:
        - Uses `schedule.every(interval).unit` pattern for scheduling
        - Passes an empty ticket_id context during scheduled executions
        """
        self.build_pipelines()
        for pipeline_cfg in self.config.pipelines:
            pipeline = self._pipelines[pipeline_cfg.id]
            sched = getattr(
                schedule.every(pipeline_cfg.schedule.interval), pipeline_cfg.schedule.unit
            )
            sched.do(pipeline.execute, PipelineContext(ticket_id=""))
