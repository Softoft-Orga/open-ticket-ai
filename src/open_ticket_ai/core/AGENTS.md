# Core Infrastructure Guidelines

**Location:** `/src/open_ticket_ai/core/` directory  
**Parent Guidelines:** [Source AGENTS.md](../../AGENTS.md)  
**Last Updated:** 2026-04-10

Guidelines for `src/open_ticket_ai/core/` — the foundational infrastructure of the runtime.

## Core Responsibilities

The `core/` module provides essential infrastructure:

- `pipes/` — `Pipe` base class, `PipeResult`, `PipeContext` (execution model)
- `ticket_system_integration/` — `TicketSystemService` ABC and unified models
- `ai_classification_services/` — `ClassificationService` ABC and models
- `logging/` — `LoggerFactory` / `AppLogger` interfaces (stdlib adapter)
- `base_model.py` — `StrictBaseModel` (frozen, extra=forbid)

## Pipe Execution Model

The `Pipe` base class defines the execution contract:

```python
class Pipe(ABC):
    def __init__(self, pipe_id: str = ""): ...

    async def process(self, context: PipeContext) -> PipeResult:
        # final — calls _process(), logs before/after

    @abstractmethod
    async def _process(self, context: PipeContext) -> PipeResult: ...
```

- Pipes take direct typed params in their constructors (no config dict)
- Use stdlib `logging.getLogger()` — no injected LoggerFactory needed
- `PipeContext.get_result(pipe_id, data_key)` retrieves prior pipe outputs
- `PipeResult` tracks success/failure/skip with optional data dict

## Removed Layers (as of 2026-04)

The following were removed during the pipeline simplification:

- `config/` — `AppConfig`, `OpenTicketAIConfig`, `ConfigBuilder`, `PipeConfigBuilder`
- `dependency_injection/` — `ComponentRegistry`, `AppModule`, Injector DI
- `plugins/` — `Plugin`, `PluginLoader`, entry-point discovery
- `template_rendering/` — `TemplateRenderer`, Jinja-in-YAML param rendering
- `injectables/` — `Injectable`, `InjectableConfig`, `InjectableConfigBase`
- `pipes/pipe_factory.py` — runtime string-to-class resolution

Pipeline configuration now lives in `open_ticket_ai/pipeline.py` as direct Python.

## Test Placement

Tests for core components: `tests/unit/core/`
