---
title: Configuration Guide
description: Learn how to configure Open Ticket AI pipelines
lang: en
nav:
  group: Guides
  order: 2
draft: false
---

# Configuration Guide

Learn how to configure your Open Ticket AI pipelines using YAML configuration files.

## Configuration Structure

All configuration lives under the top-level `open_ticket_ai` key.

### Basic Example

```yaml
open_ticket_ai:
  plugins:
    - otai-base
  services:
    template_renderer:
      use: base:Jinja2TemplateRenderer
  orchestrator:
    use: base:SimpleSequentialOrchestrator
    params:
      steps: []
```

## Next Steps

Explore advanced configuration options and plugin development.
