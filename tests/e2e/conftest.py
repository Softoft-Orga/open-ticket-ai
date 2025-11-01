import logging
import os
import shutil
import subprocess
import sys
from collections.abc import AsyncIterator, Iterator
from datetime import timedelta
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
import yaml
from otai_otobo_znuny.models import OTOBOZnunyTSServiceParams
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import Article, IdName, TicketCreate, TicketSearch, TicketUpdate
from otobo_znuny.domain_models.ticket_operation import TicketOperation
from pydantic import BaseModel, Field

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_builder import ConfigBuilder

logger = logging.getLogger(__name__)
pytestmark = [pytest.mark.e2e]


class OtoboTestEnvironment(BaseModel):
    """Test environment configuration for OTOBO E2E tests"""

    monitored_queue: str = Field(description="Queue that is actively monitored and processed by the test workflows")
    cleanup_queue: str = Field(description="Queue where test tickets are moved for cleanup after tests")
    polling_interval: timedelta = Field(
        default=timedelta(seconds=5), description="How frequently the orchestrator checks for new tickets"
    )

    # Default ticket properties for test ticket creation
    default_state: str = Field(default="new", description="Default state for created test tickets")
    default_priority: str = Field(default="medium", description="Default priority for created test tickets")
    default_type: str = Field(default="Incident", description="Default type for created test tickets")
    default_customer_user: str = Field(default="otai-demo-user", description="Default customer user for test tickets")

    @property
    def interval_seconds(self) -> float:
        return self.polling_interval.total_seconds()


class OtoboE2EConfig(BaseModel):
    """Complete E2E test configuration for OTOBO integration"""

    service: OTOBOZnunyTSServiceParams
    environment: OtoboTestEnvironment


def create_otobo_e2e_config(
    *,
    password: str | None = None,
    base_url: str = "http://3.66.72.29/otobo/nph-genericinterface.pl",
    username: str = "open_ticket_ai",
    webservice_name: str = "OpenTicketAI",
    monitored_queue: str = "~Test-Queue1",
    cleanup_queue: str = "~Test-Queue2",
    polling_interval: timedelta = timedelta(seconds=0.1),
    default_state: str = "new",
    default_priority: str = "medium",
    default_type: str = "Incident",
    default_customer_user: str = "otai-demo-user",
) -> OtoboE2EConfig:
    """
    Factory function to create OTOBO E2E configuration with sensible defaults.

    Args:
        password: OTOBO API password (reads from OTAI_E2E_OTOBO_PASSWORD env var if not provided)
        base_url: OTOBO instance base URL
        username: OTOBO API username
        webservice_name: Name of the OTOBO web service
        monitored_queue: Queue to monitor in tests
        cleanup_queue: Queue for cleaning up test tickets
        polling_interval: How often to poll for tickets
        default_state: Default ticket state for test tickets
        default_priority: Default ticket priority for test tickets
        default_type: Default ticket type for test tickets
        default_customer_user: Default customer user for test tickets

    Returns:
        Configured OtoboE2EConfig instance

    Raises:
        ValueError: If password is not provided and OTAI_E2E_OTOBO_PASSWORD is not set
    """
    # Get password from env if not explicitly provided
    if password is None:
        password = os.getenv("OTAI_E2E_OTOBO_PASSWORD")
        if not password:
            raise ValueError(
                "OTOBO password must be provided via 'password' parameter "
                "or OTAI_E2E_OTOBO_PASSWORD environment variable"
            )

    service = OTOBOZnunyTSServiceParams(
        base_url=base_url,
        username=username,
        password=password,
        webservice_name=webservice_name,
        operation_urls={
            TicketOperation.CREATE.value: "ticket-create",
            TicketOperation.SEARCH.value: "ticket-search",
            TicketOperation.GET.value: "ticket-get",
            TicketOperation.UPDATE.value: "ticket-update",
        },
    )

    environment = OtoboTestEnvironment(
        monitored_queue=monitored_queue,
        cleanup_queue=cleanup_queue,
        polling_interval=polling_interval,
        default_state=default_state,
        default_priority=default_priority,
        default_type=default_type,
        default_customer_user=default_customer_user,
    )

    return OtoboE2EConfig(service=service, environment=environment)


class DockerComposeController:
    def __init__(self, compose_file: Path, work_dir: Path) -> None:
        self._compose_file = compose_file
        self._work_dir = work_dir
        self._config_file = compose_file.parent / "config.yml"

    def write_config_to_test_storage(self, config: AppConfig, test_name: str) -> Path:
        config_file_path = Path(__file__).parent / "config_files" / f"{test_name}-config.yml" or self._config_file
        return self.write_config(config, config_file_path)

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

    def restart(self) -> None:
        logger.info("Restarting Docker Compose services")
        self.down()
        self.up()

    def up(self) -> None:
        logger.info(f"Starting Docker Compose services from {self._compose_file}")
        self._run(["up", "-d", "--remove-orphans"])
        logger.info("Docker Compose services started")

    def down(self) -> None:
        logger.info("Stopping Docker Compose services")
        self._run(["down", "--remove-orphans"])
        logger.info("Docker Compose services stopped")

    def remove_config(self) -> None:
        if self._config_file.exists():
            logger.info(f"Removing config file: {self._config_file}")
            self._config_file.unlink()

    def _run(self, args: list[str]) -> None:
        command = ["docker", "compose", "-f", str(self._compose_file), *args]
        logger.debug(f"Running docker compose command: {' '.join(command)}")
        subprocess.run(command, check=True, cwd=self._work_dir)


class OtoboTestHelper:
    """Helper class for managing OTOBO tickets during E2E tests"""

    def __init__(self, client: OTOBOZnunyClient, config: OtoboE2EConfig) -> None:
        self._client = client
        self._config = config
        self._created_ticket_ids: list[str] = []

    async def create_ticket(
        self,
        *,
        subject: str,
        body: str,
        queue_name: str | None = None,
    ) -> str:
        """Create a test ticket in OTOBO"""
        env = self._config.environment
        queue_value = queue_name or env.monitored_queue

        logger.info(f"Creating test ticket: subject='{subject}', queue='{queue_value}'")
        ticket = TicketCreate(
            title=subject,
            queue=IdName(name=queue_value),
            state=IdName(name=env.default_state),
            priority=IdName(name=env.default_priority),
            type=IdName(name=env.default_type),
            article=Article(subject=subject, body=body, content_type="text/plain"),
            customer_user=env.default_customer_user,
        )
        created = await self._client.create_ticket(ticket)
        if created.id is None:
            raise RuntimeError("Ticket creation did not return an id")
        ticket_id = str(created.id)
        self._created_ticket_ids.append(ticket_id)
        logger.info(f"Ticket created successfully: id={ticket_id}")
        return ticket_id

    async def move_ticket_to_queue(self, ticket_id: str, queue_name: str) -> None:
        """Move a ticket to a different queue"""
        logger.debug(f"Moving ticket {ticket_id} to queue '{queue_name}'")
        await self._client.update_ticket(
            TicketUpdate(
                id=int(ticket_id),
                queue=IdName(name=queue_name),
            )
        )
        logger.debug(f"Ticket {ticket_id} moved to '{queue_name}'")

    async def get_ticket(self, ticket_id: str) -> Any:
        """Fetch a ticket by ID"""
        logger.debug(f"Fetching ticket {ticket_id}")
        return await self._client.get_ticket(int(ticket_id))

    async def empty_monitored_queue(self) -> None:
        """Move all tickets from the monitored queue to the cleanup queue"""
        env = self._config.environment
        logger.info(f"Emptying monitored queue: {env.monitored_queue}")

        search = TicketSearch(queues=[IdName(name=env.monitored_queue)], limit=100)
        total_moved = 0

        while True:
            ticket_ids = await self._client.search_tickets(search)
            if not ticket_ids:
                break
            logger.debug(f"Found {len(ticket_ids)} tickets to move")
            for identifier in ticket_ids:
                await self.move_ticket_to_queue(str(identifier), env.cleanup_queue)
                total_moved += 1

        logger.info(f"Monitored queue emptied: {total_moved} tickets moved")

    async def cleanup(self) -> None:
        """Clean up all tickets created during tests"""
        if not self._created_ticket_ids:
            logger.debug("No tickets to cleanup")
            return

        logger.info(f"Cleaning up {len(self._created_ticket_ids)} test tickets")
        env = self._config.environment

        for ticket_id in self._created_ticket_ids:
            await self.move_ticket_to_queue(ticket_id, env.cleanup_queue)

        self._created_ticket_ids.clear()
        logger.info("Cleanup complete")


@pytest.fixture(scope="session")
def e2e_compose_file() -> Path:
    """Path to E2E-specific docker-compose file"""
    return Path(__file__).parent / "compose.e2e.yml"


@pytest.fixture(scope="session")
def docker_compose_controller(
    e2e_compose_file: Path,
    tmp_path_factory: pytest.TempPathFactory,
) -> Iterator[DockerComposeController]:
    if shutil.which("docker") is None:
        pytest.skip("docker is required for E2E tests")

    skip_compose = os.getenv("OTAI_E2E_SKIP_COMPOSE", "").lower() in ("1", "true", "yes")
    logger.info(f"Docker Compose controller setup (skip_compose={skip_compose})")

    work_dir = tmp_path_factory.mktemp("e2e_compose")
    logger.info(f"E2E work directory: {work_dir}")
    controller = DockerComposeController(e2e_compose_file, work_dir)

    if not skip_compose:
        controller.down()
        controller.remove_config()

    try:
        yield controller
    finally:
        if not skip_compose:
            controller.down()
            controller.remove_config()


@pytest.fixture(scope="session")
def otobo_e2e_config() -> OtoboE2EConfig:
    """Complete OTOBO E2E test configuration"""
    config = create_otobo_e2e_config()
    logger.info(
        f"OTOBO E2E Config: base_url={config.service.base_url}, monitored_queue={config.environment.monitored_queue}"
    )
    return config


@pytest.fixture
def base_config_builder(otobo_e2e_config: OtoboE2EConfig) -> ConfigBuilder:
    """Base configuration builder with OTOBO service configured"""
    logger.info("Building E2E config with OTOBO service")
    builder = ConfigBuilder().with_logging(level="DEBUG")
    builder.add_plugin("otai-base")
    builder.add_plugin("otai-otobo-znuny")
    builder.add_jinja_renderer()
    builder.add_service(
        "otobo_znuny",
        "otobo-znuny:OTOBOZnunyTicketSystemService",
        params=otobo_e2e_config.service.model_dump(exclude_none=True),
    )
    builder.configure_simple_orchestrator(orchestrator_sleep=otobo_e2e_config.environment.polling_interval)
    logger.info("Config builder ready")
    return builder


@pytest_asyncio.fixture
async def otobo_client(otobo_e2e_config: OtoboE2EConfig) -> AsyncIterator[OTOBOZnunyClient]:
    """OTOBO client for direct API interactions in tests"""
    client = OTOBOZnunyClient(config=otobo_e2e_config.service.to_client_config())
    client.login(otobo_e2e_config.service.get_basic_auth())
    try:
        yield client
    finally:
        await client.aclose()


@pytest_asyncio.fixture
async def otobo_helper(
    otobo_client: OTOBOZnunyClient,
    otobo_e2e_config: OtoboE2EConfig,
) -> AsyncIterator[OtoboTestHelper]:
    """Helper for OTOBO ticket operations during tests"""
    helper = OtoboTestHelper(otobo_client, otobo_e2e_config)
    try:
        yield helper
    finally:
        await helper.cleanup()


@pytest.fixture(scope="session", autouse=True)
def configure_e2e_logging():
    """Configure logging for E2E tests"""
    # Create logs directory
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Console handler (for pytest output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s [%(levelname)8s] [%(name)s] %(message)s", datefmt="%H:%M:%S")
    console_handler.setFormatter(console_formatter)

    # File handler (detailed logs)
    file_handler = logging.FileHandler(log_dir / "e2e_test.log", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)8s] [%(name)s] (%(filename)s:%(lineno)d) - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers if not already present
    if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
        root_logger.addHandler(console_handler)
    if not any(isinstance(h, logging.FileHandler) for h in root_logger.handlers):
        root_logger.addHandler(file_handler)

    logger.info("E2E test logging configured")

    yield

    # Cleanup
    root_logger.removeHandler(console_handler)
    root_logger.removeHandler(file_handler)
