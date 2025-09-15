
import asyncio
import logging

from injector import inject

from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.core.pipeline.pipeline import Pipeline


class Orchestrator:
    @inject
    def __init__(self, pipeline: Pipeline, config: OpenTicketAIConfig):
        self.config = config
        self._logger = logging.getLogger(__name__)
        self.pipeline = pipeline

    async def run(self) -> None:
        self._logger.info("Starting orchestrator...")

        while True:
            await self.pipeline.execute()
            await asyncio.sleep(self.config.run_every_seconds)
