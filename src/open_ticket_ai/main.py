import logging
import sys

import uvicorn

from open_ticket_ai.api.app import create_app
from open_ticket_ai.settings import Settings


def _configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
        force=True,
    )


def run() -> None:
    settings = Settings()
    _configure_logging(settings.log_level)

    app = create_app(settings)
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)


if __name__ == "__main__":
    run()
