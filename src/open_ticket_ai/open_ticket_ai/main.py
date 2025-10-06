import asyncio
import os

from injector import Injector

from open_ticket_ai.open_ticket_ai.app import OpenTicketAIApp
from open_ticket_ai.open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.open_ticket_ai.core.pipeline.pipe_factory import PipeFactory
from open_ticket_ai.open_ticket_ai.core.plugins.manager import PluginManager


def get_container():
    config_path = os.getenv("OPEN_TICKET_AI_CONFIG")
    injector = Injector([AppModule(config_path)])

    plugin_manager = injector.get(PluginManager)
    pipe_factory = injector.get(PipeFactory)
    plugin_manager.register_pipes(pipe_factory)

    return injector


async def run() -> None:
    container = get_container()
    app = container.get(OpenTicketAIApp)
    await app.run()


if __name__ == "__main__":
    asyncio.run(run())
