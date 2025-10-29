import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from open_ticket_ai.main import run

CONFIG_DIR = Path(__file__).parent

if __name__ == "__main__":
    load_dotenv(override=True)
    os.chdir(CONFIG_DIR)
    asyncio.run(run())
