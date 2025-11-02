from textwrap import dedent
from uuid import uuid4

import pytest

from open_ticket_ai.core.config.config_builder import ConfigBuilder
from open_ticket_ai.core.config.pipe_config_builder import PipeConfigBuilder, PipeConfigFactory
from tests.e2e.conftest import (
    DockerComposeController,
    OtoboE2EConfig,
    OtoboTestHelper,
)
from tests.e2e.docs_examples import OTAIConfigExampleMetaInfo, save_example
from tests.e2e.util import wait_for_condition

pytestmark = pytest.mark.e2e


@pytest.mark.asyncio
async def test_update_ticket_subject(
    base_config_builder: ConfigBuilder,
    docker_compose_controller: DockerComposeController,
    otobo_helper: OtoboTestHelper,
    otobo_e2e_config: OtoboE2EConfig,
) -> None:
    _CONFIG_META_INFO = OTAIConfigExampleMetaInfo(
        name="Update Ticket Subject",
        description=dedent("""
        # Update Ticket Subject
        Periodic single-step workflow that sets a ticket’s subject in OTOBO/Znuny.
        Pipe: `base:UpdateTicketPipe` with `ticket_system: otobo_znuny`.
        Key: `ticket_id`, `updated_ticket.subject`, `environment.polling_interval`.
        """),
        tags=["basic", "simple-ticket-system"],
    )
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

    config = base_config_builder.add_orchestrator_pipe(runner).build()

    docker_compose_controller.write_config(config)
    docker_compose_controller.restart()

    async def subject_matches() -> bool:
        ticket = await otobo_helper.get_ticket(ticket_id)
        return ticket.title == updated_subject

    await wait_for_condition(subject_matches)
    save_example(
        config,
        meta=_CONFIG_META_INFO
    )


@pytest.mark.asyncio
async def test_fetch_queue_and_add_note(
    base_config_builder: ConfigBuilder,
    docker_compose_controller: DockerComposeController,
    otobo_helper: OtoboTestHelper,
    otobo_e2e_config: OtoboE2EConfig,
) -> None:
    _CONFIG_META_INFO = OTAIConfigExampleMetaInfo(
        name="Fetch Ticket from Queue and Add Note",
        description="""
            # Simple Ticket: Fetch → Add Note → Move

            Configures a periodic queue processor for OTOBO/Znuny.

            ## Components
            - Orchestrator: SimpleSequential with interval trigger (`environment.polling_interval`)
            - Injects: `ticket_system: otobo_znuny`
            - Pipes:
              1. `base:FetchTicketsPipe` fetches exactly one ticket from `environment.monitored_queue`
              2. `base:AddNotePipe` adds an acknowledgment note (`subject`, `body`)
              3. `base:UpdateTicketPipe` moves the ticket to `environment.cleanup_queue`

            ## Key parameters
            - `environment.monitored_queue`
            - `environment.cleanup_queue`
            - `environment.polling_interval`
            - Note `subject`, `body`

            ## Outcome
            Each cycle processes one ticket: adds the note and moves it to the cleanup queue.
            If the queue is empty, nothing happens.
        """,
        tags=[
            "basic",
            "simple-ticket-system",
        ],
    )

    pipe_factory = PipeConfigFactory()

    # Ensure queue is empty before starting
    await otobo_helper.empty_monitored_queue()

    # Create a single test ticket in the monitored queue
    ticket_id = await otobo_helper.create_ticket(
        subject=f"E2E Queue Ticket {uuid4()}",
        body="This ticket will receive an automated note and be moved",
    )

    note_subject = f"E2E Acknowledgment {uuid4()}"
    note_body = "Your ticket has been received and is being processed."

    otobo_znuny_pipe_builder = PipeConfigBuilder().set_injects({"ticket_system": "otobo_znuny"})

    # Step 1: Fetch ONE ticket from the monitored queue
    fetch_step = (
        otobo_znuny_pipe_builder.copy()
        .set_id("fetch-next-ticket")
        .set_use("base:FetchTicketsPipe")
        .set_params(
            {
                "ticket_search_criteria": {
                    "queue": {"name": otobo_e2e_config.environment.monitored_queue},
                    "limit": 1,  # Process one ticket at a time
                },
            },
        )
        .build()
    )

    # Step 2: Add note to the fetched ticket
    # Use Jinja2 to reference the first (and only) ticket from fetch results
    add_note_step = (
        otobo_znuny_pipe_builder.copy()
        .set_id("add-acknowledgment")
        .set_use("base:AddNotePipe")
        .set_params(
            {
                "ticket_id": "{{ get_pipe_result('fetch-next-ticket', 'fetched_tickets')[0]['id'] }}",
                "note": {
                    "subject": note_subject,
                    "body": note_body,
                },
            },
        )
        .build()
    )

    # Step 3: Move ticket to cleanup queue (marks as processed)
    move_ticket_step = (
        otobo_znuny_pipe_builder.copy()
        .set_id("move-to-processed")
        .set_use("base:UpdateTicketPipe")
        .set_params(
            {
                "ticket_id": "{{ get_pipe_result('fetch-next-ticket', 'fetched_tickets')[0]['id'] }}",
                "updated_ticket": {
                    "queue": {"name": otobo_e2e_config.environment.cleanup_queue},
                },
            },
        )
        .build()
    )

    # Build the composite workflow: fetch -> add note -> move
    composite = (
        pipe_factory.create_composite_builder("process-queue-ticket")
        .add_step(fetch_step)
        .add_step(add_note_step)
        .add_step(move_ticket_step)
        .build()
    )

    # Set up orchestrator to run this workflow repeatedly
    runner = pipe_factory.create_simple_sequential_runner(
        runner_id="queue-processor",
        on=pipe_factory.create_interval_trigger(interval=otobo_e2e_config.environment.polling_interval),
        run=composite,
    )

    # Deploy the configuration
    config = base_config_builder.add_orchestrator_pipe(runner).build()

    docker_compose_controller.write_config(config)
    docker_compose_controller.restart()

    async def tickets_have_note_and_are_moved() -> bool:
        ticket = await otobo_helper.get_ticket(ticket_id)

        articles = ticket.articles or []
        has_note = any(article.subject == note_subject and (note_body in (article.body or "")) for article in articles)

        in_cleanup_queue = ticket.queue.name == otobo_e2e_config.environment.cleanup_queue

        return has_note and in_cleanup_queue

    await wait_for_condition(
        tickets_have_note_and_are_moved,
        timeout=240.0,
        message=f"Ticket {ticket_id} was not processed (note added and moved to cleanup queue)",
    )

    save_example(
        config,
        meta=_CONFIG_META_INFO
    )
