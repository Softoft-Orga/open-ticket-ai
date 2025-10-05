---
description: Learn how to install and configure the Hugging Face inference pipe and the OTOBO/Znuny/OTRS adapter that ship with Open Ticket AI.
---

# Available Plugins

Open Ticket AI ships with a small but growing plugin catalog. This page summarises the two plugins that are available
and explains how to enable them in your configuration.

| Plugin                                          | Purpose                                                                                                                     | Where it runs                                      | Installation |
|-------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|--------------|
| **Hugging Face Local Text Classification Pipe** | Runs a Hugging Face Transformers pipeline to predict queue, priority, or any custom label inside your automation pipelines. | Inside the Open Ticket AI worker container.        | Included with Open Ticket AI |
| **OTOBO/Znuny/OTRS Ticket System Service**      | Connects Open Ticket AI to your helpdesk via the official OTOBO REST API (compatible with Znuny & legacy OTRS).             | Against your on-premise OTOBO/Znuny/OTRS instance. | Separate package: `pip install open-ticket-ai-otobo-znuny-plugin` or via CLI: `otai plugin install open-ticket-ai-otobo-znuny-plugin` |

## Plugin Management via CLI

Open Ticket AI provides a command-line interface for managing plugins:

```bash
# List installed plugins
otai plugin list

# Install a plugin
otai plugin install open-ticket-ai-otobo-znuny-plugin

# Remove a plugin
otai plugin remove open-ticket-ai-otobo-znuny-plugin
```

For more details, see the [CLI Usage Guide](../../../../docs/CLI_USAGE.md).

## Before you begin

1. Decide where you manage your runtime configuration. The default config lives at `src/config.yml` and already contains
   reference definitions for both plugins.
2. Make sure your environment variables are set before starting Open Ticket AI—secrets such as API tokens are injected
   through Jinja expressions in the config file.

---

## Hugging Face Local Text Classification Pipe

This pipe lets you execute any Hugging Face sequence-classification model locally. When the pipe runs it loads the
tokenizer and model, builds a `text-classification` pipeline, and returns the top label together with its confidence
score.

### Installation & dependencies

The Hugging Face local text classification plugin is now available as a standalone PyPI package. Install it with:

```bash
pip install open-ticket-ai-hf-local
```

This will automatically install the required dependencies including `transformers[torch]` and `open-ticket-ai` core.

If your model is private you must supply a Hugging Face token.

### Configure the pipe

Declare the pipe class in your configuration and inject it into your pipeline. The plugin is now referenced by its
standalone package name:

```yaml
open_ticket_ai:
  general_config:
    pipe_classes:
      - &ticket_classifier_pipe
        use: "open_ticket_ai_hf_local:HFLocalTextClassificationPipe"
  defs:
    - &ticket_classifier
      <<: *ticket_classifier_pipe
      token: "{{ env.OTAI_HUGGINGFACE_TOKEN }}"
      prompt: "{{ data.ticket.subject }} {{ data.ticket.body }}"
```

**Note:** The import path has changed from `open_ticket_ai.open_ticket_ai_hf_local` to just `open_ticket_ai_hf_local` 
since it's now a standalone package.

### Runtime parameters

When you reference the pipe inside a workflow you provide the model name (for example, `softoft/EHS_Queue_V8`) and 
configure how it processes your ticket data.

**Required parameters:**
- `model` (str): The Hugging Face model identifier (e.g., `"softoft/EHS_Queue_V8"`)
- `prompt` (str): Text to classify, typically constructed from ticket fields using Jinja2 templates

**Optional parameters:**
- `token` (str): Hugging Face API token for private models

Example configuration with queue classification:

```yaml
- id: classify_queue
  use: "open_ticket_ai_hf_local:HFLocalTextClassificationPipe"
  model: "softoft/EHS_Queue_V8"
  token: "{{ env.OTAI_HUGGINGFACE_TOKEN }}"
  prompt: "{{ data.ticket.subject }} {{ data.ticket.body }}"
```

### Usage tips

* **Cache behaviour:** Models are cached per `(model, token)` combination, so repeated runs avoid reloading the weights 
  when the worker stays warm.
* **Secret management:** Keep your Hugging Face token in the `OTAI_HUGGINGFACE_TOKEN` environment variable or omit the 
  `token` field if the model is public.
* **Prompt control:** The `prompt` parameter can be any string—use Jinja templates to concatenate ticket subject, body, 
  or other context fields.
* **Package updates:** Install updates with `pip install --upgrade open-ticket-ai-hf-local`

For more details, see the [package repository](https://github.com/Softoft-Orga/open-ticket-ai/tree/main/src/open_ticket_ai_hf_local) 
and [PyPI page](https://pypi.org/project/open-ticket-ai-hf-local/).

---

## OTOBO / Znuny / OTRS Ticket System Service

This adapter exposes a unified ticket-system interface that Open Ticket AI pipelines can call to fetch, update, or
annotate tickets. Internally it wraps the asynchronous `otobo_znuny` client library and converts between native ticket
objects and the platform-agnostic models used by the automation engine.【F:
src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service.py†L1-L79】

### Installation & prerequisites

1. Install the OTOBO/Znuny plugin package:
   ```bash
   pip install open-ticket-ai-otobo-znuny-plugin
   ```
   
   Or install Open Ticket AI with the OTOBO/Znuny extra:
   ```bash
   pip install open-ticket-ai[otobo-znuny]
   ```

2. In OTOBO/Znuny/OTRS create a dedicated API web service and an agent with permissions to search, read, update tickets,
   and add articles.
3. Note the base URL of your GenericInterface endpoint, the web service name, and the credential you just created.

### Quick Setup via CLI

The plugin provides an interactive CLI setup command to help you configure your OTOBO/Znuny connection:

```bash
otai otobo-znuny setup
```

This command will:
- Prompt you for your OTOBO/Znuny instance details (base URL, web service name, credentials)
- Optionally verify the connection
- Generate a configuration file for Open Ticket AI

You can also provide all options via command-line flags:

```bash
otai otobo-znuny setup \
  --base-url "https://your-otobo.com/otrs" \
  --webservice-name "OpenTicketAI" \
  --username "open_ticket_ai" \
  --password "your-password" \
  --verify-connection \
  --output-config config.yml
```

**Note:** For security, it's recommended to use environment variables for passwords rather than command-line flags.

### Configure the ticket system

The default config file registers the adapter as `otobo_znuny` and sources secrets from environment variables:

```yaml
open_ticket_ai:
  defs:
    - id: "otobo_znuny"
      use: "open_ticket_ai.open_ticket_ai_otobo_znuny_plugin:OToboZnunyTicketSystemService"
      server_address: "{{ env.OTAI_OTOBO_ZNUNY_SERVER_ADDRESS }}"
      password: "{{ env.OTAI_OTOBO_ZNUNY_PASSWORD }}"
```

【F:src/config.yml†L22-L30】

Behind the scenes the rendered configuration wraps the password as a secret, constructs the correct operation URLs (
search, get, update), and turns your credentials into the `BasicAuth` structure that the client expects.【F:
src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service_config.py†L1-L46】

### Runtime behaviour

* **Initialisation:** when Open Ticket AI starts it instantiates the client, logs in against the GenericInterface, and
  keeps the session ready for subsequent requests.【F:
  src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service.py†L29-L45】
* **Fetching tickets:** search criteria such as queue and limit are translated to the OTOBO search payload and returned
  as unified tickets that downstream pipes can consume.【F:
  src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service.py†L47-L66】
* **Updating & notes:** updates build a `TicketUpdate` request and can optionally append a new article, enabling both
  field changes and audit notes in one step.【F:
  src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service.py†L68-L79】

### Suggested checks

After wiring the adapter into your automation pipeline:

1. Run the orchestrator in dry-run or a staging queue to confirm tickets are fetched correctly.
2. Monitor the helpdesk’s web-service logs—failed logins indicate incorrect credentials or GenericInterface permissions.
3. Trigger a test ticket and verify that queue/priority updates and audit notes appear as expected.

---

## Next steps

* Combine both plugins in a single workflow: fetch tickets from OTOBO, classify them with Hugging Face, then push
  updates back.
* Add your own pipe definitions or adapters by following the patterns above and registering them via `pipe_classes` or
  `defs`.
