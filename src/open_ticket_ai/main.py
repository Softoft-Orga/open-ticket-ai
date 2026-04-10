import asyncio
import logging
import sys

from open_ticket_ai.app import OpenTicketAIApp
from open_ticket_ai.pipeline import create_pipeline
from open_ticket_ai.settings import Settings


def _configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
        force=True,
    )


async def run() -> None:
    settings = Settings()
    _configure_logging(settings.log_level)

    orchestrator = create_pipeline(settings)
    app = OpenTicketAIApp(orchestrator)
    await app.run()


if __name__ == "__main__":
    asyncio.run(run())
