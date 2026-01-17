# noinspection PyUnresolvedReferences
app = (
    App(api_version=">=1.0.0")
    .infrastructure(
        Logging()
        .level("INFO")
        .log_to_file(False)
        .log_file_path(None)
        .log_format("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        .date_format("%Y-%m-%d %H:%M:%S")
    )
    .services(
        Services()
        .add("jinja_default", Service("base:JinjaRenderer"))
        .add(
            "otobo_znuny",
            Service("otobo-znuny:OTOBOZnunyTicketSystemService").with_params(
                base_url="http://52.57.217.182/otobo/nph-genericinterface.pl",
                password=Env("OTAI_OTOBO_DEMO_PASSWORD"),
            ),
        )
        .add("hf_local", Service("hf-local:HFClassificationService"))
    )
    .orchestrator(
        Orchestrator.simple()
        .sleep("PT0.01S")
        .steps(
            Runner.sequential("ticket-routing-runner")
            .on(Trigger.interval("trigger_interval").every("PT0.5S"))
            .run(
                Pipe.composite("ticket-routing")
                .then(
                    Pipe.fetch_tickets("ticket_fetcher")
                    .inject(ticket_system="otobo_znuny")
                    .criteria(queue={"name": "OpenTicketAI::Incoming"}, limit=1)
                )
                .then(
                    Pipe.expect("fail_no_tickets")
                    .that(Result("ticket_fetcher", "fetched_tickets").length().gt(0))
                    .otherwise_fail("No tickets")
                )
                .then(Pipe.let("ticket").value(Result("ticket_fetcher", "fetched_tickets").at(0)))
                .then(
                    Pipe.classify("queue_classify")
                    .inject(classification_service="hf_local")
                    .use_model("softoft/otai-queue-de-bert-v1")
                    .on_text(
                        Text.concat(
                            Result("ticket").at("subject"),
                            " ",
                            Result("ticket").at("body"),
                        )
                    )
                )
                .then(
                    Pipe.select("queue_select_final")
                    .from_classification("queue_classify")
                    .with_confidence_check()
                    .lower(0.8)
                    .set("OpenTicketAI::Unclassified")
                )
                .then(
                    Pipe.update_ticket("queue_update_ticket")
                    .inject(ticket_system="otobo_znuny")
                    .ticket_id(Result("ticket").at("id"))
                    .set_queue(Result("queue_select_final"))
                )
                .then(
                    Pipe.add_note("queue_add_note")
                    .inject(ticket_system="otobo_znuny")
                    .ticket_id(Result("ticket").at("id"))
                    .note(
                        subject="Automatische Queue-Klassifizierung",
                        body=Text.f("Das Ticket wurde der Queue {q} zugeordnet (Konfidenz: {c}).").fmt(
                            q=Result("queue_select_final"),
                            c=Result("queue_classify", "confidence").round(2),
                        ),
                    )
                )
                .then(
                    Pipe.classify("priority_classify")
                    .inject(classification_service="hf_local")
                    .use_model("softoft/otai-priority-de-bert-v1")
                    .on_text(
                        Text.concat(
                            Result("ticket").at("subject"),
                            " ",
                            Result("ticket").at("body"),
                        )
                    )
                )
                .then(
                    Pipe.select("priority_select_final")
                    .from_classification("priority_classify")
                    .with_confidence_check()
                    .lower(0.8)
                    .set("medium")
                )
                .then(
                    Pipe.update_ticket("priority_update_ticket")
                    .inject(ticket_system="otobo_znuny")
                    .ticket_id(Result("ticket").at("id"))
                    .set_priority(Result("priority_select_final"))
                )
                .then(
                    Pipe.add_note("priority_add_note")
                    .inject(ticket_system="otobo_znuny")
                    .ticket_id(Result("ticket").at("id"))
                    .note(
                        subject="Automatische Priorisierung",
                        body=Text.f("Das Ticket wurde der Priorität {p} zugeordnet (Konfidenz: {c}).").fmt(
                            p=Result("priority_select_final"),
                            c=Result("priority_classify", "confidence").round(2),
                        ),
                    )
                )
            )
        )
    )
)
