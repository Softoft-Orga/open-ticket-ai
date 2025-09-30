---
description: Learn how to install and configure the Hugging Face inference pipe and the OTOBO/Znuny/OTRS adapter that ship with Open Ticket AI.
---
# Available Plugins

Open Ticket AI ships with a small but growing plugin catalog. This page summarises the two plugins that are available out of the box and explains how to enable them in your configuration.

| Plugin | Purpose | Where it runs |
| --- | --- | --- |
| **Hugging Face Local Text Classification Pipe** | Runs a Hugging Face Transformers pipeline to predict queue, priority, or any custom label inside your automation pipelines. | Inside the Open Ticket AI worker container. |
| **OTOBO/Znuny/OTRS Ticket System Service** | Connects Open Ticket AI to your helpdesk via the official OTOBO REST API (compatible with Znuny & legacy OTRS). | Against your on-premise OTOBO/Znuny/OTRS instance. |

## Before you begin

1. Decide where you manage your runtime configuration. The default config lives at `src/config.yml` and already contains reference definitions for both plugins.
2. Make sure your environment variables are set before starting Open Ticket AI—secrets such as API tokens are injected through Jinja expressions in the config file.

---

## Hugging Face Local Text Classification Pipe

This pipe lets you execute any Hugging Face sequence-classification model locally. When the pipe runs it loads the tokenizer and model, builds a `text-classification` pipeline, and returns the top label together with its confidence score.【F:src/open_ticket_ai/hf_local/hf_local_text_classification_pipe.py†L1-L47】

### Installation & dependencies

The dependency on `transformers[torch]` is already declared in `pyproject.toml`, so no additional package installation is needed once you install Open Ticket AI.【F:pyproject.toml†L17-L27】 If your model is private you must supply a Hugging Face token.

### Configure the pipe

The default configuration declares the pipe class and injects it into the reusable `classification_generic` pipeline step. Copy the relevant snippet if you are creating your own config:

```yaml
open_ticket_ai:
  general_config:
    pipe_classes:
      - &ticket_classifier_pipe
        use: "open_ticket_ai.hf_local:HFLocalTextClassificationPipe"
  defs:
    - &ticket_classifier
      <<: *ticket_classifier_pipe
      token: "{{ env.OTAI_HUGGINGFACE_EHS_TOKEN }}"
      prompt: "{{ data.ticket.subject }} {{ data.ticket.body }}"
```

【F:src/config.yml†L10-L41】

### Runtime parameters

When you reference the pipe inside a workflow you provide the model name (for example, `softoft/EHS_Queue_V8`) and a mapping that translates raw labels to your helpdesk queue or priority names. The example automation shipped with the repo shows the queue and priority classification steps using two different models but sharing the same Hugging Face pipe definition.【F:src/config.yml†L59-L126】

### Usage tips

* Cache behaviour: models are cached per `(model, token)` combination, so repeated runs avoid reloading the weights when the worker stays warm.【F:src/open_ticket_ai/hf_local/hf_local_text_classification_pipe.py†L20-L32】
* Secret management: keep your Hugging Face token in the `OTAI_HUGGINGFACE_EHS_TOKEN` environment variable or remove the `token` field if the model is public.
* Prompt control: the `prompt` parameter can be any string—use Jinja templates to concatenate ticket subject, body, or other context fields.

---

## OTOBO / Znuny / OTRS Ticket System Service

This adapter exposes a unified ticket-system interface that Open Ticket AI pipelines can call to fetch, update, or annotate tickets. Internally it wraps the asynchronous `otobo_znuny` client library and converts between native ticket objects and the platform-agnostic models used by the automation engine.【F:src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service.py†L1-L79】

### Installation & prerequisites

1. Install Open Ticket AI—`otobo_znuny` is included as a dependency, so no extra packages are required.
2. In OTOBO/Znuny/OTRS create a dedicated API web service and an agent with permissions to search, read, update tickets, and add articles.
3. Note the base URL of your GenericInterface endpoint, the web service name, and the credential you just created.

### Configure the ticket system

The default config file registers the adapter as `otobo_znuny` and sources secrets from environment variables:

```yaml
open_ticket_ai:
  defs:
    - id: "otobo_znuny"
      use: "open_ticket_ai.otobo_znuny_plugin:OToboZnunyTicketSystemService"
      server_address: "{{ env.OTAI_OTOBO_ZNUNY_SERVER_ADDRESS }}"
      password: "{{ env.OTAI_OTOBO_ZNUNY_PASSWORD }}"
```

【F:src/config.yml†L22-L30】

Behind the scenes the rendered configuration wraps the password as a secret, constructs the correct operation URLs (search, get, update), and turns your credentials into the `BasicAuth` structure that the client expects.【F:src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service_config.py†L1-L46】

### Runtime behaviour

* **Initialisation:** when Open Ticket AI starts it instantiates the client, logs in against the GenericInterface, and keeps the session ready for subsequent requests.【F:src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service.py†L29-L45】
* **Fetching tickets:** search criteria such as queue and limit are translated to the OTOBO search payload and returned as unified tickets that downstream pipes can consume.【F:src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service.py†L47-L66】
* **Updating & notes:** updates build a `TicketUpdate` request and can optionally append a new article, enabling both field changes and audit notes in one step.【F:src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service.py†L68-L79】

### Suggested checks

After wiring the adapter into your automation pipeline:

1. Run the orchestrator in dry-run or a staging queue to confirm tickets are fetched correctly.
2. Monitor the helpdesk’s web-service logs—failed logins indicate incorrect credentials or GenericInterface permissions.
3. Trigger a test ticket and verify that queue/priority updates and audit notes appear as expected.

---

## Next steps

* Combine both plugins in a single workflow: fetch tickets from OTOBO, classify them with Hugging Face, then push updates back.
* Add your own pipe definitions or adapters by following the patterns above and registering them via `pipe_classes` or `defs`.
