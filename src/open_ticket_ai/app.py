import logging

from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext

logger = logging.getLogger(__name__)


class OpenTicketAIApp:
    def __init__(self, orchestrator: Pipe) -> None:
        self._orchestrator = orchestrator

    async def run(self) -> None:
        logger.info("Starting Open Ticket AI orchestration...")
        try:
            await self._orchestrator.process(PipeContext.empty())
        except KeyboardInterrupt:
            logger.info("Shutdown requested...")
        logger.info("Orchestration complete")
