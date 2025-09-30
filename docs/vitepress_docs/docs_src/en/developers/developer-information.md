---
description: Dev guide for the on-premise ATC ticket classifier. Learn to configure
  with YAML, run from the CLI, and extend with custom Python components & adapters.
title: Developer Information
---
# Developer Information for the ATC Community Edition

## Overview

The ATC Community Edition is an on-premise solution for automated classification of support tickets. The current MVP
version is controlled via a YAML configuration file and started via CLI. There is no REST API for uploading training
data or triggering a training run.

## Software Architecture

The application essentially consists of the following packages:

* **core** – configuration models, dependency injection helpers, the pipeline engine, and template rendering utilities.
* **base** – reusable pipe implementations (e.g. ticket fetch/update pipes and composite helpers).
* **hf_local** – HuggingFace-powered inference pipes shipped as examples.
* **ticket\_system\_integration** – adapters for different ticket systems.
* **main.py** – CLI entry point that wires the injector, scheduler, and orchestrator.

The orchestrator now executes YAML-defined `Pipe` graphs. Definitions are composed from reusable `defs`, rendered with the
current scope, and resolved through the dependency-injection container at runtime. Each scheduled entry declares which pipe tree
should run and how often the orchestrator should trigger it.

An example command to start the application:

```bash
python -m open_ticket_ai.src.ce.main start
```

## Pipeline Architecture

The runtime pipeline is described in YAML. `RawOpenTicketAIConfig` collects plug-ins, global configuration, reusable `defs`,
and the `orchestrator` schedule that instructs which pipes should run and in which interval. When the application boots, the
dependency-injection container loads this file, constructs singleton services declared under `defs`, and registers them in the
`UnifiedRegistry`. Pipes and templates can then reference these shared services by ID.

Every pipeline entry is normalised into a `RegisterableConfig` with an `id`, the target class in `use`, optional nested `steps`,
and optional orchestration metadata like `_if` and `depends_on`. At execution time the configuration is rendered against the
current `Context`, so Jinja2 expressions can pull values from previous results via helper functions such as
`get_pipe_result('classify', 'label')`. `_if` expressions (configured in YAML as `if:`) toggle pipes on or off per run, and
`depends_on` ensures that a pipe only executes after the listed dependencies have produced successful results.

The `Context` carries two dictionaries: `pipes` holds each step's `PipeResult` (success/failed/message/data), and `config`
exposes the rendered configuration for the active schedule entry. Pipes read from this context, perform their work inside the
asynchronous `_process()` method, and return data that becomes the `PipeResult.data` payload. Because every result shares the
same structure, downstream pipes and templates can easily react to failures or reuse earlier outputs.

The `orchestrator` field in YAML is a list of schedule entries. Each entry provides `run_every_milli_seconds` and a `pipe`
definition that can itself be a composite pipe (with nested `steps`) built from the reusable `defs`. The scheduler walks this
list, triggers runs when intervals elapse, and hands the orchestrator a fresh `Context` seeded with the schedule configuration.

## Training Custom Models

Direct training through the application is not provided in the MVP. Pre-trained models can be specified and used in the
configuration. If a model needs to be adjusted or newly created, this must be done outside the application.

## Extension

Custom fetchers, preparers, AI services, or modifiers can be implemented as Python classes and registered via the
configuration. Thanks to dependency injection, new components can be easily integrated.

## How to Add a Custom Pipe

The processing pipeline can be extended with your own pipe classes. A pipe is a
unit of work that receives a `Context`, inspects previously stored `PipeResult`
objects, and emits a new `PipeResult` with the latest data and status flags.

1. **Define a configuration model** (optional) for your pipe parameters.
2. **Subclass `Pipe`** and implement the asynchronous `_process()` method.
3. **Return a dictionary** shaped like `PipeResult` (or call `PipeResult(...).model_dump()`).

The following simplified example shows a sentiment analysis pipe that uses
HuggingFace locally:

```python
from typing import Any

from pydantic import BaseModel
from transformers import pipeline

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult


class SentimentPipeConfig(BaseModel):
    model_name: str = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    text: str


class SentimentAnalysisPipe(Pipe):
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.cfg = SentimentPipeConfig(**config)
        self.classifier = pipeline("sentiment-analysis", model=self.cfg.model_name)

    async def _process(self) -> dict[str, Any]:
        if not self.cfg.text:
            return PipeResult(success=False, failed=True, message="No text available", data={}).model_dump()

        sentiment = self.classifier(self.cfg.text)[0]
        return PipeResult(
            success=True,
            failed=False,
            data={
                "label": sentiment["label"],
                "confidence": sentiment["score"],
            },
        ).model_dump()
```

After implementing the class, register it under `open_ticket_ai.defs` (or
`general_config.pipe_classes`) so that the YAML pipeline can reference it via its
`id`. Because the orchestrator renders configuration through Jinja2, you can use
template expressions in your definitions to inject environment variables or
results from previous pipes.

## How to Integrate a New Ticket System

To connect another help desk system, implement a new adapter that inherits from
`TicketSystemAdapter`. The adapter converts between the external API and the
project's unified models.

1. **Create an adapter class**, e.g. `FreshdeskAdapter(TicketSystemAdapter)`.
2. **Implement all abstract methods**:
    - `find_tickets`
    - `find_first_ticket`
    - `create_ticket`
    - `update_ticket`
    - `add_note`
3. **Translate data** to and from the `UnifiedTicket` and `UnifiedNote` models.
4. **Provide a configuration model** for credentials or API settings.
5. **Register the adapter** in `create_registry.py` so it can be instantiated
   from the YAML configuration.

Once registered, specify the adapter in the `system` section of `config.yml` and
the orchestrator will use it to communicate with the ticket system.

## Summary

The ATC Community Edition offers a locally executed workflow for automatic ticket classification in its MVP version. All
settings are managed via YAML files; no REST API is available. External processes or scripts must be used for training.
