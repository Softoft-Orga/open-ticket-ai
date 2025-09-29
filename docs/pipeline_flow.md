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
