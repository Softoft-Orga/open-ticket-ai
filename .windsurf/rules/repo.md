---
trigger: glob
description: High-level guidance for anyone working in the Open Ticket AI repository.
globs: ["**/*"]
---

# Repository Overview

- **Purpose:** Automation components that enhance open-source ticket systems (primarily OTOBO/Znuny) with AI-driven
  workflows.
- **Source layout:**
    - Application code lives in `src/open_ticket_ai/` organised by domain (e.g. `core/`, `base/`, `hf_local/`).
    - Configuration schemas and examples reside in `src/open_ticket_ai/core/config/` and `docs/config_examples/`.
    - Tests live in `tests/` and `classification_api_tests/`.
- **Tooling:**
    - Use [`uv`](https://github.com/astral-sh/uv) for dependency management and commands (see `uv.lock`).
    - Python formatting/linting via Ruff; typing enforced by MyPy (strict) with the `pydantic.mypy` plugin.
    - Run `uv run pytest` for the test suite; async tests rely on `pytest-asyncio`.
- **Key configs:**
    - Project metadata and tool configuration are centralised in `pyproject.toml`.
    - Runtime configuration is loaded from YAML (`src/config.yml` by default) and validated with Pydantic models.
- **AI integrations:**
    - Hugging Face transformers (with optional local pipelines) live under `src/open_ticket_ai/hf_local`.
    - Ticket system integrations for OTOBO/Znuny sit in `src/open_ticket_ai/otobo_znuny_plugin`.
- **Documentation:**
    - Developer notes and diagrams are in `docs/`; VitePress docs under `docs/vitepress_docs`.
- **When in doubt:** align new code with existing module boundaries, keep configuration-driven behaviour, and update
  docs/tests alongside code changes.
