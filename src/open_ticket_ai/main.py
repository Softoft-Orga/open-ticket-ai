import asyncio
import logging
from logging.config import dictConfig
import os
import tomllib
from pathlib import Path
from typing import Any

import pyfiglet
from injector import Injector

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline import Orchestrator
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory


def get_project_info():
    pyproject_path = Path("../../pyproject.toml")

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

    project_data = data.get("project", {})

    authors = project_data.get("authors", [{}])
    author_name = authors[0].get("name", defaults["author_name"])
    author_email = authors[0].get("email", defaults["author_email"])

    license_info = project_data.get("license", {}).get("text", defaults["license"])

    homepage = project_data.get("urls", {}).get("Homepage", defaults["homepage"])

    return {
        "name": project_data.get("name", defaults["name"]),
        "version": project_data.get("version", defaults["version"]),
        "license": license_info,
        "author_name": author_name,
        "author_email": author_email,
        "homepage": homepage,
    }


class OpenTicketAIApp:
    def __init__(self, config_path: str | Path | None = None):
        self._config_path = config_path
        self._injector = Injector([AppModule(config_path)])
        self.print_info()

        dictConfig(self.config.general_config["logging"])

    @property
    def config(self) -> RawOpenTicketAIConfig:
        return self._injector.get(RawOpenTicketAIConfig)

    @property
    def registry(self) -> UnifiedRegistry:
        return self._injector.get(UnifiedRegistry)

    @property
    def pipe_factory(self) -> PipeFactory:
        return self._injector.get(PipeFactory)

    @property
    def injector(self) -> Injector:
        return self._injector

    def print_info(self) -> None:
        project_info = get_project_info()
        banner = pyfiglet.figlet_format(project_info["name"])
        print(banner)
        print(f" Version: {project_info['version']}")
        print(f" License: {project_info['license']}")
        print(f" Author:  {project_info['author_name']} <{project_info['author_email']}>")
        print(f" Website: {project_info['homepage']}\n")

    async def run(self) -> None:
        print("🚀 Starting Open Ticket AI orchestration...")
        print(f"📄 Config loaded from: {self._config_path or 'default location'}")
        print(f"📦 Loaded {len(self.config.defs)} definitions")
        print(f"🔧 Orchestrator has {len(self.config.orchestrator)} step(s)\n")
        
        orchestrator = self._injector.get(Orchestrator)
        
        try:
            await orchestrator.run()
        except KeyboardInterrupt:
            print("\n⚠️  Shutdown requested...")
            await orchestrator.stop()
        
        print("✅ Orchestration complete")


def get_container():
    config_path = os.getenv("OPEN_TICKET_AI_CONFIG")
    injector = Injector([AppModule(config_path)])
    return injector


async def run() -> None:
    config_path = os.getenv("OPEN_TICKET_AI_CONFIG")
    app = OpenTicketAIApp(config_path)
    await app.run()


if __name__ == "__main__":
    asyncio.run(run())
