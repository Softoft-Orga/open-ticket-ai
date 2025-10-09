import asyncio

from injector import Injector

from open_ticket_ai.app import OpenTicketAIApp
from open_ticket_ai.core.dependency_injection.container import AppModule


def get_container(config_path: str | None = None) -> Injector:
    return Injector([AppModule(config_path)])


async def run(config_path: str | None = None) -> None:
    container = get_container(config_path)
    app = container.get(OpenTicketAIApp)
    await app.run()


if __name__ == "__main__":
    asyncio.run(run())
