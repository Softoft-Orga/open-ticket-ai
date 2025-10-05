import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from open_ticket_ai.main import run

CONFIG_PATH = Path(__file__).parent / "config.yml"


if __name__ == "__main__":
    load_dotenv(override=True)
    os.environ["OPEN_TICKET_AI_CONFIG"] = str(CONFIG_PATH)

    asyncio.run(run())
