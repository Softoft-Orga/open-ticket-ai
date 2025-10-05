import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from open_ticket_ai.core.config.config_models import load_config
from open_ticket_ai.app import OpenTicketAIApp
from open_ticket_ai.main import run

CONFIG_PATH = Path(__file__).parent / "config.yml"


if __name__ == '__main__':
    load_dotenv(override=True)
    os.environ["OPEN_TICKET_AI_CONFIG"] = str(CONFIG_PATH)
    os.environ["PREFECT_API_URL"] = "http://localhost:4200/api"
    os.environ["PREFECT_SERVER_ALLOW_EPHEMERAL_MODE"] = "false"

    asyncio.run(run())
