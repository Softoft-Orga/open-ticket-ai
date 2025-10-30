import asyncio
import time
from collections.abc import Awaitable, Callable
from uuid import uuid4

import pytest

from open_ticket_ai.core.config.config_builder import ConfigBuilder
from tests.e2e.conftest import (
    DockerComposeController,
    OtoboConnectionSettings,
    OtoboTestHelper,
)

pytestmark = pytest.mark.e2e


async def wait_for_condition(
        check: Callable[[], Awaitable[bool]],
        *,
        timeout: float,
        poll_interval: float,
) -> None:
    deadline = time.monotonic() + timeout
    await asyncio.sleep(min(poll_interval, 5.0))
    while True:
        if await check():
            return
        if time.monotonic() >= deadline:
            raise AssertionError("Timed out waiting for condition")
        await asyncio.sleep(poll_interval)


@pytest.mark.asyncio
async def test_update_ticket_subject(
        base_config_builder: ConfigBuilder,
        docker_compose_controller: DockerComposeController,
        otobo_helper: OtoboTestHelper,
        otobo_settings: OtoboConnectionSettings,
) -> None:
    original_subject = f"E2E Update {uuid4()}"
    ticket_id = await otobo_helper.create_ticket(subject=original_subject, body="initial subject validation")
    updated_subject = f"{original_subject} :: updated"

    update_pipe = ConfigBuilder.pipe(
        "update-ticket",
        "base:UpdateTicketPipe",
        params={
            "ticket_id": ticket_id,
            "updated_ticket": {
                "subject": updated_subject,
            },
        },
        injects={"ticket_system": "otobo_znuny"},
    )
    composite = ConfigBuilder.composite_pipe(
        "update-workflow",
        steps=[update_pipe],
    )
    runner = ConfigBuilder.simple_sequential_runner(
        runner_id="update-runner",
        on=ConfigBuilder.interval_trigger(interval=otobo_settings.interval),
        run=composite,
    )

    builder = base_config_builder
    builder.add_orchestrator_pipe(runner)
    config = builder.build()

    docker_compose_controller.write_config(config)
    docker_compose_controller.restart()

    async def subject_matches() -> bool:
        ticket = await otobo_helper.get_ticket(ticket_id)
        return ticket.title == updated_subject

    await wait_for_condition(
        subject_matches,
        timeout=180.0,
        poll_interval=max(otobo_settings.interval_seconds, 5.0),
    )


@pytest.mark.asyncio
async def test_fetch_queue_and_add_notes(
        base_config_builder: ConfigBuilder,
        docker_compose_controller: DockerComposeController,
        otobo_helper: OtoboTestHelper,
        otobo_settings: OtoboConnectionSettings,
) -> None:
    await otobo_helper.empty_test_queue()

    ticket_subjects = [f"E2E Queue Ticket {uuid4()}" for _ in range(2)]
    ticket_ids = [
        await otobo_helper.create_ticket(subject=subject, body="queue processing note") for subject in ticket_subjects
    ]

    note_subject = f"E2E Note {uuid4()}"
    note_body = f"Processed by pipeline {uuid4()}"

    fetch_step = ConfigBuilder.pipe(
        "fetch-test-queue",
        "base:FetchTicketsPipe",
        params={
            "ticket_search_criteria": {
                "queue": {"name": otobo_settings.test_queue},
                "limit": len(ticket_ids),
            }
        },
        injects={"ticket_system": "otobo_znuny"},
    )

    note_steps = []
    for index in range(len(ticket_ids)):
        ticket_ref = f"{{{{ get_pipe_result('fetch-test-queue','fetched_tickets')[{index}]['id'] }}}}"
        note_steps.append(
            ConfigBuilder.pipe(
                f"add-note-{index}",
                "base:AddNotePipe",
                params={
                    "ticket_id": ticket_ref,
                    "note": {
                        "subject": note_subject,
                        "body": note_body,
                    },
                },
                injects={"ticket_system": "otobo_znuny"},
            )
        )

    composite = ConfigBuilder.composite_pipe(
        "note-workflow",
        steps=[fetch_step, *note_steps],
    )
    runner = ConfigBuilder.simple_sequential_runner(
        runner_id="note-runner",
        on=ConfigBuilder.interval_trigger(interval=otobo_settings.interval),
        run=composite,
    )

    builder = base_config_builder
    builder.add_orchestrator_pipe(runner)
    config = builder.build()

    docker_compose_controller.write_config(config)
    docker_compose_controller.restart()

    async def notes_applied() -> bool:
        for ticket_id in ticket_ids:
            ticket = await otobo_helper.get_ticket(ticket_id)
            articles = ticket.articles or []
            if not any(article.subject == note_subject and (note_body in (article.body or "")) for article in articles):
                return False
        return True

    await wait_for_condition(
        notes_applied,
        timeout=240.0,
        poll_interval=max(otobo_settings.interval_seconds, 5.0),
    )
