# FILE_PATH: open_ticket_ai\src\ce\main.py
"""Open Ticket AI CLI entry point.

This module provides the command-line interface for the Open Ticket AI application.
It configures logging levels and launches the main application.
"""

import logging

import typer

cli = typer.Typer()
"""The main Typer CLI application instance.

This instance is used to register commands and callbacks for the command-line interface.
"""

@cli.callback()
def main(
    verbose: bool = typer.Option(False, "-v", "--verbose", help="INFO-level logging"),
    debug:   bool = typer.Option(False, "-d", "--debug",   help="DEBUG-level logging"),
):
    # determine log level
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    else:
        level = logging.WARNING

    # configure root logger
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)  # example: quiet noisy libraries

@cli.command()
def start():
    """Start the Open Ticket AI application."""
    from pyfiglet import Figlet
    from open_ticket_ai.src.app import App
    from open_ticket_ai.src.core.dependency_injection.container import DIContainer

    logger = logging.getLogger(__name__)
    f = Figlet(font="slant")
    logger.info("Starting Open Ticket AI")
    print(f.renderText("Open Ticket AI"))
    container = DIContainer()
    app: App = container.get(App)
    app.run()

if __name__ == "__main__":
    cli()
