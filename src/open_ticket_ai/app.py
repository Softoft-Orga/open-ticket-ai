from injector import inject

from open_ticket_ai.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory


class OpenTicketAIApp:
    @inject
    def __init__(self, config: OpenTicketAIConfig, pipe_factory: PipeFactory, logger_factory: LoggerFactory):
        self._config = config
        self._orchestrator = pipe_factory.render_pipe(config.orchestrator, PipeContext.empty())
        self._logger = logger_factory.create(self.__class__.__name__)

    async def run(self) -> None:
        self._logger.info("🚀 Starting Open Ticket AI orchestration...")
        self._logger.info(f"📦 Loaded {len(self._config.services)} services")
        self._logger.info(f"🔧 Orchestrator has {len(self._config.orchestrator.runners)} runners\n")

        try:
            await self._orchestrator.process(PipeContext.empty())
        except KeyboardInterrupt:
            self._logger.info("\n⚠️  Shutdown requested...")

        self._logger.info("✅ Orchestration complete")
