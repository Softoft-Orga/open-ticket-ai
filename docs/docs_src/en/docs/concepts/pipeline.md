# Pipeline System

The pipeline system is Open Ticket AI's core orchestration mechanism. It coordinates the execution of data processing workflows through sequences of interconnected processing components called **pipes**.

## What is a Pipeline?

A **pipeline** in Open Ticket AI is a configured sequence of pipes that execute in order to accomplish a specific task, such as fetching tickets, classifying them, and updating their properties. Pipelines are:

- **Sequential**: Pipes execute one after another in defined order
- **Context-driven**: Data flows through a shared execution context
- **Declarative**: Defined in YAML configuration files
- **Scheduled**: Triggered by time intervals or external events
- **Composable**: Pipes can contain nested sub-pipelines

## Pipeline Architecture

```plantuml
@startuml Pipeline Architecture

skinparam classAttributeIconSize 0
skinparam classFontSize 11

package "Core Pipeline Components" {
    abstract class Pipe<ParamsT> {
        +pipe_config: PipeConfig
        --
        +process(context: PipeContext): PipeContext
        +have_dependent_pipes_been_run(context): bool
        #{abstract} _process(): PipeResult
        #_save_pipe_result(context, result): PipeContext
    }

    class CompositePipe {
        -_factory: RenderableFactory
        -_context: PipeContext
        --
        +_process_steps(context): list[PipeResult]
        +_build_pipe_from_step_config(step_config, context): Pipe
        +process(context): PipeContext
    }

    class PipeConfig<ParamsT> {
        +id: str
        +use: str
        +params: ParamsT
        +if_: str | bool
        +depends_on: list[str]
        +steps: list[PipeConfig] | None
        --
        +should_run: bool
    }

    class PipeContext {
        +pipes: dict[str, PipeResult]
        +params: dict[str, Any]
        +parent: PipeContext | None
        --
        +has_succeeded(pipe_id: str): bool
    }

    class PipeResult<DataT> {
        +success: bool
        +failed: bool
        +message: str
        +data: DataT
        --
        +__and__(other): PipeResult
        +union(results): PipeResult
    }
}

package "Pipeline Construction" {
    class RenderableFactory {
        -_template_renderer: TemplateRenderer
        -_registerable_configs: list[RenderableConfig]
        --
        +create_pipe(pipe_config_raw, scope): Pipe
        -__create_renderable_instance(config, scope): Renderable
        -__resolve_injects(injects, scope): dict
    }

    class TemplateRenderer {
        --
        +render_template(template, context): str
        +render_object(obj, context): Any
    }
}

package "Orchestration" {
    class PipeRunner {
        +definition: RunnerDefinition
        +pipe_factory: RenderableFactory
        --
        +execute(): void
        +on_trigger_fired(): void
    }

    class RunnerDefinition {
        +pipe_id: str
        +run: PipeConfig
        +trigger: Trigger
    }

    class Trigger {
        +interval_ms: int
    }
}

' Inheritance relationships
CompositePipe --|> Pipe

' Composition relationships
Pipe --> PipeConfig : configured by
Pipe --> PipeContext : reads/writes
Pipe --> PipeResult : produces
PipeContext --> PipeResult : stores
CompositePipe --> RenderableFactory : uses to create child pipes
PipeConfig --> PipeConfig : contains steps

' Factory relationships
RenderableFactory --> Pipe : creates
RenderableFactory --> TemplateRenderer : uses
RenderableFactory --> PipeConfig : renders

' Orchestration relationships
PipeRunner --> RunnerDefinition : configured by
PipeRunner --> RenderableFactory : uses
RunnerDefinition --> PipeConfig : contains
RunnerDefinition --> Trigger : scheduled by

note right of Pipe
    Base class for all pipes.
    Handles dependency checking,
    conditional execution, and
    result persistence.
end note

note right of CompositePipe
    Special pipe that orchestrates
    multiple child pipes defined
    in its "steps" configuration.
end note

note bottom of PipeContext
    Shared state that flows through
    the pipeline. Maps pipe IDs to
    their results for data sharing.
end note

@enduml
```

## Pipeline Orchestration Lifecycle

The pipeline system follows a well-defined lifecycle from configuration to execution:

### 1. Initialization Phase

When Open Ticket AI starts:

1. **Configuration Loading**: YAML configuration files are parsed
2. **Service Bootstrapping**: Dependency injection container is initialized
3. **Factory Setup**: `RenderableFactory` and `TemplateRenderer` are created
4. **Registry Population**: Services and pipe definitions are registered

### 2. Scheduling Phase

The orchestrator sets up pipeline execution schedules:

1. **Pipeline Definitions**: Each pipeline in `orchestrator.pipelines` is processed
2. **Runner Creation**: A `PipeRunner` is created for each pipeline
3. **Trigger Setup**: Time-based or event-based triggers are configured
4. **Schedule Activation**: Triggers begin firing at specified intervals

### 3. Rendering Phase

When a pipeline is triggered, its configuration is rendered:

```plantuml
@startuml Pipeline Rendering Flow

actor Orchestrator
participant "PipeRunner" as Runner
participant "RenderableFactory" as Factory
participant "TemplateRenderer" as Renderer
participant "PipeConfig" as Config

Orchestrator -> Runner: on_trigger_fired()
activate Runner

Runner -> Factory: create_pipe(pipe_config_raw, scope)
activate Factory

Factory -> Renderer: render_base_model(pipe_config, scope)
activate Renderer

Renderer -> Renderer: Process Jinja2 templates\nin configuration strings

note right
    Template rendering resolves:
    - Environment variables
    - Previous pipe results
    - Context parameters
    - Service references
end note

Renderer --> Factory: rendered_config
deactivate Renderer

Factory -> Config: Validate rendered configuration
activate Config
Config --> Factory: validated PipeConfig
deactivate Config

Factory -> Factory: __resolve_injects(injects, scope)
note right
    Resolve dependency injections:
    - Service lookups
    - Nested pipe configurations
    - Shared adapters
end note

Factory -> Factory: __create_renderable_instance(config, scope)
note right
    Instantiate the Pipe class
    specified in "use" field
end note

Factory --> Runner: Pipe instance
deactivate Factory

Runner --> Orchestrator: Ready for execution
deactivate Runner

@enduml
```

**Key rendering concepts:**

- **Template Resolution**: Jinja2 templates in configuration values are evaluated against the current context
- **Dependency Injection**: Services referenced in `injects` are resolved from the registry
- **Conditional Evaluation**: The `if` field determines whether the pipe should execute
- **Dependency Checking**: The `depends_on` field specifies prerequisite pipes

### 4. Execution Phase

Once rendered, the pipeline executes:

```plantuml
@startuml Pipeline Execution Flow

participant "PipeRunner" as Runner
participant "Pipe" as Pipe
participant "PipeContext" as Context
participant "CompositePipe" as Composite
participant "Child Pipe" as Child

Runner -> Pipe: process(context)
activate Pipe

Pipe -> Pipe: Check if_condition
alt if_ == False
    Pipe --> Runner: Return context unchanged
    note right: Pipe is skipped
else if_ == True
    
    Pipe -> Pipe: have_dependent_pipes_been_run(context)
    
    alt dependencies not met
        Pipe --> Runner: Return context unchanged
        note right: Pipe is skipped
    else dependencies met
        
        alt Pipe is CompositePipe
            Pipe -> Composite: _process_steps(context)
            activate Composite
            
            loop for each step in steps
                Composite -> Composite: _build_pipe_from_step_config(step, context)
                Composite -> Child: process(context)
                activate Child
                Child -> Child: _process()
                Child -> Context: Save result to context.pipes[step_id]
                activate Context
                Child --> Composite: Updated context
                deactivate Child
                deactivate Context
            end
            
            Composite -> Composite: PipeResult.union(all_step_results)
            Composite --> Pipe: Aggregated PipeResult
            deactivate Composite
            
        else Regular Pipe
            Pipe -> Pipe: _process()
            note right
                Execute pipe's
                business logic
            end note
            Pipe --> Pipe: PipeResult
        end
        
        Pipe -> Context: _save_pipe_result(context, pipe_result)
        activate Context
        note right: Store result at context.pipes[pipe_id]
        Context --> Pipe: Updated context
        deactivate Context
    end
end

Pipe --> Runner: Final context with results
deactivate Pipe

@enduml
```

**Execution flow details:**

1. **Conditional Check**: Pipe evaluates its `if` condition
2. **Dependency Check**: Verifies all `depends_on` pipes have succeeded
3. **Processing**: 
   - **Regular Pipe**: Calls `_process()` to execute business logic
   - **Composite Pipe**: Iterates through `steps`, creating and executing child pipes
4. **Result Aggregation**: Composite pipes merge child results using `PipeResult.union()`
5. **Context Update**: Result is saved to `context.pipes[pipe_id]`
6. **Return**: Updated context is returned for next pipe

### 5. Result Handling Phase

After execution:

1. **Success Check**: `PipeRunner` examines the final `PipeResult`
2. **Logging**: Success or failure is logged with context
3. **Error Handling**: Exceptions are caught and logged
4. **Cleanup**: Context is discarded after pipeline completion

## When and How Pipelines Execute

### Trigger Mechanisms

Pipelines can be triggered by:

#### 1. Time-based Intervals

The most common trigger type, configured with `run_every_milli_seconds`:

```yaml
orchestrator:
  pipelines:
    - name: ticket_classifier
      run_every_milli_seconds: 300000  # Every 5 minutes
      pipes:
        - pipe_name: classify_tickets
```

#### 2. Event-based Triggers

Pipelines can respond to external events (webhook triggers, file system changes, etc.)

### Execution Guarantees

The orchestrator provides:

- **Non-overlapping Execution**: A pipeline won't start if previous execution is still running
- **Error Isolation**: One pipeline failure doesn't affect others
- **Consistent Context**: Each execution gets a fresh context
- **Ordered Execution**: Pipes execute in configuration order

## Relationship of Pipes, Composite Pipes, and Steps

### Regular Pipes

**Regular pipes** are atomic processing units:

```yaml
- id: fetch_tickets
  use: open_ticket_ai.base.pipes.ticket_system_pipes.FetchTicketsPipe
  params:
    criteria:
      state: new
```

A regular pipe:
- Implements `_process()` method with business logic
- Receives input from context
- Produces a single `PipeResult`
- Returns updated context

### Composite Pipes

**Composite pipes** orchestrate multiple child pipes:

```yaml
- id: process_ticket_workflow
  use: open_ticket_ai.base.pipes.CompositePipe
  steps:
    - id: fetch
      use: FetchTicketsPipe
      params:
        criteria: { state: new }
    
    - id: classify
      use: ClassifyTicketPipe
      params:
        input_ticket: "{{ pipes.fetch.data.ticket }}"
      depends_on: [fetch]
    
    - id: update
      use: UpdateTicketPipe
      params:
        ticket_id: "{{ pipes.fetch.data.ticket.id }}"
        updates: "{{ pipes.classify.data.classification }}"
      depends_on: [classify]
```

A composite pipe:
- Contains a `steps` list of child pipe configurations
- Uses `RenderableFactory` to instantiate each child
- Executes children sequentially
- Merges child results into a single `PipeResult`
- Allows child pipes to depend on previous siblings

### Dependency Relationships

The `depends_on` field creates execution dependencies:

```yaml
- id: step_a
  use: SomePipe

- id: step_b
  use: AnotherPipe
  depends_on: [step_a]  # Waits for step_a to succeed

- id: step_c
  use: FinalPipe
  depends_on: [step_a, step_b]  # Waits for both
```

**Dependency behavior:**

- A pipe only executes if all `depends_on` pipes have `success=True` and `failed=False`
- If dependencies aren't met, the pipe is skipped
- Dependencies are checked via `context.has_succeeded(pipe_id)`
- Circular dependencies are not detected and will cause execution to skip

### Conditional Execution

The `if` field enables conditional execution:

```yaml
- id: conditional_update
  use: UpdateTicketPipe
  if: "{{ pipes.classify.data.confidence > 0.8 }}"
  params:
    ticket_id: "{{ ticket.id }}"
```

**Conditional behavior:**

- `if` is evaluated as a Jinja2 template
- Result must be truthy for pipe to execute
- Can reference context data, environment variables, or service state
- Defaults to `"True"` if not specified

## Implementation References

The pipeline system is implemented across several modules:

### Core Pipeline Module

**Location**: `src/open_ticket_ai/core/pipeline/`

- **`pipe.py`**: Base `Pipe` class with `process()` and dependency checking
- **`pipe_config.py`**: `PipeConfig` and `PipeResult` data models
- **`pipe_context.py`**: `PipeContext` for sharing data between pipes

### Base Pipes Module

**Location**: `src/open_ticket_ai/base/pipes/`

- **`composite_pipe.py`**: `CompositePipe` implementation for step orchestration
- **`jinja_expression_pipe.py`**: Pipe that evaluates Jinja2 expressions

### Orchestration Module

**Location**: `src/open_ticket_ai/core/orchestration/`

- **`orchestrator.py`**: Main orchestrator that manages pipeline scheduling
- **`scheduled_runner.py`**: `PipeRunner` that executes individual pipelines
- **`trigger.py`**: Trigger definitions for scheduling

### Configuration Module

**Location**: `src/open_ticket_ai/core/config/`

- **`renderable_factory.py`**: `RenderableFactory` for creating pipes from configuration
- **`renderable.py`**: Base `Renderable` interface and `RenderableConfig` model

### Template Rendering Module

**Location**: `src/open_ticket_ai/core/template_rendering/`

- **`template_renderer.py`**: Jinja2 template rendering for configuration values

## Best Practices

### Designing Pipelines

✅ **Do:**
- Keep pipelines focused on a single workflow
- Use descriptive IDs for pipes
- Leverage dependencies for clear execution order
- Use conditionals to skip unnecessary work
- Document expected context data

❌ **Don't:**
- Create overly long pipelines (split into multiple if needed)
- Use ambiguous pipe IDs
- Create circular dependencies
- Rely on implicit execution order
- Modify context data without documenting

### Working with Context

✅ **Do:**
- Use descriptive keys in `PipeResult.data`
- Check if data exists before accessing
- Use Jinja2 templates for safe access: `{{ pipes.step_id.data.field | default('fallback') }}`
- Clean up large objects after use

❌ **Don't:**
- Store secrets in context (use environment variables)
- Mutate context directly (use `model_copy()`)
- Rely on undocumented context keys
- Store entire API responses (extract needed fields)

### Composite Pipe Design

✅ **Do:**
- Use composite pipes to group related operations
- Make steps atomic and reusable
- Use clear step IDs
- Document step dependencies
- Keep step count manageable (< 10)

❌ **Don't:**
- Nest composite pipes too deeply (>3 levels)
- Create tightly coupled steps
- Share state outside the context
- Skip error handling in steps

## Related Documentation

- **[Pipeline Architecture](./pipeline-architecture.md)** - Detailed system architecture
- **[First Pipeline Tutorial](../guides/first_pipeline.md)** - Step-by-step guide to creating pipelines
- **[Dependency Injection](../code/dependency_injection.md)** - Service management and injection
- **[Template Rendering](../code/template_rendering.md)** - Jinja2 template system
- **[Configuration Structure](../configuration/config_structure.md)** - YAML configuration reference
- **[Plugin Development](../plugins/plugin_development.md)** - Creating custom pipes

## Summary

The pipeline system in Open Ticket AI provides a powerful, flexible framework for orchestrating data processing workflows. By combining:

- **Declarative configuration** for defining workflows
- **Sequential execution** for predictable behavior
- **Shared context** for data flow
- **Dependency management** for execution ordering
- **Composite pipes** for workflow composition
- **Template rendering** for dynamic configuration

You can build sophisticated automation workflows that are maintainable, testable, and extensible.
