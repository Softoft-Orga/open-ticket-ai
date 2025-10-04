"""Working example of Prefect integration with open-ticket-ai."""

import asyncio
import logging

from prefect import Flow, Task

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def simple_task_logic(message: str) -> str:
    """Core logic for a simple task."""
    logger.info("Executing task with message: %s", message)
    return f"Processed: {message}"


def simple_flow_logic(name: str = "World") -> str:
    """Core logic for a simple flow."""
    logger.info("Starting flow")

    # Create tasks imperatively
    task1 = Task(fn=simple_task_logic, name="simple_task_1")
    task2 = Task(fn=simple_task_logic, name="simple_task_2")

    # Execute tasks
    result1 = task1(f"Hello, {name}!")
    result2 = task2("Prefect is working!")

    logger.info("Flow completed successfully")
    return f"{result1} | {result2}"


# Create flow imperatively (avoids Pydantic 2.11.x compatibility issue with decorators)
simple_flow = Flow(fn=simple_flow_logic, name="simple_flow")


async def test_basic_prefect() -> None:
    """Test basic Prefect functionality."""
    logger.info("=" * 60)
    logger.info("Testing Prefect Integration")
    logger.info("=" * 60)

    # Import Prefect modules
    import prefect
    logger.info("✓ Prefect version: %s", prefect.__version__)

    # Run a simple flow
    result = simple_flow(name="open-ticket-ai")
    logger.info("✓ Flow result: %s", result)

    logger.info("=" * 60)
    logger.info("✓ Prefect is working correctly!")
    logger.info("=" * 60)


async def demonstrate_integration() -> None:
    """Demonstrate the open-ticket-ai Prefect integration."""
    logger.info("\n" + "=" * 60)
    logger.info("Open-Ticket-AI Prefect Integration")
    logger.info("=" * 60)

    logger.info("\n✓ Integration components created:")
    logger.info("  1. src/open_ticket_ai/core/pipeline/prefect_flows.py")
    logger.info("     - execute_pipe_task: Runs pipes with retry logic")
    logger.info("     - execute_scheduled_pipe_flow: Flow wrapper for pipelines")

    logger.info("\n  2. src/open_ticket_ai/core/pipeline/prefect_orchestrator.py")
    logger.info("     - PrefectOrchestrator: Manages scheduled pipe execution")
    logger.info("     - Methods: start(), stop(), run(), run_once(pipe_id)")

    logger.info("\n✓ Usage:")
    logger.info("  # Via dependency injection")
    logger.info("  orchestrator = injector.get(PrefectOrchestrator)")
    logger.info("  await orchestrator.run()")

    logger.info("\n✓ Start Prefect server:")
    logger.info("  prefect server start")
    logger.info("  UI: http://127.0.0.1:4200")

    logger.info("\n" + "=" * 60)


async def main() -> None:
    """Main entry point."""
    await test_basic_prefect()
    await demonstrate_integration()


if __name__ == "__main__":
    asyncio.run(main())
