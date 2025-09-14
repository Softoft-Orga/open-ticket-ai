"""Top level orchestration utilities."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import schedule

from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext

if TYPE_CHECKING:  # pragma: no cover - imported only for type hints
    from open_ticket_ai.src.core.pipeline.pipeline import Pipeline


class Orchestrator:
    def __init__(self, pipelines: list[Pipeline], config: OpenTicketAIConfig):
        self.config = config
        self._logger = logging.getLogger(__name__)
        self.pipelines = pipelines

    def set_schedules(self) -> None:
        for pipeline in self.pipelines:
            def pipeline_job(pipeline=pipeline) -> None:
                """Execute the provided pipeline within a new context.

                Using the loop variable directly inside the nested function would
                cause all scheduled jobs to reference the *same* pipeline
                instance (the last one from the loop) due to Python's late
                binding behaviour for closures.  By capturing the current
                pipeline as a default argument we ensure each job keeps a
                reference to the pipeline it was created for.
                """

                pipeline.execute(PipelineContext())

            # Look up the scheduling unit dynamically (e.g. ``seconds``,
            # ``minutes``) and register the job.
            getattr(
                schedule.every(pipeline.config.schedule.interval),
                pipeline.config.schedule.unit,
            ).do(pipeline_job)
