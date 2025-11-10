from datetime import timedelta
import logging
import os
import shutil
import sys
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
import pytest_asyncio
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient

from open_ticket_ai.core.config.config_builder import ConfigBuilder
from tests.e2e.test_util.docker_compose_controller import logger, DockerComposeController
from tests.e2e.test_util.e2e_ticketsystem_helper import E2ETicketsystemHelper
from tests.e2e.test_util.e2e_ticketsystem_config import OtoboE2EConfig, create_otobo_e2e_config

pytestmark = [pytest.mark.e2e]


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
    work_dir = Path(__file__).parent
    logger.info(f"E2E work directory: {work_dir}")
    controller = DockerComposeController(e2e_compose_file, work_dir)

    controller.down()
    controller.remove_config()
    controller.pull()

    try:
        yield controller
    finally:
        controller.down()


@pytest.fixture(scope="session")
def otobo_e2e_config() -> OtoboE2EConfig:
    """Complete OTOBO E2E test configuration"""
    config = create_otobo_e2e_config()
    logger.info(
        f"OTOBO E2E Config: base_url={config.service.base_url}, monitored_queue={config.environment.monitored_queue}",
    )
    return config


@pytest.fixture
def base_config_builder(otobo_e2e_config: OtoboE2EConfig) -> ConfigBuilder:
    """Base configuration builder with OTOBO service configured"""
    logger.info("Building E2E config with OTOBO service")
    builder = ConfigBuilder().with_logging(level="DEBUG")
    builder.add_jinja_renderer()
    builder.add_service(
        "otobo_znuny",
        "otobo-znuny:OTOBOZnunyTicketSystemService",
        params=otobo_e2e_config.service.model_dump(exclude_none=True),
    )
    builder.set_orchestrator(params={
        "orchestrator_sleep": timedelta(seconds=5),
    })
    logger.info("Config builder ready")
    return builder


@pytest_asyncio.fixture
async def otobo_client(otobo_e2e_config: OtoboE2EConfig) -> AsyncIterator[OTOBOZnunyClient]:
    """OTOBO client for direct API interactions in tests

    Note: This fixture resolves the password from the environment variable directly
    because it creates a client outside the application's normal configuration flow.
    The otobo_e2e_config still contains the Jinja template for use in config.yml.
    """
    password = os.getenv("OTAI_E2E_OTOBO_PASSWORD")
    if not password:
        raise ValueError(
            "OTAI_E2E_OTOBO_PASSWORD environment variable is not set. "
            "This is required for E2E tests to authenticate with OTOBO.",
        )

    # Create a service config with the resolved password for direct client use
    service_config = otobo_e2e_config.service.model_copy(update={"password": password})

    client = OTOBOZnunyClient(config=service_config.to_client_config())
    client.login(service_config.get_basic_auth())
    try:
        yield client
    finally:
        await client.aclose()


@pytest_asyncio.fixture
async def otobo_helper(
    otobo_client: OTOBOZnunyClient,
    otobo_e2e_config: OtoboE2EConfig,
) -> AsyncIterator[E2ETicketsystemHelper]:
    """Helper for OTOBO ticket operations during tests"""
    async with E2ETicketsystemHelper(otobo_client, otobo_e2e_config) as helper:
        yield helper


@pytest.fixture(scope="session", autouse=True)
def configure_e2e_logging():
    """Configure logging for E2E tests"""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)8s] [%(name)s] %(message)s", datefmt="%H:%M:%S"),
    )

    file_handler = logging.FileHandler(log_dir / "e2e_test.log", mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)8s] [%(name)s] (%(filename)s:%(lineno)d) - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ),
    )

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    logger.info("E2E test logging configured")

    yield

    root_logger.removeHandler(console_handler)
    root_logger.removeHandler(file_handler)
