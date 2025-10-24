# Predefined Pipe Concepts

:::warning Exploratory design
This page documents an exploratory design for predefined Pipes. The feature is not yet available in production releases and the concepts here may change significantly as we validate the approach with internal prototypes.
:::

This document captures early ideas for shipping reusable, predefined Pipes that can be imported into project-level YAML
pipelines.

## Current status

Predefined Pipes are in the discovery phase with only YAML prototypes drafted for internal review. No runtime support exists in the engine, and the catalog has not been published. Engineering is validating the import mechanics, dependency handling, and packaging flows before committing to an implementation timeline. The immediate focus is on delivering the loader, compatibility tests, and developer tooling outlined below, followed by iterative pilot programs with a small set of design partners.

## Goals

- Provide a catalog of shareable automation patterns for support workflows.
- Allow teams to compose complex automations by importing a single file.
- Keep the predefined pipes compatible with the existing execution engine, so an imported YAML can run without
  additional wiring.

## Design Principles

1. **Single-file portability** – Each predefined Pipe lives in its own YAML file with all required steps and metadata.
   Importing the file should immediately make the Pipe runnable.
2. **Declarative parameters** – Pipes expose a `parameters` block where downstream YAMLs can override defaults without
   editing the shared file.
3. **Idempotent steps** – Every Pipe should be safe to run multiple times.
4. **Observability hooks** – Standard annotations for logging, metrics, and alerting so imported Pipes integrate cleanly
   with monitoring.

## YAML Structure Prototype

```yaml
# file: pipes/triage-basic.yaml
pipe:
  name: triage-basic
  version: 0.1.0
  description: >-
    Basic triage workflow that classifies an incoming ticket, enriches context,
    and queues follow-up actions.

  parameters:
    classification_model: clf-ticket-small
    notification_channel: slack://#support-triage
    sla_minutes: 30

  steps:
    - id: normalize
      uses: actions/normalize-text@v1
      with:
        fields: [ title, description ]

    - id: classify
      uses: actions/classify@v2
      with:
        model: "${{ parameters.classification_model }}"
        input: ${{ steps.normalize.output.cleaned_text }}

    - id: sla_guard
      uses: actions/sla-reminder@v1
      when: ${{ ticket.created_at + parameters.sla_minutes < now() }}
      with:
        channel: "${{ parameters.notification_channel }}"
        message: "SLA threshold reached for ticket ${{ ticket.id }}"

  outputs:
    classification: ${{ steps.classify.output.label }}
    confidence: ${{ steps.classify.output.confidence }}
```

### Import Pattern

The team-level YAML simply references the predefined Pipe and optionally overrides parameters:

```yaml
imports:
  - from: pipes/triage-basic.yaml
    as: triage-basic

pipe:
  name: support-intake
  steps:
    - uses: triage-basic
      with:
        classification_model: clf-ticket-enterprise
        notification_channel: slack://#support-critical
```

## Catalog Ideas

| Pipe Name                    | Problem Solved                                          | Key Steps                                                            | Notes                             |
|------------------------------|---------------------------------------------------------|----------------------------------------------------------------------|-----------------------------------|
| `triage-basic`               | Classify and enqueue new tickets                        | normalization → classification → SLA reminder                        | Baseline for all teams            |
| `triage-advanced`            | Multi-language classification with translation fallback | language detection → translation → classification → routing          | Requires translation credits      |
| `auto-escalate`              | Escalate urgent tickets                                 | severity detection → senior engineer notification → incident logging | Integrates with on-call schedules |
| `knowledge-base-suggest`     | Suggest KB articles to agents                           | vector embed → similarity search → suggestion post                   | Consumes search API quota         |
| `customer-sentiment-monitor` | Track sentiment drift over conversation lifetime        | conversation aggregation → sentiment scoring → trend alerting        | Works best with hourly cron       |
| `bug-report-digest`          | Aggregate bug-related tickets                           | label filter → deduplicate → weekly digest email                     | Ties into product board           |

## Validation Checklist

Before publishing a predefined Pipe:

- [ ] Verify schema with `python -m open_ticket.pipeline validate pipes/<pipe-name>.yaml`.
- [ ] Run integration tests against staging data.
- [ ] Document required secrets, external services, and quotas.
- [ ] Tag the pipe release in the catalog repository.

## Next Steps

1. Build a lightweight loader that merges imported parameters into the active pipeline context and validates dependencies.
2. Create automated smoke and contract tests to ensure imported pipes remain compatible across version bumps.
3. Prototype a CLI command `ot pipe add triage-basic` that fetches and verifies the YAML before adding it to a project repository.
4. Evaluate hosting the catalog in a Git-based registry for versioned distribution and controlled pilot access.
