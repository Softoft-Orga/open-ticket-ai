---
description: 'Discover Open Ticket AI''s suite: an on-prem classifier, hosted API,
  synthetic data generator, and public models to automate your support ticket workflow.'
pageClass: full-page
---

# Products Overview

Use this page to see what’s available today, what’s hosted by us, and what’s coming next.
**Open Ticket AI** is the flagship on-prem product; **models** and **APIs** are optional add-ons.

## At a glance

<Table>
    <Row>
      <C header>Product</C>
      <C header>What it is</C>
      <C header>Status</C>
      <C header>Links</C>
    </Row>
    <Row>
      <C><strong>Open Ticket AI (On-Prem/Main Product)</strong></C>
      <C>Local, open-source ticket classifier (queues & priority) integrated via pipelines/adapters.</C>
      <C>✅ Available</C>
      <C><Link to="/">Overview</Link></C>
    </Row>
    <Row>
      <C><strong>Hosted Prediction API (German)</strong></C>
      <C>HTTP API to classify queue & priority using our public German base model (hosted by us).</C>
      <C>✅ Free for now</C>
      <C><Link to="/products/prediction-api/overview">API Docs</Link></C>
    </Row>
    <Row>
      <C><strong>Public Base Models (German)</strong></C>
      <C>Base models for queue/priority published on Hugging Face for users without their own data.</C>
      <C>✅ Available</C>
      <C>See links in <Link to="/products/prediction-api/overview">API Docs</Link></C>
    </Row>
    <Row>
      <C><strong>Synthetic Data Generator</strong></C>
      <C>Python tool to create multilingual synthetic ticket datasets; planned LGPL.</C>
      <C>✅ Available</C>
      <C><Link to="/products/synthetic-data/synthetic-data-generation">Generator</Link></C>
    </Row>
    <Row>
      <C><strong>Ticket Datasets (v5, v4, v3)</strong></C>
      <C>Synthetic datasets made with our generator (EN/DE focus in v5/v4; more langs in v3).</C>
      <C>✅ Available</C>
      <C><Link to="/products/synthetic-data/ticket-dataset">Dataset</Link></C>
    </Row>
    <Row>
      <C><strong>English Prediction Model</strong></C>
      <C>Base model for EN queue/priority.</C>
      <C>🚧 Coming soon</C>
      <C>(will be added here)</C>
    </Row>
    <Row>
      <C><strong>Additional Languages & Attributes</strong></C>
      <C>Models for other languages; predictions for tags, assignee; optional first-answer.</C>
      <C>🧭 Exploring</C>
      <C>(roadmap)</C>
    </Row>
    <Row>
      <C><strong>Web UI for Data Generator</strong></C>
      <C>Browser UI on top of the generator for non-technical users.</C>
      <C>🧭 Exploring</C>
      <C>(roadmap)</C>
    </Row>
</Table>

> **Pricing note:** The hosted **German Prediction API** is currently free. If demand drives infra costs too high, we
> may introduce rate limits or pricing. On-prem **Open Ticket AI** remains open-source and local.

---

## Open Ticket AI (On-Prem/Main Product)

- Runs locally; integrates with Znuny/OTRS/OTOBO via adapters.
- Classifies **Queue** & **Priority** on inbound tickets; extensible pipeline architecture.
- Pairs well with our **Synthetic Data Generator** for cold-start or class balancing.

**Learn more:**
[Overview](../index.md)

---

## Hosted Prediction API & Public Base Models (German)

- For teams **without their own data** where the **base queues/priorities** fit reasonably well.
- Use the **German** model via our hosted API (**free for now**).
- Models are **public on Hugging Face**; you can also self-host or fine-tune.

**Start here:** [Prediction API](./prediction-api/overview.md)

---

## Synthetic Data Generator

- Python tool to create realistic, labeled ticket datasets (subject, body, queue, priority, type, tags, language, first
  answer).
- Planned **LGPL** release; email for access or modifications: **sales@softoft.de**.

**Details:** [Synthetic Data Generation](./synthetic-data/synthetic-data-generation.md)

---

## Ticket Datasets

- Multiple versions available:
    - **v5 / v4:** EN & DE, largest and most diverse.
    - **v3:** more languages (e.g., FR/ES/PT), smaller.
- Ideal for bootstrapping, benchmarking, and multilingual experiments.

**Browse:** [Multilingual Customer Support Tickets](./synthetic-data/ticket-dataset.md)

---

## Roadmap

- **English** base model for queue/priority (hosted & downloadable).
- Optional models for **other languages**.
- Additional attributes: **tags**, **assignee**, and **first-answer** generation.
- Early prototype of a **web interface** for the data generator.

---

## FAQ

**Is the API part of Open Ticket AI?**
No. **Open Ticket AI** runs locally. The **Prediction API** is a separate, hosted service that uses our public models.

**Can I bring my own taxonomy?**
Yes. Train locally with your data, or ask us to generate synthetic data that mirrors your queues/priorities.

**Support & Services?**
We offer support subscriptions and custom integrations. Contact **sales@softoft.de**.
