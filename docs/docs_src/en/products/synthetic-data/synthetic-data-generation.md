---
description: Generate multilingual synthetic customer-support ticket datasets with
  our Python tool. Features a graph pipes, AI assistants, rich fields & cost tracking.
---

# Synthetic Data Generation for Support Tickets

<WaitlistSignupForm />

Create high-quality, multilingual support-ticket datasets for classification, routing, and response automation.
This page describes our Python-based **Synthetic Data Generator** and the public dataset we created with it. It also
explains how the generator supports the **Open Ticket AI** training workflow and our commercial data-generation
services.

::: info

- **Purpose:** Generate realistic tickets (subject, body, queue, priority, type, tags, language, and a first AI agent
  reply).
- **Languages:** DE, EN, FR, ES, PT.
- **Pipeline:** Graph of configurable AI “nodes” (topic → email → tags → paraphrase → translate → response).
- **Models:** Works with OpenAI, OpenRouter, Together… (GPT-4, Qwen, LLaMA, etc.).
- **Controls:** Built-in CLI, dev/prod modes, cost & token tracking with currency summaries.
- **License:** Planned **LGPL** release.
- **Need the tool or custom mods?** → **sales@softoft.de**
  :::

## What it generates

- **Core fields:** `ticket_id`, `subject`, `body`
- **Classification labels:** `type` (Incident/Request/Problem/Change), `queue` (e.g., Technical Support, Billing, HR),
  `priority` (Low/Medium/High)
- **Language:** `language` (DE/EN/FR/ES/PT)
- **Tags:** 4–8 domain/topic tags per ticket
- **Agent reply:** a **first-response** message authored by an AI assistant

A sample record (CSV):

```csv
ticket_id,subject,body,language,type,queue,priority,tags,first_response
8934012332184,"VPN verbindet nicht","Seit dem Update keine Verbindung…","DE","Incident","IT / Security","High","vpn,update,remote-access,windows","Hallo! Bitte öffnen Sie die VPN-App…"
```

> IDs are guaranteed unique in a 12–13 digit range, making joins and merges simple across runs.

## How it works (in short)

The generator uses a **graph-based pipeline** of small, testable “nodes.” Typical path:

```
Topic → Draft subject → Draft email body → Tagging → Paraphrase → Translate → First response
```

You can reorder nodes, remove steps, or add your own. Each “assistant” is configurable (system/user prompts,
model/provider, limits). That means you can quickly produce domain-specific tickets (e.g., HR, healthcare, retail,
public sector) without rewriting code.

## Model & provider flexibility

Bring your preferred LLMs:

* **Providers:** OpenAI, OpenRouter, Together (and others via adapters)
* **Models:** GPT-4 class, Qwen, LLaMA, etc.
* Swap prompts per node to increase diversity and control tone, terminology, and structure.

## Cost & usage tracking (built in)

* **Per-run token and cost accounting** (input vs. output) per model
* **Configurable thresholds** that warn/error if a single run crosses a cost limit
* **Currency summaries** (e.g., USD, EUR) for clear budgeting
* **Dev vs. Prod modes** to switch between small test runs and full dataset builds

## Quick start

Run a dataset generation job with the built-in CLI:

```bash
python -m ticket_generator
```

Minimal config ideas (pseudocode):

```python
# config/config.py (example)
RUN = {
    "rows": 10_000,  # total configExamples
    "batch_size": 50,  # lower for cheap dev runs
    "languages": ["DE", "EN", "FR", "ES", "PT"],
    "timezone": "Europe/Berlin",
    "pipes": [
        "topic_node",
        "email_draft_node",
        "tagging_node",
        "paraphrase_node",
        "translate_node",
        "first_response_node"
    ],
    "models": {
        "default": {
            "provider": "openai",
            "name": "gpt-4o-mini",
            "max_tokens": 800
        }
    },
    "cost_limits": {
        "warn": 0.001,  # USD per single assistant run
        "error": 0.01
    }
}
```

> In practice, you’ll tune prompts, pick different models per node, and add domain-specific randomization tables (
> queues, priorities, business types, etc.).

## Output schema

Common columns you’ll see in our generated CSV/Parquet exports:

* `ticket_id` (12–13 digit string)
* `subject`, `body`
* `language` (DE/EN/FR/ES/PT)
* `type` ∈ (Incident, Request, Problem, Change)
* `queue` (domain-specific, e.g., *Technical Support*, *Billing*, *HR*)
* `priority` ∈ (Low, Medium, High)
* `tags` (array/list of 4–8)
* `first_response` (agent reply)

## Example dataset on Kaggle

We used this generator to build the public **Multilingual Customer Support Tickets** dataset, including **priorities,
queues, types, tags, and business types**, ideal for training ticket-classification and prioritization models.
➡️ Kaggle: **Multilingual Customer Support Tickets**

* Includes multiple languages and all labels listed above
* Community notebooks demonstrate classification and routing use cases

## How this supports Open Ticket AI

**Open Ticket AI** classifies **queue** and **priority** on inbound tickets. Synthetic data is invaluable when you have:

* **No or limited** labeled history
* **Sensitive** data that can’t leave your infrastructure
* A need for **balanced** classes (e.g., rare queues/priorities)
* **Multilingual** coverage from day one

We routinely use the generator to:

1. bootstrap model training,
2. balance long-tail classes, and
3. simulate multilingual operations.
   If you want us to generate tailored datasets (your domain/queues/priorities/tags, your languages), we offer it as a *
   *service**.

\::: tip Services
Need domain-specific synthetic data for your helpdesk? We’ll design prompts, nodes, and randomization tables for your
industry, integrate with your data pipeline, and deliver CSV/Parquet ready for training and evaluation.
**Contact:** [sales@softoft.de](mailto:sales@softoft.de)
\:::

## Licensing & availability

* The **Synthetic Data Generator** is planned to be released under **LGPL**.
* If you want early access, a private license, or custom modifications/extensibility, **email `sales@softoft.de`** and
  we’ll set it up for you.

---

### FAQ

**Is the dataset “real” or “synthetic”?**
Fully synthetic, produced by a configurable LLM pipeline.

**Can I add my own fields (e.g., *Business Unit*, *Impact*, *Urgency*)?**
Yes—extend the randomization tables and add a node to emit the fields.

**Can I control style and tone?**
Absolutely. Prompts are per-node, so you can enforce tone, formality, regionalisms, and terminology.

**How do I keep costs in check?**
Use dev mode (small `rows`, lower `max_tokens`), cost thresholds, and cheaper models for early iterations. Switch to
your preferred model mix once outputs look right.
