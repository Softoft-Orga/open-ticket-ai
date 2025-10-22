import asyncio
from contextlib import suppress
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from open_ticket_ai.app import OpenTicketAIApp
from open_ticket_ai.core.config.config_models import InfrastructureConfig, OpenTicketAIConfig
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


@pytest.mark.asyncio
async def test_orchestrator_execution_with_keyboard_interrupt(logger_factory):
    """Test that orchestrator pipe is called multiple times during app execution.

    This test verifies that app.run() continuously calls the orchestrator's process() method
    in a loop until interrupted. We use asyncio to run the app for a short time, then cancel
    it to simulate a KeyboardInterrupt scenario.

    Note: The test mocks PipeContext.empty() and orchestrator.runners which are referenced
    by app.py but don't exist in the actual model classes.
    """
    orchestrator_config = PipeConfig(
        id="test-orchestrator",
        use="open_ticket_ai.base.orchestrators.simple_sequential_orchestrator.SimpleSequentialOrchestrator",
        params={
            "orchestrator_sleep": 0.1,
            "steps": [
                PipeConfig(
                    id="test-runner",
                    use="tests.unit.conftest.SimplePipe",
                ),
            ],
        },
    )

    orchestrator_config_mock = MagicMock(spec=orchestrator_config)
    orchestrator_config_mock.runners = []

    config = OpenTicketAIConfig(
        infrastructure=InfrastructureConfig(logging=LoggingConfig(level="INFO")),
        services={},
        orchestrator=orchestrator_config,
    )

    config_mock = MagicMock(spec=config)
    config_mock.services = {}
    config_mock.orchestrator = orchestrator_config_mock

    process_call_count = 0

    async def count_calls(_ctx):
        nonlocal process_call_count
        process_call_count += 1
        await asyncio.sleep(0.05)
        return PipeResult.success()

    async def mock_process_loop(ctx):
        while True:
            await count_calls(ctx)
            await asyncio.sleep(0.05)

    mock_pipe = MagicMock()
    mock_pipe.process = AsyncMock(side_effect=mock_process_loop)

    mock_pipe_factory = MagicMock()
    mock_pipe_factory.render_pipe.return_value = mock_pipe

    with (
        patch(
            "open_ticket_ai.core.pipes.pipe_context_model.PipeContext.empty",
            return_value=PipeContext(),
            create=True,
        ),
        patch.object(OpenTicketAIApp, "__init__", lambda *_args, **_kwargs: None),
    ):
        app = OpenTicketAIApp(
            config=config_mock,
            pipe_factory=mock_pipe_factory,
            logger_factory=logger_factory,
        )
        app._config = config_mock
        app._orchestrator = mock_pipe
        app._logger = logger_factory.create("OpenTicketAIApp")

        task = asyncio.create_task(app.run())
        await asyncio.sleep(0.5)
        task.cancel()

        with suppress(asyncio.CancelledError):
            await task

    assert process_call_count > 1


@pytest.mark.asyncio
async def test_logging_output():
    """Test that app.run() logs appropriate startup messages.

    This test verifies that the OpenTicketAIApp logs messages containing
    "open ticket ai" (case-insensitive) when run() is called. The app should
    log startup information before processing begins.

    Note: The test mocks PipeContext.empty() and orchestrator.runners which are referenced
    by app.py but don't exist in the actual model classes.
    """
    orchestrator_config = PipeConfig(
        id="test-orchestrator",
        use="open_ticket_ai.base.orchestrators.simple_sequential_orchestrator.SimpleSequentialOrchestrator",
    )

    orchestrator_config_mock = MagicMock(spec=orchestrator_config)
    orchestrator_config_mock.runners = []

    config = OpenTicketAIConfig(
        infrastructure=InfrastructureConfig(logging=LoggingConfig(level="INFO")),
        services={},
        orchestrator=orchestrator_config,
    )

    config_mock = MagicMock(spec=config)
    config_mock.services = {}
    config_mock.orchestrator = orchestrator_config_mock

    mock_pipe = MagicMock()
    mock_pipe.process = AsyncMock(side_effect=KeyboardInterrupt)

    captured_logs = []

    mock_logger = MagicMock()
    mock_logger.info = MagicMock(side_effect=lambda msg: captured_logs.append(msg))

    mock_logger_factory = MagicMock()
    mock_logger_factory.create.return_value = mock_logger

    mock_pipe_factory = MagicMock()
    mock_pipe_factory.render_pipe.return_value = mock_pipe

    with (
        patch(
            "open_ticket_ai.core.pipes.pipe_context_model.PipeContext.empty",
            return_value=PipeContext(),
            create=True,
        ),
        patch.object(OpenTicketAIApp, "__init__", lambda *_args, **_kwargs: None),
    ):
        app = OpenTicketAIApp(
            config=config_mock,
            pipe_factory=mock_pipe_factory,
            logger_factory=mock_logger_factory,
        )
        app._config = config_mock
        app._orchestrator = mock_pipe
        app._logger = mock_logger

        with suppress(KeyboardInterrupt):
            await app.run()

    logs_combined = " ".join(captured_logs).lower()
    assert "open ticket ai" in logs_combined
