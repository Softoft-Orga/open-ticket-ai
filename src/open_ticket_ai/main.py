import asyncio
import tomllib
from logging.config import dictConfig
from pathlib import Path

import pyfiglet
from injector import Injector

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.core.pipeline.orchestrator import Orchestrator

# Create the banner text
# Print the banner


def get_project_info():
    """Reads and returns project metadata from pyproject.toml."""
    pyproject_path = Path("../../pyproject.toml")

    # Define default values for robustness
    defaults = {
        "name": "Open Ticket AI",
        "version": "unknown",
        "license": "Not specified",
        "author_name": "Unknown",
        "author_email": "Unknown",
        "homepage": "Not specified",
    }

    if not pyproject_path.exists():
        return defaults

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    # Safely access nested keys using .get()
    project_data = data.get("project", {})

    # Get author info (takes the first author from the list)
    authors = project_data.get("authors", [{}])
    author_name = authors[0].get("name", defaults["author_name"])
    author_email = authors[0].get("email", defaults["author_email"])

    # Get license text
    license_info = project_data.get("license", {}).get("text", defaults["license"])

    # Get homepage URL
    homepage = project_data.get("urls", {}).get("Homepage", defaults["homepage"])

    return {
        "name": project_data.get("name", defaults["name"]),
        "version": project_data.get("version", defaults["version"]),
        "license": license_info,
        "author_name": author_name,
        "author_email": author_email,
        "homepage": homepage,
    }


def get_container():
    """Create the dependency injection container.

    Imported lazily to avoid importing heavy dependencies during module import,
    which also makes the function easy to patch in tests.
    """
    injector = Injector([AppModule()])

    # 3. Get the top-level object (App)
    return injector


async def run() -> None:
    """Initialise and start the Open Ticket AI application."""
    project_info = get_project_info()

    banner = pyfiglet.figlet_format(project_info["name"])
    print(banner)

    # Print all project details
    print(f" Version: {project_info['version']}")
    print(f" License: {project_info['license']}")
    print(f" Author:  {project_info['author_name']} <{project_info['author_email']}>")
    print(f" Website: {project_info['homepage']}\n")

    container = get_container()
    orchestrator = container.get(Orchestrator)
    config = container.get(RawOpenTicketAIConfig)
    dictConfig(config.logging)
    await orchestrator.run()


if __name__ == "__main__":  # pragma: no cover - manual execution
    asyncio.run(run())
