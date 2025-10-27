show-on-news: true
toast_message: New Release: Open Ticket AI 1.4.1 — Explore the production-ready platform
image: https://softoft.sirv.com/Images/open-ticket-ai/releases/1-4-hero.jpg
title: Open Ticket AI 1.4.1 Release - The First Major Production Release
description: Discover Open Ticket AI 1.4.1, the first production-ready release featuring powerful plugin architecture, flexible pipelines, dynamic configuration, and commercial plugin support.
date: 2025-10-27
authors:
  - Open Ticket AI Team
tags:
  - release
  - changelog
  - automation
  - production
---

# Open Ticket AI 1.4.X: The First Major Production Release

Open Ticket AI 1.4.X is here, marking the **first major production-ready release**! This version
brings enterprise-grade features, a mature plugin ecosystem, and the flexibility to automate your
ticket system workflows like never before. Get the full release
on [GitHub](https://github.com/Softoft-Orga/open-ticket-ai/releases/tag/v1.4.1).

## What Open Ticket AI 1.4.X Offers

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

- Reference environment variables: `{{ get_env('API_KEY') }}`
- Access pipe results: `{{ get_pipe_result('fetch', 'tickets') }}`
- Conditional parameters based on runtime state
- Type-safe configuration schemas

Services are defined once and reused across multiple pipes via dependency injection.
Explore [Configuration & Template Rendering](../users/config_rendering.md) for details.

### Easy Installation

Get started in minutes:

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Open Ticket AI
uv pip install open-ticket-ai

# Add plugins as needed
uv add otai-otobo-znuny otai-hf-local
```

See the full [Installation Guide](../guides/installation.md) for system requirements and deployment
options.

---

## For Plugin Developers: Build and Monetize

Open Ticket AI 1.4.1 empowers developers to **create and sell commercial plugins** with complete
licensing freedom. There's no marketplace yet, but the foundation is ready.

### Plugin Development Freedom

- **No licensing restrictions**: Choose your own license model
- **Sell commercial plugins**: Monetize your extensions however you like
- **Full documentation**: Complete guide
  at [Plugin Development](../developers/plugin_development.md)
- **Community visibility**: Your plugin can be listed on our [Plugins](../users/plugins.md) page

### Monetization Approaches

#### Private PyPI + License Keys

Host your plugin on a private PyPI server (DevPI, Gemfury, AWS CodeArtifact) with authentication
tokens. Add license validation in your plugin's `__init__` method:

```python
import os
from open_ticket_ai.core.plugins.plugin import Plugin


class CommercialPlugin(Plugin):
    def __init__(self, config):
        license_key = os.getenv('MY_PLUGIN_LICENSE_KEY')
        if not license_key or not self._validate_license(license_key):
            raise LicenseError("Valid license key required")
        super().__init__(config)

    def _validate_license(self, key: str) -> bool:
        # Your validation logic
        pass
```

#### Public PyPI + License Enforcement

Publish freely to PyPI but enforce runtime licensing:

```python
class PublicCommercialPlugin(Plugin):
    def _get_all_injectables(self):
        license_key = os.getenv('MY_PLUGIN_LICENSE_KEY')
        if not license_key or not self._verify_license(license_key):
            raise LicenseError(
                "This plugin requires a valid license. "
                "Visit https://myplugin.com for licensing."
            )
        return [MyPipe, MyService]
```

Installation remains open, but usage requires purchasing a license key.

### Future Marketplace

While there's no official marketplace today, we're building toward one:

- **Plugin listings**: Already available on the documentation site
- **Discovery page**: Coming soon with search, categories, and ratings
- **Community showcase**: Highlight popular and trending plugins

Start building now, and your plugin will be ready when the marketplace launches!

---

## Technical Highlights

- **Python 3.13**: Modern type hints, performance improvements
- **Dependency Injection**: Clean architecture with Injector framework
- **Entry Point Discovery**: Standard Python packaging for plugin loading
- **API Compatibility Validation**: Plugins and core versions checked at runtime
- **Comprehensive Testing**: Full test coverage with pytest

---

Open Ticket AI 1.4.1 is production-ready, extensible, and built for the future. Install it today,
automate your workflows, and join the growing plugin ecosystem!

