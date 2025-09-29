# Pipeline Execution Flow

```mermaid
flowchart TD
    Start([Start]) --> LoadConfig[Load Config]
    LoadConfig --> InitContext[Initialize Context]
    InitContext --> CreateContainer[Create Services]
    
    CreateContainer --> OrchestratorLoop{Orchestrator Loop}
    
    OrchestratorLoop --> GetPipelineConfig[Get Pipeline Config]
    GetPipelineConfig --> RenderConfig[Render Config with Jinja2]
    
    RenderConfig --> CreatePipe[Create Pipe]
    CreatePipe --> CheckWhen{Check when condition}
    
    CheckWhen -->|True| ProcessSteps[Process Steps]
    CheckWhen -->|False| SkipPipe[Skip Pipe]
    
    ProcessSteps --> StepLoop{For each step}
    
    StepLoop --> RenderStep[Render Step Config]
    RenderStep --> BuildPipe[Build Step Pipe]
    BuildPipe --> ExecutePipe[Execute Pipe]
    
    ExecutePipe --> PipeWork[Do Pipe Work]
    PipeWork --> SaveResult[Save to Context]
    SaveResult --> MoreSteps{More Steps?}
    
    MoreSteps -->|Yes| StepLoop
    MoreSteps -->|No| ExecuteMain[Execute Main Process]
    
    ExecuteMain --> SaveState[Save Pipe State]
    
    SkipPipe --> CheckMore{More Pipelines?}
    SaveState --> CheckMore
    
    CheckMore -->|Yes| OrchestratorLoop
    CheckMore -->|No| FinalState[Final Context]
    
    FinalState --> End([End])
    
    %% Styling
    classDef configClass fill:#e1f5fe
    classDef processClass fill:#f3e5f5
    classDef contextClass fill:#e8f5e8
    classDef decisionClass fill:#fff3e0
    
    class LoadConfig,RenderConfig,RenderStep configClass
    class ProcessSteps,ExecutePipe,PipeWork processClass
    class InitContext,SaveResult,SaveState,FinalState contextClass
    class CheckWhen,StepLoop,MoreSteps,CheckMore,OrchestratorLoop decisionClass
```

## Key Components

### Context Flow
- **Initial State**: Empty context with `pipes={}` and `config={}`
- **State Accumulation**: Each pipe saves results to `context.pipes[pipe_name]`
- **Template Access**: Subsequent steps access previous results via `{{ pipes.* }}`

### Configuration Rendering
- **Pipeline Level**: Renders service instances and environment variables
- **Step Level**: Renders with current execution context and pipe results
- **Just-in-Time**: Pipes created dynamically from rendered configurations

### Execution Pattern
- **Conditional Processing**: `when` conditions control pipe execution
- **Nested Steps**: Pipes can contain multiple sub-steps
- **State Preservation**: Context carries state through entire pipeline execution

### Service Integration
- **Registry Pattern**: Services accessed via `{{ get_instance('service_id') }}`
- **Template Functions**: Jinja2 functions for dynamic service resolution
- **Stateless Pipes**: Pipes recreated for each execution with fresh context

## Dependency Injection Lifecycle

Open Ticket AI keeps object wiring out of the pipeline code by funnelling all
instantiation through a lightweight dependency injection (DI) layer.

### 1. Container bootstrapping
- The application entry point builds an `Injector` with `AppModule` and uses it
  to resolve the orchestrator, configuration, and instance factory during
  startup.
- `AppModule` reads the YAML configuration, exposes it as a singleton, and
  shares a process-wide `UnifiedRegistry` plus an `InstanceCreator` that knows
  how to populate that registry.

### 2. Registering configured services
- Configuration blocks placed under `open_ticket_ai.defs` are modelled by the
  `RawOpenTicketAIConfig` schema and describe reusable services with a `use`
  import path and arbitrary keyword arguments.
- During startup `InstanceCreator.create_instances()` walks over each `defs`
  entry, locates the referenced class, instantiates it with the configuration
  mapping, and registers the resulting object inside the shared registry so it
  can be reused later.
- The registry enforces singleton semantics by raising if the same identifier
  is registered twice and exposes `get_instance` to fetch stored services by
  their class name.

### 3. Consuming dependencies inside pipes
- Pipeline definitions reference registered services by identifier. For
  example, the bundled configuration creates an `otobo_znuny` ticket system
  service once and reuses its identifier within downstream pipe definitions to
  link to that adapter.
- When a configurable pipe is constructed, it resolves its dependencies through
  the registry. `FetchTicketsPipe`, `UpdateTicketsPipe`, and
  `AddNoteTicketsPipe` all take the configured ticket-system identifier and call
  `UnifiedRegistry.get_instance` to receive the shared service instance before
  performing their work.

This flow allows integrators to swap or extend services purely through YAML
configuration—new adapters only need to be registered in `defs`, and any pipe
that relies on them can look them up by identifier without importing concrete
classes.
