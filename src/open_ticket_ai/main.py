import asyncio

from injector import Injector

from open_ticket_ai.app import OpenTicketAIApp
from open_ticket_ai.core.dependency_injection.container import AppModule


async def run() -> None:
    container = Injector([AppModule()])
    app = container.get(OpenTicketAIApp)
    await app.run()


if __name__ == "__main__":
    asyncio.run(run())
