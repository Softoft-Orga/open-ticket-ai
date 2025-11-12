import asyncio
import logging
import os
from textwrap import dedent
import time
from uuid import uuid4

import pytest

from open_ticket_ai.core.config.config_builder import ConfigBuilder
from open_ticket_ai.core.config.pipe_config_builder import PipeConfigBuilder, PipeConfigFactory
from tests.e2e.test_util.e2e_ticketsystem_helper import E2ETicketsystemHelper
from tests.e2e.test_util.docker_compose_controller import DockerComposeController
from tests.e2e.test_util.e2e_ticketsystem_config import OtoboE2EConfig
from tests.e2e.docs_examples import OTAIConfigExampleMetaInfo, save_example
from tests.e2e.test_util.util import wait_for_condition

pytestmark = pytest.mark.e2e


@pytest.mark.asyncio
async def test_e2e_classify_sets_ticket_subject(
    base_config_builder: ConfigBuilder,
    docker_compose_controller: DockerComposeController,
    otobo_helper: E2ETicketsystemHelper,
    otobo_e2e_config: OtoboE2EConfig,
) -> None:
    _CONFIG_META_INFO = OTAIConfigExampleMetaInfo(
        name="Classify Text and Set Ticket Subject",
        md_description="Classifies text with a local HF model and sets the ticket subject to <LABEL>;<SCORE>.",
        md_details=dedent("""
        Classifies a fixed text via HF local model and updates the ticket subject to the predicted label and confidence.

        Components:
        - Pipes: base:ClassificationPipe -> base:UpdateTicketPipe
        - Injects: classification_service: hf_local, ticket_system: otobo_znuny

        Notes:
        - Subject format: <LABEL>;<SCORE> where SCORE is 0–1
        """).strip(),
        tags=["basic", "simple-ai", "simple-ticket-system"],
    )

    base_config_builder.add_service(
        "hf_local",
        "hf-local:HFClassificationService",
        params={"api_token": os.getenv("E2E_HF_TOKEN")},
    )

    pipe_factory = PipeConfigFactory()

    ticket_id = await otobo_helper.create_ticket(subject=f"E2E Classify {uuid4()}", body="seed")
    expected_label = "POS"

    classify_step = (
        PipeConfigBuilder()
        .set_injects({"classification_service": "hf_local"})
        .set_id("classify")
        .set_use("base:ClassificationPipe")
        .set_params(
            {
                "text": "I absolutely love this product. It works perfectly and I would recommend it to everyone.",
                "model_name": "finiteautomata/bertweet-base-sentiment-analysis",
            },
        )
        .build()
    )

    subject_template = "{{ get_pipe_result('classify', 'label') }};{{ get_pipe_result('classify', 'confidence') }}"
    update_subject_step = (
        PipeConfigBuilder()
        .set_injects({"ticket_system": "otobo_znuny"})
        .set_id("set-subject-to-label-score")
        .set_use("base:UpdateTicketPipe")
        .set_params(
            {
                "ticket_id": ticket_id,
                "updated_ticket": {
                    "subject": subject_template,
                },
            },
        )
        .build()
    )

    composite = (
        pipe_factory.create_composite_builder("classify-and-update-subject")
        .add_step(classify_step)
        .add_step(update_subject_step)
        .build()
    )

    runner = pipe_factory.create_simple_sequential_runner(
        runner_id="runner",
        on=pipe_factory.create_interval_trigger(interval=otobo_e2e_config.environment.polling_interval),
        run=composite,
    )

    config = base_config_builder.add_orchestrator_pipe(runner).build()
    save_example(config, meta=_CONFIG_META_INFO)

    docker_compose_controller.write_config(config)
    docker_compose_controller.down()
    time.sleep(2)
    await asyncio.sleep(2)
    docker_compose_controller.up()

    async def subject_matches() -> bool:
        ticket = await otobo_helper.get_ticket(ticket_id)
        parts = (ticket.title or "").split(";")
        logging.info(f"Ticket title {ticket.title}")
        if len(parts) != 2:
            return False
        label = parts[0].strip()
        try:
            score = float(parts[1].strip())
        except ValueError:
            return False
        return label == expected_label and 0.8 <= score <= 1.0

    await wait_for_condition(subject_matches, timeout=300.0,
        message="Ticket subject was not updated with expected classification label and score")
