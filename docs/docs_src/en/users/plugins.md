---
description: Learn about Open Ticket AI's plugin system - what plugins are, how to install them, and which plugins are available for your automation workflows.
---

# Plugins

Plugins extend Open Ticket AI with additional capabilities. Each plugin provides services and pipes
that you can use in your configuration to connect to different ticket systems, run ML models, or add
custom processing logic.

## What is a Plugin?

A **plugin** is a Python package that adds new functionality to Open Ticket AI:

- **Services**: Connect to ticket systems (OTOBO, Znuny), ML models, or external APIs
- **Pipes**: Fetch tickets, classify content, update fields, add notes, or run custom logic
- **Ready to Use**: Just install, configure, and reference in your YAML

## How to Install Plugins

Install plugins using the `uv` package manager:

```bash
# Install a single plugin
uv add otai-otobo-znuny

# Install multiple plugins at once
uv add otai-otobo-znuny otai-hf-local
```

That's it! Once installed, the plugin's services and pipes are automatically available in your
configuration.

## How to Use Plugins in Configuration

Plugins provide services and pipes that you reference in your YAML configuration using the format
`plugin-name:ComponentName`.

### Example: Complete Workflow with Plugins

<InlineExample slug="basics-minimal" />

```yaml
# Define services from plugins
services:
  ticket_system:
    use: "otobo-znuny:OTOBOZnunyTicketSystemService"
    params:
      base_url: "{{ get_env('OTOBO_URL') }}"
      username: "{{ get_env('OTOBO_USER') }}"
      password: "{{ get_env('OTOBO_PASSWORD') }}"

  classifier:
    use: "hf-local:HuggingFaceLocalTextClassificationService"
    params:
      model_name: "distilbert-base-uncased-finetuned-sst-2-english"

# Use plugin pipes in your pipeline
orchestrator:
  runners:
    - run:
        id: fetch_tickets
        use: "base:FetchTicketsPipe"
        injects:
          ticket_system: "ticket_system"
        params:
          ticket_search_criteria:
            queue_name: "Support"
            state: "new"
            limit: 25

    - run:
        id: classify_tickets
        use: "hf-local:TextClassificationPipe"
        injects:
          classifier: "classifier"
        params:
          tickets: "{{ get_pipe_result('fetch_tickets', 'fetched_tickets') }}"

    - run:
        id: update_tickets
        use: "base:UpdateTicketPipe"
        injects:
          ticket_system: "ticket_system"
        params:
          ticket_id: "{{ ticket.id }}"
          queue: "{{ classification.label }}"
```

## Available Plugins

### Base Plugin

**Package**: `otai-base` (installed automatically with Open Ticket AI)

The Base plugin provides core functionality that works with any ticket system:

**Pipes:**

- `base:FetchTicketsPipe` - Fetch tickets from your ticket system
- `base:UpdateTicketPipe` - Update ticket fields (queue, priority, state, etc.)
- `base:AddNotePipe` - Add notes or comments to tickets
- `base:ExpressionPipe` - Evaluate dynamic expressions and conditional logic

**Example:**

```yaml
orchestrator:
  runners:
    - run:
        id: fetch_new_tickets
        use: "base:FetchTicketsPipe"
        injects:
          ticket_system: "my_ticket_system"
        params:
          ticket_search_criteria:
            state: "new"
            limit: 50
```

### OTOBO/Znuny Plugin

**Package**: `otai-otobo-znuny`

Connect to OTOBO, Znuny, and OTRS ticket systems.

**Installation:**

```bash
uv add otai-otobo-znuny
```

**What it provides:**

- Full integration with OTOBO, Znuny, and OTRS
- Ticket fetching, updating, and note management
- Queue, priority, and state management

**Example Configuration:**

```yaml
services:
  otobo:
    use: "otobo-znuny:OTOBOZnunyTicketSystemService"
    params:
      base_url: "https://helpdesk.example.com"
      username: "{{ get_env('OTOBO_USER') }}"
      password: "{{ get_env('OTOBO_PASSWORD') }}"

orchestrator:
  runners:
    - run:
        id: fetch
        use: "base:FetchTicketsPipe"
        injects:
          ticket_system: "otobo"
        params:
          ticket_search_criteria:
            queue_name: "IT Support"
            state: "new"
```

### HuggingFace Local Plugin

**Package**: `otai-hf-local`

Run machine learning classification models locally using HuggingFace transformers.

**Installation:**

```bash
uv add otai-hf-local
```

**What it provides:**

- Local ML model inference (no external API calls)
- Text classification for ticket content
- Support for any HuggingFace text classification model

**Example Configuration:**

```yaml
services:
  ml_classifier:
    use: "hf-local:HuggingFaceLocalTextClassificationService"
    params:
      model_name: "distilbert-base-uncased-finetuned-sst-2-english"
      # Or use your custom fine-tuned model
      # model_name: "my-org/custom-ticket-classifier"

orchestrator:
  runners:
    - run:
        id: classify
        use: "hf-local:TextClassificationPipe"
        injects:
          classifier: "ml_classifier"
        params:
          text: "{{ ticket.title }} {{ ticket.body }}"
```

## Benefits of the Plugin System

**Install Only What You Need:**

- Don't use OTOBO? Don't install the OTOBO plugin
- Running classification in the cloud? Skip the HuggingFace plugin
- Keeps your installation lightweight

**Mix and Match:**

- Use OTOBO plugin with HuggingFace models
- Combine multiple ticket systems in one setup
- Add community plugins as they become available

**Independent Updates:**

- Update plugins without updating core
- Get new features faster
- Roll back individual plugins if needed

## Plugin Naming Convention

When you use plugins in configuration, the format is:

```
plugin-name:ComponentName
```

**Examples:**

- `base:FetchTicketsPipe` - FetchTicketsPipe from the base plugin
- `otobo-znuny:OTOBOZnunyTicketSystemService` - Service from the otobo-znuny plugin
- `hf-local:TextClassificationPipe` - Pipe from the hf-local plugin

The plugin name is derived from the package name by removing `otai-` prefix.

## For Developers

Want to create your own plugin? Whether free or commercial, you have complete freedom!

See the [Plugin Development Guide](../developers/plugin_development.md) for:

- How to build custom plugins
- Publishing to PyPI
- Monetization strategies for commercial plugins
- Getting your plugin listed

## Related Documentation

- [Plugin Development](../developers/plugin_development.md)
- [Dependency Injection](../developers/dependency_injection.md)
- [Pipe System](pipeline.md)
- [Configuration](../details/_config_reference.md)
