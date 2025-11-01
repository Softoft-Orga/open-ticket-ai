import asyncio
import time
from collections.abc import Awaitable, Callable
from uuid import uuid4

import pytest

from open_ticket_ai.core.config.config_builder import ConfigBuilder
from open_ticket_ai.core.config.pipe_config_builder import PipeConfigFactory
from tests.e2e.conftest import (
    DockerComposeController,
    OtoboE2EConfig,
    OtoboTestHelper,
)

pytestmark = pytest.mark.e2e


async def wait_for_condition(
    check: Callable[[], Awaitable[bool]],
    *,
    timeout: float = 10.0,
    interval: float = 0.1,
    message: str | None = None,
) -> None:
    deadline = time.monotonic() + timeout
    await asyncio.sleep(min(interval, 0.1))

    while True:
        if await check():
            return

        if time.monotonic() >= deadline:
            error_msg = message or f"Timed out after {timeout}s waiting for condition"
            raise AssertionError(error_msg)

        await asyncio.sleep(interval)


@pytest.mark.asyncio
async def test_update_ticket_subject(
    base_config_builder: ConfigBuilder,
    docker_compose_controller: DockerComposeController,
    otobo_helper: OtoboTestHelper,
    otobo_e2e_config: OtoboE2EConfig,
) -> None:
    pipe_factory = PipeConfigFactory()
    original_subject = f"E2E Update {uuid4()}"
    ticket_id = await otobo_helper.create_ticket(subject=original_subject, body="initial subject validation")
    updated_subject = f"{original_subject} :: updated"

    update_pipe = pipe_factory.create_pipe(
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
    composite = pipe_factory.create_composite_builder("update-workflow").add_step(update_pipe).build()
    runner = pipe_factory.create_simple_sequential_runner(
        runner_id="update-runner",
        on=pipe_factory.create_interval_trigger(interval=otobo_e2e_config.environment.polling_interval),
        run=composite,
    )

    builder = base_config_builder
    builder.add_orchestrator_pipe(runner)
    config = builder.build()

    docker_compose_controller.write_config(config)
    docker_compose_controller.write_config_to_test_storage(config, "test_update_ticket_subject")
    docker_compose_controller.restart()

    async def subject_matches() -> bool:
        ticket = await otobo_helper.get_ticket(ticket_id)
        return ticket.title == updated_subject

    await wait_for_condition(subject_matches)


@pytest.mark.asyncio
async def test_fetch_queue_and_add_note(
    base_config_builder: ConfigBuilder,
    docker_compose_controller: DockerComposeController,
    otobo_helper: OtoboTestHelper,
    otobo_e2e_config: OtoboE2EConfig,
) -> None:
    """
    Demonstrate: Queue monitoring with automated note addition

    Use Case:
        Monitor a support queue and automatically add a standardized note to
        each new ticket. The orchestrator runs continuously, processing one
        ticket at a time on each run.

    Real-World Example:
        Every minute, check the "New Tickets" queue and add an acknowledgment
        note to the first unprocessed ticket, then move it to "In Progress".

    Configuration Pattern:
        - Fetch one ticket from queue
        - Add note to that ticket
        - Move ticket to cleanup queue (marks as "processed")
        - Orchestrator runs repeatedly, processing tickets one by one

    What This Tests:
        1. Continuous queue monitoring (repeated orchestrator runs)
        2. Processing tickets individually
        3. Using Jinja2 to reference fetched ticket data
        4. Moving tickets between queues after processing
    """
    pipe_factory = PipeConfigFactory()

    # Ensure queue is empty before starting
    await otobo_helper.empty_monitored_queue()

    # Create a single test ticket in the monitored queue
    test_subject = f"E2E Queue Ticket {uuid4()}"
    ticket_id = await otobo_helper.create_ticket(
        subject=test_subject, body="This ticket will receive an automated note and be moved"
    )

    note_subject = f"E2E Acknowledgment {uuid4()}"
    note_body = "Your ticket has been received and is being processed."

    # Step 1: Fetch ONE ticket from the monitored queue
    fetch_step = pipe_factory.create_pipe(
        "fetch-next-ticket",
        "base:FetchTicketsPipe",
        params={
            "ticket_search_criteria": {
                "queue": {"name": otobo_e2e_config.environment.monitored_queue},
                "limit": 1,  # Process one ticket at a time
            }
        },
        injects={"ticket_system": "otobo_znuny"},
    )

    # Step 2: Add note to the fetched ticket
    # Use Jinja2 to reference the first (and only) ticket from fetch results
    add_note_step = pipe_factory.create_pipe(
        "add-acknowledgment",
        "base:AddNotePipe",
        params={
            "ticket_id": "{{ get_pipe_result('fetch-next-ticket', 'fetched_tickets')[0]['id'] }}",
            "note": {
                "subject": note_subject,
                "body": note_body,
            },
        },
        injects={"ticket_system": "otobo_znuny"},
    )

    # Step 3: Move ticket to cleanup queue (marks as processed)
    move_ticket_step = pipe_factory.create_pipe(
        "move-to-processed",
        "base:UpdateTicketPipe",
        params={
            "ticket_id": "{{ get_pipe_result('fetch-next-ticket', 'fetched_tickets')[0]['id'] }}",
            "updated_ticket": {
                "queue": {"name": otobo_e2e_config.environment.cleanup_queue},
            },
        },
        injects={"ticket_system": "otobo_znuny"},
    )

    # Build the composite workflow: fetch -> add note -> move
    composite_builder = pipe_factory.create_composite_builder("process-queue-ticket")
    composite_builder.add_step(fetch_step)
    composite_builder.add_step(add_note_step)
    composite_builder.add_step(move_ticket_step)
    composite = composite_builder.build()

    # Set up orchestrator to run this workflow repeatedly
    runner = pipe_factory.create_simple_sequential_runner(
        runner_id="queue-processor",
        on=pipe_factory.create_interval_trigger(interval=otobo_e2e_config.environment.polling_interval),
        run=composite,
    )

    # Deploy the configuration
    builder = base_config_builder
    builder.add_orchestrator_pipe(runner)
    config = builder.build()

    docker_compose_controller.write_config(config)
    docker_compose_controller.write_config_to_test_storage(config, "test_fetch_queue_and_add_note")
    docker_compose_controller.restart()

    # Verify: The ticket should receive the note AND be moved to cleanup queue
    async def ticket_processed() -> bool:
        """Check if ticket has the note and is in the cleanup queue"""
        ticket = await otobo_helper.get_ticket(ticket_id)

        # Check if note was added
        articles = ticket.articles or []
        has_note = any(article.subject == note_subject and (note_body in (article.body or "")) for article in articles)

        # Check if ticket was moved to cleanup queue
        in_cleanup_queue = ticket.queue.name == otobo_e2e_config.environment.cleanup_queue

        return has_note and in_cleanup_queue

    await wait_for_condition(
        ticket_processed,
        timeout=240.0,
        message=f"Ticket {ticket_id} was not processed (note added and moved to cleanup queue)",
    )
