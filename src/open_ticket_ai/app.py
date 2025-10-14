from injector import inject

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.orchestrator import Orchestrator


class OpenTicketAIApp:
    @inject
    def __init__(self, config: RawOpenTicketAIConfig, orchestrator: Orchestrator, logger_factory: LoggerFactory):
        self.config = config
        self.orchestrator = orchestrator

        self._logger = logger_factory.create(self.__class__.__name__)

    async def run(self) -> None:
        self._logger.info("🚀 Starting Open Ticket AI orchestration...")
        self._logger.info(f"📦 Loaded {len(self.config.services)} services")
        self._logger.info(f"🔧 Orchestrator has {len(self.config.orchestrator.runners)} runners\n")

        try:
            await self.orchestrator.run()
        except KeyboardInterrupt:
            self._logger.info("\n⚠️  Shutdown requested...")
            self.orchestrator.stop()

        self._logger.info("✅ Orchestration complete")
