---
title: Open Ticket AI 1.4 Release - The First Major Production Release
description: "Discover Open Ticket AI 1.4, the first production-ready release featuring powerful"
toast_message: "New Release: Open Ticket AI 1.4 — Explore the production-ready platform"
image: "https://softoft.sirv.com/open-ticket-ai/Open-Ticket-AI-Release-Version-1.png"
show-on-news: true
date: 2025-10-28
---

# Open Ticket AI 1.4: The First Major Production Release

Open Ticket AI 1.4 is here, marking the **first major production-ready release**! This version
brings enterprise-grade features, a mature plugin ecosystem, and the flexibility to automate your
ticket system workflows like never before. Get the full release
on [GitHub](https://github.com/Softoft-Orga/open-ticket-ai/releases/tag/v1.4.1).

![https://softoft.sirv.com/open-ticket-ai/Open-Ticket-AI-Release-Version-1.png](https://softoft.sirv.com/open-ticket-ai/Open-Ticket-AI-Release-Version-1.png)

## Checkout the Demo!

This Demo shows the OTOBO Ticketsystem with OTAI setup to classify queue and priority based on the
ticket content. You can login with the following link!

::: warning German Models!
The Queue and Priority model only work for German tickets as it was trained with German data.
:::

[OTOBO Queue Priority Demo](https://otobo-demo.open-ticket-ai.com/otobo/customer.pl?Action=Login;User=otai;Password=otai)

Example!

Subject: "DRINGEND! Wohnung in Mainzer Straße 8 Heizung kaputt;"
Text: "Hallo,
meine Heizung in der Wohnung in der Mainzer Straße 8 funktioniert nicht. Bitte um schnelle Hilfe!
dringend!
Die Heizungsrohre sind kalt und es ist sehr kalt in der Wohnung. Vielen Dank!
Mit freundlichen Grüßen,
Max Mustermann
"

[Queue Priority - Test Ticket](https://otobo-demo.open-ticket-ai.com/otobo/customer.pl?Action=CustomerTicketMessage;Subject=DRINGEND!%20Wohnung%20in%20Mainzer%20Stra%C3%9Fe%208%20Heizung%20kaputt;Body=Hallo,%20meine%20Heizung%20in%20der%20Wohnung%20in%20der%20Mainzer%20Stra%C3%9Fe%208%20funktioniert%20nicht.%20Bitte%20um%20schnelle%20Hilfe!%20dringend!%20Die%20Heizungsrohre%20sind%20kalt%20und%20es%20ist%20sehr%20kalt%20in%20der%20Wohnung.%20Vielen%20Dank!%20Mit%20freundlichen%20Gr%C3%BC%C3%9Fen,%20Max%20Mustermann)

These are just test models. You can use any model you want with Open Ticket AI!
It works with Huggingface Models

interesting models:
OpenAlex/bert-base-multilingual-cased-finetuned-openalex-topic-classification-title-abstract
oliverguhr/german-sentiment-bert
siebert/sentiment-roberta-large-english
distilbert/distilbert-base-uncased-finetuned-sst-2-english

Often it is better to train your own models with your own data.
Then you need to publish this to huggingface_hub change the model and HF_TOKEN in the config.yml and
restart OTAI.

## What Open Ticket AI 1.4 Offers

### Powerful Plugin Architecture

Install only the capabilities you need through a **modular plugin system**. Plugins extend Open
Ticket AI with custom ticket system integrations, ML models, and processing logic—all without
touching core code.

- **OTOBO/Znuny Plugin** (`otai-otobo-znuny`): Connect to OTOBO, Znuny, and OTRS ticket systems
- **HuggingFace Local Plugin** (`otai-hf-local`): Run ML classification models on your own
  infrastructure

**How it works:** Plugins are standard Python packages discovered via entry points. Install with
`uv add otai-otobo-znuny`, reference in your config, and you're ready. Learn more in
the [Plugin System](../users/plugins.md) documentation.

### Flexible Pipeline System

Build sophisticated automation workflows with **sequential pipe execution**:

- **Simple Pipes**: Fetch tickets, classify content, update fields, add notes
- **Expression Pipes**: Dynamic conditional logic with Jinja2 templates
- **Composite Pipes**: Nest pipelines for multi-stage orchestration

Each pipe receives context from previous steps, executes its task, and passes results forward. Read
the complete guide in [Pipe System](../users/pipeline.md).

### Dynamic Configuration with Template Rendering

Configure everything using **YAML + Jinja2** for maximum flexibility:

<div v-pre>

- Reference environment variables: `{{ get_env('API_KEY') }}`
- Access pipe results: `{{ get_pipe_result('fetch', 'tickets') }}`
- Conditional parameters based on runtime state
- Type-safe configuration schemas

</div>

Services are defined once and reused across multiple pipes via dependency injection.
Explore [Configuration & Template Rendering](../users/config_rendering.md) for details.

### Easy Installation

The easiest way to setup Open Ticket AI on your server is using **Docker Compose**:

**1. Create `compose.yml`:**

```yaml
services:
    open-ticket-ai:
        image: openticketai/engine:latest
        restart: "unless-stopped"
        environment:
            OTAI_TS_PASSWORD: "${OTAI_TS_PASSWORD}"
        volumes:
            - ./config.yml:/app/config.yml:ro
```

**2. Create your `config.yml`** (see [Configuration Guide](../users/config_rendering.md))

**3. Start the service:**

```bash
docker compose up -d
```

**4. You also need to setup the Ticketsystem**

#### Alternative: Install with pip/uv

For local development or custom deployments:

::: code-group

```bash [uv (Recommended)]
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Open Ticket AI with all plugins
uv pip install open-ticket-ai[all]

# Or install plugins individually
uv pip install open-ticket-ai
uv pip install otai-otobo-znuny otai-hf-local
```

```bash [pip]
# Install Open Ticket AI with all plugins
pip install open-ticket-ai[all]

# Or install plugins individually
pip install open-ticket-ai
pip install otai-otobo-znuny otai-hf-local
```

:::

See the full [Installation Guide](../guides/installation.md) for system requirements and deployment
options.

---

## For Plugin Developers: Build and Monetize

Open Ticket AI 1.4 empowers developers to **create and sell commercial plugins** with complete
licensing freedom. There's no marketplace yet, but the foundation is ready.

### Plugin Development Freedom

- **No licensing restrictions**: Choose your own license model
- **Sell commercial plugins**: Monetize your extensions however you like
- **Full documentation**: Complete guide
  at [Plugin Development](../developers/plugin_development.md)
- **Community visibility**: Your plugin can be listed on our [Plugins](../users/plugins.md) page

### Future Marketplace

While there's no official marketplace today, we're building toward one:

- **Plugin listings**: Already available on the documentation site
- **Discovery page**: Coming soon with search, categories, and ratings
- **Community showcase**: Highlight popular and trending plugins

Start building now, and your plugin will be ready when the marketplace launches!

---

## Technical Highlights

- **Python 3.14**: Modern type hints, performance improvements
- **Dependency Injection**: Clean architecture with Injector framework
- **Entry Point Discovery**: Standard Python packaging for plugin loading
- **API Compatibility Validation**: Plugins and core versions checked at runtime
- **Comprehensive Testing**: Full test coverage with pytest

---

Open Ticket AI 1.4 is production-ready, extensible, and built for the future. Install it today,
automate your workflows, and join the growing plugin ecosystem!

