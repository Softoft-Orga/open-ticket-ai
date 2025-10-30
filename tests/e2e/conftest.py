from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, AsyncIterator, Iterator

import pytest
import pytest_asyncio
import yaml
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import Article, IdName, TicketCreate, TicketSearch, TicketUpdate

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_builder import ConfigBuilder
from otai_otobo_znuny.models import RenderedOTOBOZnunyTSServiceParams

_DURATION_PATTERN = re.compile(r"^PT(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+(?:\.\d+)?)S)?$")


def _parse_duration_seconds(value: str) -> float:
    match = _DURATION_PATTERN.match(value)
    if not match:
        raise ValueError(value)
    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes") or 0)
    seconds = float(match.group("seconds") or 0.0)
    total = (hours * 3600) + (minutes * 60) + seconds
    if total == 0:
        raise ValueError(value)
    return total


@dataclass(frozen=True)
class OtoboConnectionSettings:
    base_url: str
    username: str
    password: str
    test_queue: str
    new_queue: str
    interval: str
    state_name: str
    priority_name: str
    webservice_name: str = "OpenTicketAI"
    operation_urls: dict[str, str] = field(
        default_factory=lambda: {
            "TicketCreate": "ticket-create",
            "TicketSearch": "ticket-search",
            "TicketGet": "ticket-get",
            "TicketUpdate": "ticket-update",
        }
    )

    @property
    def interval_seconds(self) -> float:
        try:
            return _parse_duration_seconds(self.interval)
        except ValueError:
            return 5.0

    def to_service_params(self) -> dict[str, Any]:
        return {
            "base_url": self.base_url,
            "username": self.username,
            "password": self.password,
            "webservice_name": self.webservice_name,
            "operation_urls": dict(self.operation_urls),
        }


class DockerComposeController:
    def __init__(self, compose_file: Path, work_dir: Path) -> None:
        self._compose_file = compose_file
        self._work_dir = work_dir
        self._config_file = work_dir / "config.yml"

    def write_config(self, config: AppConfig) -> Path:
        self._work_dir.mkdir(parents=True, exist_ok=True)
        data = config.model_dump(mode="json", exclude_none=True)
        with self._config_file.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(data, handle, sort_keys=False)
        return self._config_file

    def restart(self) -> None:
        self.down()
        self.up()

    def up(self) -> None:
        self._run(["up", "-d", "--remove-orphans"])

    def down(self) -> None:
        self._run(["down", "--remove-orphans"])

    def remove_config(self) -> None:
        if self._config_file.exists():
            self._config_file.unlink()

    def _run(self, args: list[str]) -> None:
        command = ["docker", "compose", "-f", str(self._compose_file), *args]
        subprocess.run(command, check=True, cwd=self._work_dir)


class OtoboTestHelper:
    def __init__(self, client: OTOBOZnunyClient, settings: OtoboConnectionSettings) -> None:
        self._client = client
        self._settings = settings
        self._created_ticket_ids: list[str] = []

    async def create_ticket(
            self,
            *,
            subject: str,
            body: str,
            queue_name: str | None = None,
    ) -> str:
        queue_value = queue_name or self._settings.test_queue
        ticket = TicketCreate(
            title=subject,
            queue=IdName(name=queue_value),
            state=IdName(name=self._settings.state_name),
            priority=IdName(name=self._settings.priority_name),
            article=Article(subject=subject, body=body, content_type="text/plain"),
        )
        created = await self._client.create_ticket(ticket)
        if created.id is None:
            raise RuntimeError("Ticket creation did not return an id")
        ticket_id = str(created.id)
        self._created_ticket_ids.append(ticket_id)
        return ticket_id

    async def move_ticket_to_queue(self, ticket_id: str, queue_name: str) -> None:
        await self._client.update_ticket(
            TicketUpdate(
                id=int(ticket_id),
                queue=IdName(name=queue_name),
            )
        )

    async def get_ticket(self, ticket_id: str) -> Any:
        return await self._client.get_ticket(int(ticket_id))

    async def empty_test_queue(self) -> None:
        search = TicketSearch(queues=[IdName(name=self._settings.test_queue)], limit=100)
        while True:
            ticket_ids = await self._client.search_tickets(search)
            if not ticket_ids:
                break
            for identifier in ticket_ids:
                await self.move_ticket_to_queue(str(identifier), self._settings.new_queue)

    async def cleanup(self) -> None:
        for ticket_id in self._created_ticket_ids:
            await self.move_ticket_to_queue(ticket_id, self._settings.new_queue)
        self._created_ticket_ids.clear()


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

    work_dir = tmp_path_factory.mktemp("e2e_compose")
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
def otobo_settings() -> OtoboConnectionSettings:
    password = os.getenv("OTAI_E2E_OTOBO_PASSWORD") or os.getenv("OTAI_OTOBO_DEMO_PASSWORD")
    if not password:
        pytest.skip("OTAI_E2E_OTOBO_PASSWORD or OTAI_OTOBO_DEMO_PASSWORD must be set for OTOBO E2E tests")
    base_url = os.getenv("OTAI_E2E_OTOBO_BASE_URL", "http://3.66.72.29/otobo/nph-genericinterface.pl")
    username = os.getenv("OTAI_E2E_OTOBO_USERNAME", "open_ticket_ai")
    test_queue = os.getenv("OTAI_E2E_TEST_QUEUE", "TEST_QUEUE")
    new_queue = os.getenv("OTAI_E2E_NEW_QUEUE", "NEW_QUEUE")
    interval = os.getenv("OTAI_E2E_INTERVAL_ISO", "PT5S")
    state_name = os.getenv("OTAI_E2E_TICKET_STATE", "new")
    priority_name = os.getenv("OTAI_E2E_TICKET_PRIORITY", "3 normal")
    return OtoboConnectionSettings(
        base_url=base_url,
        username=username,
        password=password,
        test_queue=test_queue,
        new_queue=new_queue,
        interval=interval,
        state_name=state_name,
        priority_name=priority_name,
    )


@pytest.fixture
def base_config_builder(otobo_settings: OtoboConnectionSettings) -> ConfigBuilder:
    builder = ConfigBuilder().with_logging(level="DEBUG")
    builder.add_plugin("otai-base")
    builder.add_plugin("otai-otobo-znuny")
    builder.add_jinja_renderer()
    builder.add_service(
        "otobo_znuny",
        "otobo-znuny:OTOBOZnunyTicketSystemService",
        params=otobo_settings.to_service_params(),
    )
    builder.configure_simple_orchestrator(orchestrator_sleep=otobo_settings.interval)
    return builder


@pytest_asyncio.fixture
async def otobo_client(otobo_settings: OtoboConnectionSettings) -> AsyncIterator[OTOBOZnunyClient]:
    params = RenderedOTOBOZnunyTSServiceParams(**otobo_settings.to_service_params())
    client = OTOBOZnunyClient(config=params.to_client_config())
    client.login(params.get_basic_auth())
    try:
        yield client
    finally:
        await client.aclose()


@pytest_asyncio.fixture
async def otobo_helper(
        otobo_client: OTOBOZnunyClient,
        otobo_settings: OtoboConnectionSettings,
) -> AsyncIterator[OtoboTestHelper]:
    helper = OtoboTestHelper(otobo_client, otobo_settings)
    try:
        yield helper
    finally:
        await helper.cleanup()
