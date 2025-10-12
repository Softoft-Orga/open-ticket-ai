ddd


´´´mermaid
%%{init:{
  "flowchart":{"defaultRenderer":"elk","htmlLabels":true,"curve":"linear"},
  "themeVariables":{"fontSize":"14px","fontFamily":"system-ui","primaryColor":"#1a1a2e","primaryTextColor":"#e0e0e0","primaryBorderColor":"#4a5568","lineColor":"#718096","background":"#0f0f1a","mainBkg":"#1a1a2e","secondBkg":"#16213e","tertiaryColor":"#0f3460","clusterBkg":"#0a0a15","clusterBorder":"#2d3748","edgeLabelBackground":"#1a1a2e","nodeTextColor":"#e0e0e0"},
  "elk":{"spacing":{"nodeNode":18,"nodeNodeBetweenLayers":16,"componentComponent":12}}
}}%%

flowchart TB

%% ===================== BOOTSTRAP & DI =====================
subgraph BOOT["🚀 Application Bootstrap"]
  direction TB
  Start([Start App]):::start
  LoadEnv["Load .env / Environment"]:::cfg
  CreateDI["Create DI Container<br/>(AppModule)"]:::di
  LoadConfig["ConfigLoader.load_config()"]:::cfg
  ParseYAML["Parse YAML → RawOpenTicketAIConfig"]:::cfg
  SetupLog["Configure Logging<br/>(dictConfig)"]:::cfg
  RegisterServices["Register Services & TemplateRenderer"]:::di
  InitFactory["Initialize RenderableFactory"]:::di
  CreateOrch["Create Orchestrator"]:::di
  
  Start --> LoadEnv --> CreateDI --> LoadConfig --> ParseYAML --> SetupLog
  SetupLog --> RegisterServices --> InitFactory --> CreateOrch
end

%% ===================== ORCHESTRATOR SETUP =====================
subgraph ORCH_SETUP["🎯 Orchestrator Setup"]
  direction TB
  StartOrch["Orchestrator.start()"]:::proc
  LoopRunners{"For each<br/>RunnerDefinition"}:::dec
  CreateRunner["Create PipeRunner<br/>(definition, factory)"]:::proc
  HasTrigger{"Has triggers<br/>(on: [...])?":::dec}
  
  StartOrch --> LoopRunners --> CreateRunner --> HasTrigger
end

%% ===================== TRIGGER SYSTEM =====================
subgraph TRIGGER["⏰ Trigger System (Observer Pattern)"]
  direction TB
  GetOrCreateTrigger["Get/Create Trigger<br/>(IntervalTrigger, etc.)"]:::proc
  AttachRunner["trigger.attach(runner)"]:::proc
  StartTrigger["trigger.start()"]:::proc
  
  GetOrCreateTrigger --> AttachRunner --> StartTrigger
end

subgraph ONETIME["▶️ One-Time Execution"]
  direction TB
  ScheduleTask["asyncio.create_task(<br/>runner.execute())"]:::proc
end

%% ===================== EXECUTION TRIGGER =====================
subgraph EXEC_TRIGGER["⚡ Trigger Fires"]
  direction TB
  TriggerEvent["Trigger fires<br/>(interval/event)"]:::event
  NotifyObservers["trigger.notify()"]:::proc
  CallObserver["runner.on_trigger_fired()"]:::proc
  
  TriggerEvent --> NotifyObservers --> CallObserver
end

%% ===================== RUNNER EXECUTION =====================
subgraph RUNNER["🔄 PipeRunner Execution"]
  direction TB
  RunnerExec["PipeRunner.execute()"]:::proc
  CreatePipeCtx["Create PipeContext<br/>(params from run config)"]:::ctx
  FactoryCreate["factory.create_pipe<br/>(pipe_config, scope)"]:::factory
  RenderParams["Render params with Jinja<br/>(render_base_model)"]:::render
  InstantiatePipe["Instantiate Pipe class"]:::proc
  CallProcess["pipe.process(context)"]:::proc
  
  RunnerExec --> CreatePipeCtx --> FactoryCreate --> RenderParams
  RenderParams --> InstantiatePipe --> CallProcess
end

%% ===================== PIPE PROCESSING =====================
subgraph PIPE_PROC["🔧 Pipe.process() Logic"]
  direction TB
  CheckShould{"should_run?<br/>(if_ condition)"}:::dec
  CheckDeps{"Dependencies met?<br/>(depends_on)"}:::dec
  ProcessAndSave["__process_and_save()"]:::proc
  SkipPipe["Skip → return context"]:::skip
  
  CheckShould -- ✓ --> CheckDeps
  CheckShould -- ✗ --> SkipPipe
  CheckDeps -- ✓ --> ProcessAndSave
  CheckDeps -- ✗ --> SkipPipe
end

%% ===================== PIPE EXECUTION =====================
subgraph PIPE_EXEC["⚙️ Pipe Execution"]
  direction TB
  TryCatch["try-catch wrapper"]:::proc
  IsComposite{"Composite<br/>Pipe?"}:::dec
  
  TryCatch --> IsComposite
end

%% ===================== SIMPLE PIPE =====================
subgraph SIMPLE["📦 Simple Pipe"]
  direction TB
  ExecProcess["await _process()"]:::proc
  CreateResult["Create PipeResult"]:::proc
  
  ExecProcess --> CreateResult
end

%% ===================== COMPOSITE PIPE =====================
subgraph COMPOSITE["🔀 Composite Pipe"]
  direction TB
  LoopSteps{"For each step"}:::dec
  MergeCtx["Merge parent + step params"]:::proc
  BuildChild["factory.create_pipe<br/>(step_config, child_scope)"]:::factory
  RenderStep["Render step params"]:::render
  RunChild["child.process(context)"]:::proc
  CollectResult["Collect result in context"]:::ctx
  AllDone{"All steps<br/>done?"}:::dec
  UnionResults["PipeResult.union(results)"]:::proc
  
  LoopSteps -- Has step --> MergeCtx --> BuildChild --> RenderStep
  RenderStep --> RunChild --> CollectResult --> LoopSteps
  LoopSteps -- Done --> AllDone --> UnionResults
end

%% ===================== RESULT HANDLING =====================
subgraph RESULT["💾 Result Persistence"]
  direction TB
  SaveResult["context.pipes[pipe_id] = result"]:::ctx
  LogResult["Logger.info/warning"]:::log
  ReturnContext["Return updated context"]:::ctx
  
  SaveResult --> LogResult --> ReturnContext
end

%% ===================== ERROR HANDLING =====================
subgraph ERROR["❌ Error Handling"]
  direction TB
  CatchEx["Catch Exception"]:::error
  CreateFailed["Create failed PipeResult<br/>(success=False, failed=True)"]:::error
  LogError["Logger.error + traceback"]:::log
  
  CatchEx --> LogError --> CreateFailed
end

%% ===================== CONNECTIONS =====================
CreateOrch --> StartOrch

HasTrigger -- Yes --> GetOrCreateTrigger
StartTrigger --> TriggerEvent
HasTrigger -- No --> ScheduleTask
ScheduleTask --> RunnerExec

CallObserver --> RunnerExec
CallProcess --> CheckShould
ProcessAndSave --> TryCatch

IsComposite -- No --> ExecProcess
IsComposite -- Yes --> LoopSteps

CreateResult --> SaveResult
UnionResults --> SaveResult
ReturnContext --> LoopRunners

TryCatch --> CatchEx
CreateFailed --> SaveResult

%% ===================== STYLES =====================
classDef start fill:#2d6a4f,stroke:#1b4332,stroke-width:3px,color:#fff,font-weight:bold
classDef cfg fill:#1e3a5f,stroke:#0d1f3d,stroke-width:2px,color:#e0e0e0
classDef di fill:#5a189a,stroke:#3c096c,stroke-width:2px,color:#e0e0e0
classDef proc fill:#2b2d42,stroke:#14213d,stroke-width:2px,color:#e0e0e0
classDef ctx fill:#165b33,stroke:#0d3b24,stroke-width:2px,color:#e0e0e0
classDef dec fill:#d97706,stroke:#b45309,stroke-width:2px,color:#fff,font-weight:bold
classDef factory fill:#7c2d12,stroke:#5c1a0a,stroke-width:2px,color:#e0e0e0
classDef render fill:#4338ca,stroke:#312e81,stroke-width:2px,color:#e0e0e0
classDef event fill:#be123c,stroke:#9f1239,stroke-width:3px,color:#fff,font-weight:bold
classDef skip fill:#374151,stroke:#1f2937,stroke-width:2px,color:#9ca3af
classDef error fill:#dc2626,stroke:#991b1b,stroke-width:2px,color:#fff
classDef log fill:#0891b2,stroke:#0e7490,stroke-width:2px,color:#fff

%% Apply styles
class Start start
class LoadEnv,LoadConfig,ParseYAML,SetupLog cfg
class CreateDI,RegisterServices,InitFactory,CreateOrch di
class StartOrch,CreateRunner,GetOrCreateTrigger,AttachRunner,StartTrigger,ScheduleTask,NotifyObservers,CallObserver,RunnerExec,CreatePipeCtx,InstantiatePipe,CallProcess,ProcessAndSave,TryCatch,ExecProcess,CreateResult,RunChild,CollectResult proc
class CheckShould,CheckDeps,HasTrigger,IsComposite,LoopSteps,AllDone,LoopRunners dec
class FactoryCreate,BuildChild factory
class RenderParams,RenderStep render
class TriggerEvent event
class SkipPipe skip
class CatchEx,CreateFailed error
class LogResult,LogError log
class CreatePipeCtx,MergeCtx,CollectResult,SaveResult,ReturnContext ctx
´´´