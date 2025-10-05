# Task-per-Pipe Prefect Architecture - Implementation Summary

## Overview

This implementation refactors the OpenTicketAI pipeline execution so that **each Pipe runs as an individual Prefect task**, providing improved observability, granular retries, better error isolation, and enabling future parallelization.

## Changes Made

### Core Implementation (5 files modified)

#### 1. `src/open_ticket_ai/core/pipeline/prefect_flows.py`
**New Functions:**
- `is_in_prefect_context()` - Detects if code is running within a Prefect task context
- `create_pipe_task(pipe_id, retries, retry_delay_seconds)` - Factory function that creates dynamically-named Prefect tasks
- `execute_single_pipe_task(...)` - Executes a single pipe as a Prefect task with configurable retry behavior

**Modified Functions:**
- `execute_pipe_task()` - Now delegates to `execute_single_pipe_task` with retry settings from pipe config

**Key Features:**
- Dynamic task naming: Each pipe gets a unique task name `pipe_{pipe_id}` in Prefect UI
- Per-pipe retry configuration
- Backward compatible with existing code

#### 2. `src/open_ticket_ai/base/composite_pipe.py`
**Changes:**
- Added `_app_config` storage in `__init__`
- Modified `_process_steps()` to detect Prefect context and dispatch steps as separate tasks
- When in Prefect context: calls `execute_single_pipe_task` for each step
- When not in Prefect context: uses traditional synchronous execution
- Passes retry configuration from pipe config to task execution
- Fixed context flow to use `_current_context` instead of creating a new one

#### 3. `src/open_ticket_ai/core/pipeline/pipe.py`
**Changes:**
- Added `_app_config` parameter storage in `__init__` for use by composite pipes

#### 4. `src/open_ticket_ai/core/pipeline/pipe_factory.py`
**Changes:**
- Modified `create_registerable_instance()` to pass `app_config` to all pipes via kwargs

#### 5. `src/open_ticket_ai/core/pipeline/pipe_config.py`
**Changes:**
- Added `retries: int = Field(default=2)` to `RenderedPipeConfig`
- Added `retry_delay_seconds: int = Field(default=30)` to `RenderedPipeConfig`

### Documentation (3 files updated)

#### 1. `docs/PREFECT_SETUP.md`
- Added task-per-pipe architecture explanation
- Updated integration components section
- Added configuration examples with retry settings

#### 2. `docs/PREFECT_USAGE.md`
- Added task-per-pipe architecture section with benefits
- Updated configuration examples
- Enhanced API reference with new functions
- Added retry configuration examples

#### 3. `docs/vitepress_docs/docs_src/en/developers/pipeline.md`
- Added new "Prefect Orchestration" section
- Documented retry configuration fields
- Provided configuration examples
- Explained benefits and use cases

### Testing (2 new test files)

#### 1. `tests/unit/open_ticket_ai/core/pipeline/test_prefect_integration.py`
Comprehensive test suite covering:
- Prefect context detection
- Task creation with correct naming
- Single pipe task execution
- Composite pipe task orchestration
- Retry configuration (custom and default values)

#### 2. `tests/misc/prefect_task_per_pipe_example.py`
Working example demonstrating:
- Multiple pipes as separate Prefect tasks
- Different retry configurations per pipe
- Context flow between pipes
- Results tracking
- How to view tasks in Prefect UI

## Architecture Benefits

### Before (Old Architecture)
```
execute_pipe_task
└── Entire pipeline execution as ONE task
    ├── Step 1
    ├── Step 2
    └── Step 3
```

**Drawbacks:**
- All steps shown as one task in Prefect UI
- Retry applies to entire pipeline
- No visibility into individual step status
- Difficult to identify which step failed

### After (New Architecture)
```
execute_scheduled_pipe_flow
├── pipe_fetch_data (task with retries: 3)
├── pipe_process_data (task with retries: 2)
└── pipe_store_data (task with retries: 5)
```

**Benefits:**
- ✅ Each pipe visible as separate task in Prefect UI
- ✅ Individual retry configuration per pipe
- ✅ Granular error isolation and tracking
- ✅ Per-pipe metrics and duration
- ✅ Better debugging experience
- ✅ Ready for parallel execution (future enhancement)

## Usage

### YAML Configuration
```yaml
orchestrator:
  runners:
    - pipe_id: data_pipeline
      pipe:
        use: CompositePipe
        steps:
          - id: fetch
            use: FetchData
            retries: 5  # Critical step gets more retries
            retry_delay_seconds: 120
          
          - id: process
            use: ProcessData
            retries: 2  # Standard retry
            
          - id: store
            use: StoreData
            retries: 3
            retry_delay_seconds: 60
```

### Python Code
```python
from open_ticket_ai.core.pipeline import execute_single_pipe_task

# Execute a pipe as a Prefect task
result = await execute_single_pipe_task(
    app_config=app_config,
    pipe_config=pipe_config,
    context_data=context_data,
    pipe_id="my_pipe",
    retries=3,
    retry_delay_seconds=60,
)
```

## Backward Compatibility

The implementation is **fully backward compatible**:

1. **Non-Prefect contexts**: Pipes execute normally without Prefect overhead
2. **Existing code**: No changes required to existing pipe implementations
3. **Configuration**: Retry fields are optional with sensible defaults
4. **Orchestrators**: Both `Orchestrator` (APScheduler) and `PrefectOrchestrator` supported

## Future Enhancements

This architecture enables:
- **Parallel execution**: Independent pipes can run concurrently
- **Dynamic dependencies**: Build dependency graphs at runtime
- **Custom retry strategies**: Different strategies per pipe type
- **Conditional execution**: More sophisticated `if` conditions based on task results

## Verification

To verify the implementation in Prefect UI:

1. Start Prefect server:
   ```bash
   prefect server start
   ```

2. Run the example:
   ```bash
   python tests/misc/prefect_task_per_pipe_example.py
   ```

3. Open Prefect UI at http://127.0.0.1:4200

4. Look for tasks named:
   - `pipe_fetch_data`
   - `pipe_process_data`
   - `pipe_store_data`

Each will appear as a separate task with its own:
- Status (success/failed)
- Duration
- Retry count
- Logs
- Error details (if failed)

## Files Changed Summary

- **Source files modified**: 5
- **Documentation files updated**: 3
- **New test files**: 2
- **Total lines added**: ~513
- **Total lines changed**: ~19 (minimal modifications to existing code)

All changes follow the principle of **minimal modification** while achieving full functionality.
