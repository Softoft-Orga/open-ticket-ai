import asyncio
from pathlib import Path

from dotenv import load_dotenv

from open_ticket_ai.core.config.config_models import load_config
from open_ticket_ai.main import OpenTicketAIApp
from open_ticket_ai.tools.config_to_mermaid import generate_mermaid_diagram

CONFIG_PATH = Path(__file__).parent / "config.yml"


def generate_mermaid():
    config = load_config(CONFIG_PATH)
    mermaid = generate_mermaid_diagram(config)
    with open(CONFIG_PATH.parent / "config.mmd", "w", encoding="utf-8") as f:
        f.write(mermaid)
    print(f"Mermaid diagram written to {CONFIG_PATH.parent / 'config.mmd'})")


if __name__ == '__main__':
    generate_mermaid()
    #load_dotenv(override=True)
    #asyncio.run(OpenTicketAIApp(Path(__file__).parent / "config.yml").run())
