import logging
from pathlib import Path
import subprocess

import yaml

from open_ticket_ai import AppConfig

logger = logging.getLogger(__name__)
SAFE_ARGS = {"up", "down", "restart", "pull", "-d", "--remove-orphans", "-f"}


class DockerComposeController:
    def __init__(self, compose_file: Path, work_dir: Path) -> None:
        self._compose_file = compose_file
        self._work_dir = work_dir
        self._config_file = compose_file.parent / "config.yml"

    def write_config(self, config: AppConfig, config_file: Path | None = None) -> Path:
        self._work_dir.mkdir(parents=True, exist_ok=True)
        data = config.model_dump(mode="json", exclude_none=True)
        logger.info(f"Config {data}")
        logger.info(f"Writing E2E config to {self._config_file}")
        logger.debug(f"Config services: {list(data.get('open_ticket_ai', {}).get('services', {}).keys())}")

        config_file_path = config_file or self._config_file
        with config_file_path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(data, handle, sort_keys=False)
        logger.info("Config written successfully")
        return self._config_file

    def up(self) -> None:
        logger.info(f"Starting Docker Compose services from {self._compose_file}")
        self._run(["up", "-d", "--remove-orphans"])
        logger.info("Docker Compose services started")

    def down(self) -> None:
        logger.info("Stopping Docker Compose services")
        self._run(["down", "--remove-orphans"])
        logger.info("Docker Compose services stopped")

    def pull(self) -> None:
        logger.info("Pulling Docker Compose service images")
        self._run(["pull"])
        logger.info("Docker Compose service images pulled")

    def remove_config(self) -> None:
        if self._config_file.exists():
            logger.info(f"Removing config file: {self._config_file}")
            self._config_file.unlink()

    def _run(self, args: list[str]) -> None:
        if not all(arg in SAFE_ARGS for arg in args):
            raise ValueError(f"disallowed arg: {args}")
        command = ["docker", "compose", "-f", str(self._compose_file), *args]
        logger.debug(f"Running docker compose command: {' '.join(command)}")
        subprocess.run(command, check=True, cwd=self._work_dir)
