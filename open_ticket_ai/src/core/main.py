# FILE_PATH: open_ticket_ai\src\ce\main.py
"""Open Ticket AI CLI entry point.

This module provides the command-line interface for the Open Ticket AI application.
It configures logging levels and launches the main application.
"""

import logging

import typer
from pyfiglet import Figlet

from open_ticket_ai.src.app import App
from open_ticket_ai.src.core.dependency_injection.container import DIContainer

cli = typer.Typer()
"""The main Typer CLI application instance.

This instance is used to register commands and callbacks for the command-line interface.
"""

@cli.callback()
def main(
    verbose: bool = typer.Option(False, "-v", "--verbose", help="INFO-level logging"),
    debug:   bool = typer.Option(False, "-d", "--debug",   help="DEBUG-level logging"),
):
    """Configure logging based on CLI options.

    This function sets the logging level for the application based on the provided command-line flags.
    It supports two levels of verbosity:
    - `--verbose` for INFO level logging
    - `--debug` for DEBUG level logging

    If no flags are provided, the default logging level is WARNING. The function also configures
    log formatting and suppresses noisy libraries (e.g., urllib3).

    Args:
        verbose (bool): Enable INFO-level logging when True.
        debug (bool): Enable DEBUG-level logging when True.
    """
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
    """Initialize the container and start the application.

    This command performs the following actions:
    1. Configures the dependency injection container
    2. Retrieves the main application instance from the container
    3. Runs the application
    4. Displays a stylized startup banner using `pyfiglet`

    The application follows a dependency injection pattern where all required
    dependencies are resolved through the `DIContainer`.
    """
    logger = logging.getLogger(__name__)
    f = Figlet(font="slant")
    logger.info("Starting Open Ticket AI")
    print(f.renderText("Open Ticket AI"))
    container = DIContainer()
    app: App = container.get(App)
    app.run()

if __name__ == "__main__":
    cli()
