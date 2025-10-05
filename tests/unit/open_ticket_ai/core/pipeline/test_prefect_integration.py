from unittest.mock import MagicMock, patch

import pytest

from open_ticket_ai.base.composite_pipe import CompositePipe
from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.pipeline.prefect_flows import (
    create_pipe_task,
    execute_single_pipe_task,
    is_in_prefect_context,
)


class SimplePipe(Pipe):
    async def _process(self) -> PipeResult:
        return PipeResult(success=True, failed=False, data={"value": f"processed_{self.config.id}"})


@pytest.mark.asyncio
async def test_create_pipe_task_creates_task_with_correct_name():
    pipe_task = create_pipe_task("test_pipe", retries=3, retry_delay_seconds=60)

    assert pipe_task is not None
    assert callable(pipe_task)
    assert pipe_task.name == "pipe_test_pipe"


@pytest.mark.asyncio
async def test_execute_single_pipe_task_executes_pipe():
    app_config = {
        "general_config": {},
        "defs": [],
        "orchestrator": [],
    }

    pipe_config = {
        "id": "test_pipe",
        "use": "tests.unit.open_ticket_ai.core.pipeline.test_prefect_integration:SimplePipe",
    }

    context_data = {"pipes": {}, "config": {}}

    result = await execute_single_pipe_task(
        app_config=app_config,
        pipe_config=pipe_config,
        context_data=context_data,
        pipe_id="test_pipe",
        retries=2,
        retry_delay_seconds=30,
    )

    assert "pipes" in result
    assert "test_pipe" in result["pipes"]
    assert result["pipes"]["test_pipe"]["success"] is True
    assert result["pipes"]["test_pipe"]["data"]["value"] == "processed_test_pipe"


@pytest.mark.asyncio
async def test_pipe_retry_configuration_from_config():
    pipe_config = {
        "id": "test_pipe",
        "use": "tests.unit.open_ticket_ai.core.pipeline.test_prefect_integration:SimplePipe",
        "retries": 5,
        "retry_delay_seconds": 120,
    }

    from open_ticket_ai.core.pipeline.pipe_config import RenderedPipeConfig

    rendered_config = RenderedPipeConfig.model_validate(pipe_config)

    assert rendered_config.retries == 5
    assert rendered_config.retry_delay_seconds == 120


@pytest.mark.asyncio
async def test_pipe_retry_configuration_defaults():
    pipe_config = {
        "id": "test_pipe",
        "use": "tests.unit.open_ticket_ai.core.pipeline.test_prefect_integration:SimplePipe",
    }

    from open_ticket_ai.core.pipeline.pipe_config import RenderedPipeConfig

    rendered_config = RenderedPipeConfig.model_validate(pipe_config)

    assert rendered_config.retries == 2
    assert rendered_config.retry_delay_seconds == 30
