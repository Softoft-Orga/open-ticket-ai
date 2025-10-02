"""Simple test to verify Prefect installation without using decorators."""

import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_prefect_import() -> None:
    """Test that Prefect can be imported."""
    try:
        import prefect
        logger.info("✓ Prefect imported successfully: version %s", prefect.__version__)
        
        from prefect.client.orchestration import get_client
        logger.info("✓ Prefect client available")
        
        from prefect.deployments.runner import deploy
        logger.info("✓ Prefect deployment tools available")
        
        logger.info("\n✓ Prefect is correctly installed!")
        logger.info("\nNext steps:")
        logger.info("1. The PrefectOrchestrator integration is ready in:")
        logger.info("   src/open_ticket_ai/core/pipeline/prefect_orchestrator.py")
        logger.info("2. Prefect flows are defined in:")
        logger.info("   src/open_ticket_ai/core/pipeline/prefect_flows.py")
        logger.info("3. Start Prefect server: prefect server start")
        logger.info("4. Access UI at: http://127.0.0.1:4200")
        
    except ImportError as e:
        logger.error("✗ Failed to import Prefect: %s", e)
        raise
    except Exception as e:
        logger.error("✗ Error during Prefect verification: %s", e)
        raise


if __name__ == "__main__":
    asyncio.run(test_prefect_import())
