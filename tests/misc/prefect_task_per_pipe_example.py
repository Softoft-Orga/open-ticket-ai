"""Example demonstrating task-per-pipe Prefect orchestration."""

import asyncio
import logging
from typing import Any

from prefect import flow

from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.pipeline.prefect_flows import execute_single_pipe_task

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DataFetchPipe(Pipe):
    async def _process(self) -> PipeResult:
        logger.info("Fetching data...")
        return PipeResult(
            success=True,
            failed=False,
            message="Data fetched successfully",
            data={"items": [1, 2, 3, 4, 5]},
        )


class DataProcessPipe(Pipe):
    async def _process(self) -> PipeResult:
        logger.info("Processing data...")
        return PipeResult(
            success=True,
            failed=False,
            message="Data processed successfully",
            data={"processed_count": 5},
        )


class DataStorePipe(Pipe):
    async def _process(self) -> PipeResult:
        logger.info("Storing data...")
        return PipeResult(
            success=True,
            failed=False,
            message="Data stored successfully",
            data={"stored": True},
        )


@flow(name="task_per_pipe_example", log_prints=True)
async def task_per_pipe_example_flow() -> dict[str, Any]:
    """Example flow showing each pipe as a separate Prefect task."""
    logger.info("=" * 70)
    logger.info("Task-per-Pipe Architecture Example")
    logger.info("=" * 70)

    app_config = {
        "general_config": {},
        "defs": [],
        "orchestrator": {"runners": []},
    }

    initial_context = Context(pipes={}, config={})

    logger.info("\n▶ Step 1: Fetch Data (retries: 3, delay: 60s)")
    context_data = await execute_single_pipe_task(
        app_config=app_config,
        pipe_config={
            "id": "fetch_data",
            "use": "tests.misc.prefect_task_per_pipe_example:DataFetchPipe",
        },
        context_data=initial_context.model_dump(),
        pipe_id="fetch_data",
        retries=3,
        retry_delay_seconds=60,
    )

    logger.info("\n▶ Step 2: Process Data (retries: 2, delay: 30s)")
    context_data = await execute_single_pipe_task(
        app_config=app_config,
        pipe_config={
            "id": "process_data",
            "use": "tests.misc.prefect_task_per_pipe_example:DataProcessPipe",
        },
        context_data=context_data,
        pipe_id="process_data",
        retries=2,
        retry_delay_seconds=30,
    )

    logger.info("\n▶ Step 3: Store Data (retries: 5, delay: 45s)")
    context_data = await execute_single_pipe_task(
        app_config=app_config,
        pipe_config={
            "id": "store_data",
            "use": "tests.misc.prefect_task_per_pipe_example:DataStorePipe",
        },
        context_data=context_data,
        pipe_id="store_data",
        retries=5,
        retry_delay_seconds=45,
    )

    final_context = Context(**context_data)

    logger.info("\n" + "=" * 70)
    logger.info("Pipeline Execution Complete!")
    logger.info("=" * 70)

    logger.info("\n📊 Results:")
    for pipe_id, result in final_context.pipes.items():
        logger.info(f"  • {pipe_id}:")
        logger.info(f"    - Success: {result.success}")
        logger.info(f"    - Message: {result.message}")
        logger.info(f"    - Data: {result.data}")

    logger.info("\n✨ Benefits of Task-per-Pipe Architecture:")
    logger.info("  ✓ Each pipe appears as a separate task in Prefect UI")
    logger.info("  ✓ Individual retry configuration per pipe")
    logger.info("  ✓ Granular error isolation and tracking")
    logger.info("  ✓ Better observability and debugging")
    logger.info("  ✓ Per-task metrics and duration tracking")

    logger.info("\n📍 View in Prefect UI:")
    logger.info("  1. Start Prefect server: prefect server start")
    logger.info("  2. Navigate to: http://127.0.0.1:4200")
    logger.info("  3. Look for tasks named: pipe_fetch_data, pipe_process_data, pipe_store_data")

    return context_data


async def main() -> None:
    """Main entry point."""
    logger.info("\n🚀 Running Task-per-Pipe Example...")
    logger.info("This demonstrates how each pipe runs as a separate Prefect task\n")

    result = await task_per_pipe_example_flow()

    logger.info("\n✅ Example completed successfully!")
    logger.info("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
