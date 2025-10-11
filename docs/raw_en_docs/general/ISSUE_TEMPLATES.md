# Issue Templates

Open Ticket AI provides structured issue templates to help contributors report bugs, request features, and suggest improvements effectively.

## Available Templates

When creating a new issue on GitHub, you can choose from the following templates:

### 🐛 Bug Report
**Use this template when:** You encounter unexpected behavior, errors, or crashes.

**What to include:**
- Clear description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- Logs/error messages (optional)
- Additional context like version, environment (optional)

**Labels:** `bug`, `needs-triage`

---

### 📚 Documentation Request
**Use this template when:** You need clarification, improvements, or additions to documentation.

**What to include:**
- What's currently documented or missing
- What should be added, changed, or clarified
- Additional context like affected files, examples (optional)

**Labels:** `documentation`, `needs-triage`

---

### ⚙️ Configuration Issue
**Use this template when:** You have problems with YAML configuration, Jinja2 templates, or dependency injection.

**What to include:**
- Description of the configuration problem
- Configuration snippet showing the issue
- Expected vs. actual behavior
- Additional context like error messages, version (optional)

**Labels:** `configuration`, `needs-triage`

---

### 🔧 Pipe or Plugin Request
**Use this template when:** You want to propose a new pipe, plugin, or extension to the pipeline system.

**What to include:**
- Description of what the pipe/plugin should do
- Use case and workflow integration
- Configuration example in YAML
- Additional context like proposed name, I/O specs, dependencies (optional)

**Labels:** `enhancement`, `pipe-request`, `needs-triage`

---

### ✨ Feature Request (General)
**Use this template when:** You have a general feature request not related to a specific pipe or plugin.

**What to include:**
- Feature description
- Use case
- Proposed solution (optional)
- Additional context like alternatives, config examples (optional)

**Labels:** `enhancement`, `needs-triage`

---

### 🔄 CI/CD Issue
**Use this template when:** You want to propose changes to CI/CD workflows, build processes, deployments, or automation.

**What to include:**
- Type of CI/CD change
- Affected files or workflows
- Description of the change
- Motivation and context
- Additional details like risk level, testing plan, rollback plan (optional)

**Labels:** `ci-cd`, `needs-triage`

---

## Template Design Principles

All templates are designed to:

1. **Align with Architecture** - Reference Open Ticket AI's pipeline & plugin architecture
2. **Minimize Required Fields** - Only essential fields are required to reduce friction
3. **Provide Examples** - Include helpful placeholders and sample YAML configs
4. **Auto-apply Labels** - Ensure proper triage with automatic labeling
5. **Guide Contributors** - Help users provide necessary information without overwhelming them

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
4. **Fill in required fields:** Only a few essential fields are required; provide optional details as needed
5. **Submit:** Your issue will be automatically labeled and triaged

---

## For Maintainers

Templates are streamlined to reduce friction while still collecting essential information. Contributors can provide additional details in the optional fields when relevant. This approach:
- Makes issue submission faster and less intimidating
- Reduces incomplete submissions due to form fatigue
- Still captures all critical information needed for triage
- Allows contributors to add context as needed without mandatory fields

---

## Need Help?

If you're unsure which template to use or need help:
- Check the [Community Discussions](https://github.com/Softoft-Orga/open-ticket-ai/discussions)
- Visit the [Q&A section](https://github.com/Softoft-Orga/open-ticket-ai/discussions/categories/q-a)
- Browse the [documentation](https://open-ticket-ai.com)
