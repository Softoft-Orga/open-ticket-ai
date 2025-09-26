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

* **core** – base classes, configuration models, and helper functions.
* **run** – contains the pipeline for ticket classification.
* **ticket\_system\_integration** – adapters for different ticket systems.
* **main.py** – CLI entry point that starts the scheduler and the orchestrator.

The orchestrator executes configurable `AttributePredictors`, which are composed of `DataFetcher`, `DataPreparer`,
`AIInferenceService`, and `Modifier`. All components are defined in `config.yml` and validated at program startup.

An example command to start the application:

```bash
python -m open_ticket_ai.src.ce.main start
```

## Training Custom Models

Direct training through the application is not provided in the MVP. Pre-trained models can be specified and used in the
configuration. If a model needs to be adjusted or newly created, this must be done outside the application.

## Extension

Custom fetchers, preparers, AI services, or modifiers can be implemented as Python classes and registered via the
configuration. Thanks to dependency injection, new components can be easily integrated.

## How to Add a Custom Pipe

The processing pipeline can be extended with your own pipe classes. A pipe is a
unit of work that receives a `PipelineContext`, modifies it and returns it. All
pipes inherit from the `Pipe` base class which already
implements the `Providable` mixin.

1. **Create a configuration model** for your pipe if it needs parameters.
2. **Subclass `Pipe`** and implement the `process` method.
3. **Override `get_provider_key()`** if you want a custom key.

The following simplified example from the `AI_README` shows a sentiment analysis
pipe:

```python
class SentimentPipeConfig(BaseModel):
    model_name: str = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"


class SentimentAnalysisPipe(Pipe, Providable):
    def __init__(self, config: SentimentPipeConfig):
        super().__init__(config)
        self.classifier = pipeline("sentiment-analysis", model=config.model_name)

    def process(self, context: PipelineContext) -> PipelineContext:
        ticket_text = context.data.get("combined_text")
        if not ticket_text:
            context.stop_pipeline()
            return context

        sentiment = self.classifier(ticket_text)[0]
        context.data["sentiment"] = sentiment["label"]
        context.data["sentiment_confidence"] = sentiment["score"]
        return context

    @classmethod
    def get_provider_key(cls) -> str:
        return "SentimentAnalysisPipe"
```

After implementing the class, register it in your dependency injection registry
and reference it in `config.yml` using the provider key returned by
`get_provider_key()`.

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
