from __future__ import annotations

import asyncio
import logging
from injector import Injector

from open_ticket_ai.src.core.dependency_injection.container import AppModule
from open_ticket_ai.src.core.orchestrator import Orchestrator

logger = logging.getLogger(__name__)


def get_container():
    """Create the dependency injection container.

    Imported lazily to avoid importing heavy dependencies during module import,
    which also makes the function easy to patch in tests.
    """
    injector = Injector([AppModule()])

    # 3. Get the top-level object (App)
    return injector



async def run() -> None:
    """Initialise and start the Open Ticket AI application."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger.info("Starting Open Ticket AI...")

    container = get_container()
    orchestrator = container.get(Orchestrator)
    await orchestrator.run()


if __name__ == "__main__":  # pragma: no cover - manual execution
    asyncio.run(run())
