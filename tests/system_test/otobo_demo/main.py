import asyncio
from pathlib import Path

from dotenv import load_dotenv

from open_ticket_ai.main import OpenTicketAIApp

if __name__ == '__main__':
    load_dotenv(override=True)
    asyncio.run(OpenTicketAIApp(Path(__file__).parent / "config.yml").run())
