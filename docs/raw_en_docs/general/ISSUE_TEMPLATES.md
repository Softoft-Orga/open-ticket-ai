# Issue Templates

Open Ticket AI provides structured issue templates to help contributors report bugs, request features, and suggest improvements effectively.

## Available Templates

When creating a new issue on GitHub, you can choose from the following templates:

### 🐛 Bug Report
**Use this template when:** You encounter unexpected behavior, errors, or crashes.

**What to include:**
- Which component is affected (Core, Pipes, Plugins, CLI, etc.)
- Steps to reproduce the issue
- Expected vs. actual behavior
- Relevant configuration file sections (YAML)
- Error logs and stack traces
- Version information (Open Ticket AI, Python)

**Labels:** `bug`, `needs-triage`

---

### 📚 Documentation Request
**Use this template when:** You need clarification, improvements, or additions to documentation.

**What to include:**
- Type of documentation (User Guide, Config Examples, API Reference, etc.)
- Current state and what's missing
- Proposed improvements
- Which component/area it relates to
- Example content or code snippets (optional)

**Labels:** `documentation`, `needs-triage`

---

### ⚙️ Configuration Issue
**Use this template when:** You have problems with YAML configuration, Jinja2 templates, or dependency injection.

**What to include:**
- Configuration area (YAML structure, Jinja2, DI, Orchestrator, etc.)
- Configuration snippet showing the problem
- Expected vs. actual behavior
- Error messages
- Whether `otai check-config` passes or fails
- Any workarounds you've found

**Labels:** `configuration`, `needs-triage`

---

### 🔧 Pipe or Plugin Request
**Use this template when:** You want to propose a new pipe, plugin, or extension to the pipeline system.

**What to include:**
- Type of request (Base Pipe, Plugin, Extension, etc.)
- Proposed name and description
- Use case and workflow integration
- Configuration example in YAML
- Input/output specifications
- External dependencies (if any)
- Whether you can contribute to implementation

**Labels:** `enhancement`, `pipe-request`, `needs-triage`

---

### ✨ Feature Request (General)
**Use this template when:** You have a general feature request not related to a specific pipe or plugin.

**What to include:**
- Feature area (Core, Config System, CLI, Orchestrator, etc.)
- Description and use case
- Current limitations
- Proposed solution
- Alternatives considered
- Whether it would be a breaking change
- Configuration example (if applicable)

**Labels:** `enhancement`, `needs-triage`

---

## Template Design Principles

All templates are designed to:

1. **Align with Architecture** - Reference Open Ticket AI's pipeline & plugin architecture
2. **Include Structured Fields** - Use dropdowns, checkboxes, and formatted code blocks
3. **Provide Examples** - Include helpful placeholders and sample YAML configs
4. **Auto-apply Labels** - Ensure proper triage with automatic labeling
5. **Guide Contributors** - Help users provide all necessary information upfront

---

## Architecture References in Templates

The templates are tailored to Open Ticket AI's specific architecture:

### Pipeline Components
- Core Pipeline/Orchestrator
- Base Pipes (FetchTickets, UpdateTicket, AddNote, etc.)
- Composite Pipes and custom implementations
- Pipe configuration fields (`id`, `use`, `injects`, `steps`, `if`, `depends_on`)

### Configuration System
- YAML structure under `open_ticket_ai` root key
- Sections: `plugins`, `general_config`, `defs`, `orchestrator`
- Template rendering with Jinja2
- Dependency injection with `injects`
- Environment variables

### Plugins
- Plugin architecture and discovery
- HuggingFace Local plugin
- OTOBO/Znuny Integration plugin
- Custom plugin development

### Tools & Validation
- CLI tool commands (`otai check-config`, `otai start`, etc.)
- Configuration validation
- Testing requirements (unit, integration, contract tests)

---

## Using the Templates

1. **Navigate to Issues:** Go to the [GitHub Issues page](https://github.com/Softoft-Orga/open-ticket-ai/issues)
2. **Click "New issue":** You'll see all available templates
3. **Choose the right template:** Select the one that best fits your situation
4. **Fill in all required fields:** The template will guide you through what to include
5. **Submit:** Your issue will be automatically labeled and triaged

---

## For Maintainers

Each template includes an implementation/resolution checklist to track:
- Investigation and reproduction (for bugs)
- Code implementation
- Testing (unit, integration)
- Documentation updates
- CHANGELOG entries
- Schema regeneration (if config changes)

---

## Need Help?

If you're unsure which template to use or need help:
- Check the [Community Discussions](https://github.com/Softoft-Orga/open-ticket-ai/discussions)
- Visit the [Q&A section](https://github.com/Softoft-Orga/open-ticket-ai/discussions/categories/q-a)
- Browse the [documentation](https://open-ticket-ai.com)
