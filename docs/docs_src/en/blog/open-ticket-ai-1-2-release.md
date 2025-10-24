---
title: Open Ticket AI 1.2.0 Release Highlights
description: Discover what's new in Open Ticket AI 1.2.0, including the HuggingFace plugin, nested composite pipelines, improved adapters, and key fixes.
date: 2025-10-13
authors:
  - Open Ticket AI Team
tags:
  - release
  - changelog
  - automation
---

# Open Ticket AI 1.2.0: Smarter Pipelines and Stronger Integrations

Open Ticket AI 1.2.0 is now available! This minor release doubles down on pipeline flexibility, local inference, and platform readiness while addressing critical bugs and dependency updates. Grab the full changelog on [GitHub](https://github.com/Softoft-Orga/open-ticket-ai/releases/tag/v1.2.0) and dive into the highlights below.【F:docs/docs_src/en/concepts/versioning.md†L159-L179】

## Release Overview

Version 1.2.0 introduces a new HuggingFace plugin for local inference, deeper composite-pipeline nesting, refreshed adapters, and documentation that walks you from setup to production-ready plugins. The release stays backward compatible while deprecating older config shapes and naming conventions so you can prepare for future majors without surprises.【F:docs/docs_src/en/concepts/versioning.md†L159-L173】

## Added

### HuggingFace Local Inference Plugin

Run modern transformers inside your own infrastructure with the new HuggingFace plugin. Install it with `uv add otai-hf-local`, then register it in your configuration to route ticket classification through on-prem models.【F:docs/docs_src/en/concepts/versioning.md†L162-L164】【F:docs/docs_src/en/concepts/plugins.md†L83-L103】

### Nested Composite Pipelines

Composite pipes can now contain other composites, letting you orchestrate complex, multi-stage workflows without losing context. Child pipes inherit parent parameters through the nested `PipeContext`, so deep pipelines remain maintainable.【F:docs/docs_src/en/concepts/versioning.md†L162-L164】【F:docs/docs_src/en/concepts/pipeline.md†L314-L328】【F:docs/docs_src/en/concepts/pipeline.md†L431-L458】

## Changed

### Better Runtime Feedback

Pipeline executions emit clearer error messaging, helping you diagnose failures from configuration rendering through pipe execution without trawling logs.【F:docs/docs_src/en/concepts/versioning.md†L166-L167】【F:docs/docs_src/en/concepts/config_rendering.md†L12-L28】

### OTOBO Adapter Ready for v11

Teams running the latest OTOBO can upgrade confidently—the bundled adapter now speaks the v11 API while keeping Znuny/OTRS compatibility.【F:docs/docs_src/en/concepts/versioning.md†L166-L168】【F:docs/docs_src/en/concepts/plugins.md†L83-L98】

## Deprecated

### Legacy Configuration Shapes

Older, pre-1.2 configuration formats and pipe naming patterns continue to work for now, but they are formally deprecated. Move to the YAML structures documented in the configuration reference so migrations to 2.0 stay painless.【F:docs/docs_src/en/concepts/versioning.md†L170-L172】【F:docs/docs_src/en/details/config_reference.md†L60-L98】

## Fixed

### Template Rendering Memory Leak

The configuration lifecycle has been hardened so Jinja2 template rendering no longer leaks memory during long-running orchestrations.【F:docs/docs_src/en/concepts/versioning.md†L174-L176】【F:docs/docs_src/en/concepts/config_rendering.md†L12-L28】

### Accurate Time Windows

Interval triggers now respect timezone boundaries, eliminating off-by-one scheduling behavior in follow-the-sun deployments.【F:docs/docs_src/en/concepts/versioning.md†L174-L176】

## Security

### Dependency Refresh

Core and plugin dependencies were bumped to remediate CVE-2025-1234. Update to 1.2.0 (or later) to stay covered without extra patching.【F:docs/docs_src/en/concepts/versioning.md†L178-L179】

## Documentation Updates

- **New ML classification guide:** Walk through building and deploying a complete ticket-classification pipeline end-to-end.【F:docs/docs_src/en/concepts/versioning.md†L189-L190】【F:docs/docs_src/en/guides/first_pipeline.md†L1-L19】
- **Plugin development tutorial:** Learn how to scaffold, register, and package custom plugins with code examples and entry-point wiring.【F:docs/docs_src/en/concepts/versioning.md†L189-L192】【F:docs/docs_src/en/developers/plugin_development.md†L1-L55】
- **Expanded troubleshooting:** Installation guidance now includes actionable fixes for Python, permissions, and network hurdles.【F:docs/docs_src/en/concepts/versioning.md†L189-L192】【F:docs/docs_src/en/guides/installation.md†L320-L379】

Stay tuned for more automation features, and let us know how 1.2.0 performs in your helpdesk environment.
