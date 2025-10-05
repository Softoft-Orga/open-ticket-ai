import asyncio
import os

from injector import Injector

from open_ticket_ai.app import OpenTicketAIApp
from open_ticket_ai.core.dependency_injection.container import AppModule


def get_container():
    config_path = os.getenv("OPEN_TICKET_AI_CONFIG")
    injector = Injector([AppModule(config_path)])
    return injector


async def run() -> None:
    container = get_container()
    app = container.get(OpenTicketAIApp)
    await app.run()


if __name__ == "__main__":
    asyncio.run(run())
