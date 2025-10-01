import asyncio
from pathlib import Path

from open_ticket_ai.main import OpenTicketAIApp

if __name__ == '__main__':
    asyncio.run(OpenTicketAIApp(Path("config.yml")).run())