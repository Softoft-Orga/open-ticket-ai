# OTAI Runtime — Documentation

OTAI Runtime is the **on-prem inference engine**: a Python package that
runs categorical-model inference next to a customer's ticket system,
without sending production ticket payloads to the cloud. It consumes
models trained by [OTAI Studio](../../otai-studio/docs/index.md) and is
embedded by [OTAI Desk](../../otai-desk/docs/index.md) and partner
deployments.

This is the entry point to everything Runtime-specific. For monorepo-wide
context start at the root [`DOCS.md`](../../DOCS.md).

## Start here

- Package overview and quickstart: [`open-ticket-ai-runtime/README.md`](../README.md).
- The customer-facing site (Astro + Vue) lives in this project's
  `/docs` directory at the **website** level (under `docs/src/...`),
  not under this `docs/` documentation folder. See the project
  [`AGENTS.md`](../AGENTS.md) for the website-vs-docs convention used
  here.

## Hard rules (Runtime)

- Python **3.14** only; modern typing (PEP 695); no docstrings or code
  comments — documentation lives in Markdown.
- All tests under `tests/` (`unit/`, `integration/`, `e2e/`); never under
  `src/**/tests/`.
- Pydantic v2 for data models; explicit type annotations everywhere.
- Prefer composition and dependency injection (Injector) over
  inheritance; no monkey patching.
- Preserve the **runtime never calls Firebase** boundary — Runtime is
  on-prem and talks to ticket systems via the
  [OTOBO/Znuny client](../../otobo-znuny-python-client/docs/index.md) and
  the Zammad connector in this repo.

## Related project docs

- [OTAI Studio docs](../../otai-studio/docs/index.md) — cloud control
  plane that trains Runtime's models.
- [OTAI Desk docs](../../otai-desk/docs/index.md) — ticketing product
  built on top of Runtime.
- [OTOBO/Znuny client docs](../../otobo-znuny-python-client/docs/index.md)
  — connector library Runtime depends on.
- [Prototype runbook](../../otai-studio/docs/architecture/prototype_runbook.md)
  — MVP scope spanning Runtime + Studio + OTOBO.
