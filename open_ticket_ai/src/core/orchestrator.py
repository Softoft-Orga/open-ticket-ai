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
    def __init__(self, pipelines: list[Pipeline], config: OpenTicketAIConfig):
        self.config = config
        self._logger = logging.getLogger(__name__)
        self.pipelines = pipelines

    def set_schedules(self) -> None:
        for pipeline in self.pipelines:
            def pipeline_job():
                pipeline.execute(PipelineContext())

            schedule.every(pipeline.config.schedule.interval).__getattribute__(pipeline.config.schedule.unit).do(
                pipeline_job
            )
