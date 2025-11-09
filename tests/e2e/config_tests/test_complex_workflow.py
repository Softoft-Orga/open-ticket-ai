import asyncio
import os
import time
from uuid import uuid4
from textwrap import dedent
import pytest

from open_ticket_ai.core.config.config_builder import ConfigBuilder
from open_ticket_ai.core.config.pipe_config_builder import PipeConfigBuilder, PipeConfigFactory
from tests.e2e.conftest import DockerComposeController, OtoboE2EConfig
from tests.e2e.docs_examples import OTAIConfigExampleMetaInfo, save_example
from tests.e2e.test_util.e2e_ticketsystem_helper import E2ETicketsystemHelper
from tests.e2e.test_util.util import wait_for_condition

pytestmark = pytest.mark.e2e

@pytest.mark.asyncio
async def test_e2e_de_classify_queue_and_priority_and_update_ticket(
    base_config_builder: ConfigBuilder,
    docker_compose_controller: DockerComposeController,
    otobo_helper: E2ETicketsystemHelper,
    otobo_e2e_config: OtoboE2EConfig,
) -> None:
    _CONFIG_META_INFO = OTAIConfigExampleMetaInfo(
        name="Queue Priority",
        md_description="Classifies queue and priority for a German ticket.",
        md_details=dedent("""
        Classifies a German ticket text using HF models to predict queue and priority, then updates the ticket.

        Components:
        - Orchestrator: SimpleSequential with interval trigger
        - Injects: classification_service: hf_local, ticket_system: otobo_znuny
        - Pipes:
          1. base:ClassificationPipe with model softoft/otai-queue-de-bert-v1
          2. base:ClassificationPipe with model softoft/otai-priority-de-bert-v1
          3. base:UpdateTicketPipe applying predicted queue and priority

        """).strip(),
        tags=["simple-ai", "simple-ticket-system"],
    )

    pipe_factory = PipeConfigFactory()

    german_text = dedent("""
    Kritischer Produktionsausfall seit heute Morgen: Unsere zentrale Web-Anwendung für Kundenportale liefert 500-Fehler nach dem letzten Deployment.
    Betroffen sind Login, Bestellübersicht und Zahlungsfreigaben. Logs zeigen zahlreiche Timeout- und Datenbank-Verbindungsfehler.
    CI/CD-Pipeline lief durch, aber nach dem Rollout häufen sich Exceptions in den Microservices Auth und Orders.
    Bitte sofortige Analyse durch das Software-Entwicklungsteam, Hotfix und ggf. Rollback. Hohe Kunden- und Umsatz-Auswirkung.
    """).strip()

    ticket_id = await otobo_helper.create_ticket(
        subject=f"E2E DE Classify {uuid4()}",
        body=german_text,
    )
    base_config_builder.add_service(
        "hf_local",
        "hf-local:HFClassificationService",
        params={"api_token": os.getenv("E2E_HF_TOKEN")},
    )
    expected_queue = "IT & Technology/Software Development"
    expected_priority = "critical"

    classify_queue = (
        PipeConfigBuilder()
        .set_injects({"classification_service": "hf_local"})
        .set_id("classify-queue")
        .set_use("base:ClassificationPipe")
        .set_params(
            {
                "text": german_text,
                "model_name": "softoft/otai-queue-de-bert-v1",
            }
        )
        .build()
    )

    classify_priority = (
        PipeConfigBuilder()
        .set_injects({"classification_service": "hf_local"})
        .set_id("classify-priority")
        .set_use("base:ClassificationPipe")
        .set_params(
            {
                "text": german_text,
                "model_name": "softoft/otai-priority-de-bert-v1",
            }
        )
        .build()
    )

    apply_classifications = (
        PipeConfigBuilder()
        .set_injects({"ticket_system": "otobo_znuny"})
        .set_id("apply-classifications")
        .set_use("base:UpdateTicketPipe")
        .set_params(
            {
                "ticket_id": ticket_id,
                "updated_ticket": {
                    "queue": {"name": "{{ get_pipe_result('classify-queue', 'label') }}"},
                    "priority": {"name": "{{ get_pipe_result('classify-priority', 'label') }}"},
                },
            }
        )
        .build()
    )

    composite = (
        pipe_factory.create_composite_builder("de-classify-queue-priority-and-update")
        .add_step(classify_queue)
        .add_step(classify_priority)
        .add_step(apply_classifications)
        .build()
    )

    runner = pipe_factory.create_simple_sequential_runner(
        runner_id="runner-de-classify",
        on=pipe_factory.create_interval_trigger(interval=otobo_e2e_config.environment.polling_interval),
        run=composite,
    )

    config = base_config_builder.add_orchestrator_pipe(runner).build()
    docker_compose_controller.write_config(config)
    docker_compose_controller.down()
    time.sleep(2)
    await asyncio.sleep(2)
    docker_compose_controller.up()

    async def ticket_updated() -> bool:
        ticket = await otobo_helper.get_ticket(ticket_id)
        print(ticket)
        q_ok = ticket.queue.name not in ["~Test-Queue1", "~Test-Queue2"]
        p_ok = ticket.priority.name != "low"
        return q_ok and p_ok

    await wait_for_condition(ticket_updated, timeout=240.0)
    save_example(config, meta=_CONFIG_META_INFO)
