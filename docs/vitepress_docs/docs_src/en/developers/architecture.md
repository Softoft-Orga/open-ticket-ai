---
description: Learn about the Open Ticket AI architecture. Discover how its modular
  data pipeline and Hugging Face models power intelligent ticket classification and
  routing.
layout: page
pageClass: full-page
title: Open Ticket AI Architecture Overview
---

# Architecture Overview

Open Ticket AI is built around a modular execution engine that processes support tickets through configurable pipelines.
Each pipeline combines reusable "pipes" that fetch data, run Hugging Face models, and push results back into external
systems.

## System Overview

- **Self-hosted core**: Runs as a Python service that loads configuration, registers services, and supervises pipeline
  execution.
- **Dependency-injected services**: Adapters, models, and utilities are provided by an inversion-of-control container so
  pipes can request only what they need.
- **Composable pipelines**: YAML configuration describes which pipes run, their order, and any conditional `when`
  clauses.
- **Shared execution context**: Intermediate results are stored on a context object so later steps can reuse previous
  outputs without recomputing work.

## Core Building Blocks

### Pipeline Orchestrator

The orchestrator loads the active pipeline configuration, renders any Jinja2 templates, and instantiates each pipe
just-in-time. It respects `when` conditions, iterates through steps, and persists pipe state back into the shared
context.

### Pipes

Pipes encapsulate a single unit of work—fetching tickets, classifying text, updating metadata, or logging telemetry.
They are stateless between runs; every execution receives fresh inputs from the orchestrator and writes results back
into the context for downstream steps.

### Services

Reusable capabilities (HTTP clients, Hugging Face pipelines, storage backends) live in the service container. Pipes
request services with `get_instance` so infrastructure code is centralized and easy to swap or extend.

### Ticket System Adapters

Adapters translate between Open Ticket AI and external helpdesk platforms. Fetcher pipes rely on an adapter to load
tickets, while updater pipes use the same adapter to apply queue, priority, or comment changes back to the remote
system.

### Machine Learning Models

Queue and priority predictions are produced by Hugging Face models that run inside dedicated pipes. These pipes hydrate
inputs from the context, execute the model, and enrich the context with structured predictions that later pipes consume.

## End-to-End Processing Flow

1. The orchestrator initializes services and the execution context, then selects the configured pipeline.
2. A fetch pipe uses a ticket system adapter to pull candidate tickets and stores them in the context.
3. Preprocessing pipes clean and normalize the ticket text for model consumption.
4. Classification pipes execute Hugging Face models to predict queue assignments, priorities, or tags.
5. Post-processing pipes consolidate predictions, apply business rules, and prepare update payloads.
6. Updater pipes call back into the ticket system adapter to write results (queue changes, priority updates, internal
   notes) to the original ticket.

## Extending the Platform

- **Add a new adapter**: Implement the adapter interface for another ticketing platform and register it in the service
  container.
- **Customize pipelines**: Compose new combinations of pipes in YAML, using `when` clauses to guard optional steps.
- **Introduce new intelligence**: Create additional model pipes or rule-based processors that read from and write to the
  shared context.

This architecture keeps the classification logic decoupled from integrations, enabling teams to tailor the pipeline to
their workflows without modifying the core runtime.
