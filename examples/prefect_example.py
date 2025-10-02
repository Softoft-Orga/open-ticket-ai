"""Example script demonstrating Prefect integration with open-ticket-ai pipelines."""

import asyncio
import logging
from pathlib import Path

from prefect import flow, task

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@task(name="simple_task", retries=1)
def simple_task(message: str) -> str:
    """A simple Prefect task for testing."""
    logger.info("Executing simple task with message: %s", message)
    return f"Processed: {message}"


@flow(name="simple_flow", log_prints=True)
def simple_flow(name: str = "World") -> str:
    """A simple Prefect flow for testing the installation."""
    logger.info("Starting simple flow")
    
    result1 = simple_task(f"Hello, {name}!")
    result2 = simple_task("Prefect is working!")
    
    logger.info("Flow completed successfully")
    return f"{result1} | {result2}"


async def test_prefect_installation() -> None:
    """Test that Prefect is properly installed."""
    logger.info("=" * 60)
    logger.info("Testing Prefect Installation")
    logger.info("=" * 60)
    
    # Run a simple flow
    result = simple_flow(name="open-ticket-ai")
    logger.info("Flow result: %s", result)
    
    logger.info("=" * 60)
    logger.info("✓ Prefect installation test completed successfully!")
    logger.info("=" * 60)


async def demonstrate_prefect_orchestrator() -> None:
    """Demonstrate the PrefectOrchestrator with a minimal example.
    
    Note: This requires a proper config.yml with orchestrator configuration.
    """
    logger.info("=" * 60)
    logger.info("Demonstrating PrefectOrchestrator")
    logger.info("=" * 60)
    
    # This would require proper dependency injection setup
    # For now, just show the concept
    logger.info("To use PrefectOrchestrator:")
    logger.info("1. Configure your orchestrator in config.yml")
    logger.info("2. Inject PrefectOrchestrator via dependency injection")
    logger.info("3. Call await orchestrator.run() to start serving deployments")
    logger.info("4. Or call await orchestrator.run_once(pipe_id) for one-time execution")
    
    logger.info("=" * 60)


async def main() -> None:
    """Main entry point for the example script."""
    # Test basic Prefect functionality
    await test_prefect_installation()
    
    # Show how to use with open-ticket-ai
    await demonstrate_prefect_orchestrator()
    
    logger.info("\nNext steps:")
    logger.info("1. Start Prefect server: prefect server start")
    logger.info("2. Access UI at: http://127.0.0.1:4200")
    logger.info("3. Use PrefectOrchestrator in your application")


if __name__ == "__main__":
    asyncio.run(main())
