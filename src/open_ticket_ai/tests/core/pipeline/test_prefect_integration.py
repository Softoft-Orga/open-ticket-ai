from unittest.mock import MagicMock, patch

import pytest

from open_ticket_ai.open_ticket_ai.base.composite_pipe import CompositePipe
from open_ticket_ai.open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.open_ticket_ai.core.pipeline import (
    create_pipe_task,
    execute_single_pipe_task,
    is_in_prefect_context,
)


class SimplePipe(Pipe):
    async def _process(self) -> PipeResult:
        return PipeResult(success=True, failed=False, data={"value": f"processed_{self.config.id}"})


@pytest.mark.asyncio
async def test_is_in_prefect_context_returns_false_outside_prefect():
    assert is_in_prefect_context() is False


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
        "orchestrator": {"runners": []},
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
async def test_composite_pipe_uses_prefect_tasks_when_in_context():
    with patch("open_ticket_ai.core.pipeline.prefect_flows.is_in_prefect_context", return_value=True):
        app_config = {
            "general_config": {},
            "defs": [],
            "orchestrator": {"runners": []},
        }

        composite_config = {
            "id": "composite",
            "use": "open_ticket_ai.base.composite_pipe:CompositePipe",
            "steps": [
                {
                    "id": "step1",
                    "use": "tests.unit.open_ticket_ai.core.pipeline.test_prefect_integration:SimplePipe",
                },
                {
                    "id": "step2",
                    "use": "tests.unit.open_ticket_ai.core.pipeline.test_prefect_integration:SimplePipe",
                },
            ],
        }

        factory = MagicMock()

        async def mock_create_pipe(parent_config, pipe_config, scope):
            pipe_id = pipe_config["id"]
            mock_pipe = MagicMock(spec=Pipe)
            mock_pipe.config = MagicMock(id=pipe_id)

            async def mock_process(context):
                result = PipeResult(success=True, failed=False, data={"value": f"processed_{pipe_id}"})
                context.pipes[pipe_id] = result
                return context

            mock_pipe.process = mock_process
            return mock_pipe

        factory.create_pipe = mock_create_pipe

        composite_pipe = CompositePipe(composite_config, factory=factory, app_config=app_config)
        context = Context(pipes={}, config=composite_config)

        with patch("open_ticket_ai.base.composite_pipe.execute_single_pipe_task") as mock_execute:

            async def mock_execute_task(
                app_config, pipe_config, context_data, pipe_id, retries=2, retry_delay_seconds=30
            ):
                ctx = Context(**context_data)
                result = PipeResult(success=True, failed=False, data={"value": f"processed_{pipe_id}"})
                ctx.pipes[pipe_id] = result
                return ctx.model_dump()

            mock_execute.side_effect = mock_execute_task

            result_context = await composite_pipe.process(context)

            assert mock_execute.call_count == 2
            assert "step1" in result_context.pipes
            assert "step2" in result_context.pipes


@pytest.mark.asyncio
async def test_pipe_retry_configuration_from_config():
    pipe_config = {
        "id": "test_pipe",
        "use": "tests.unit.open_ticket_ai.core.pipeline.test_prefect_integration:SimplePipe",
        "retries": 5,
        "retry_delay_seconds": 120,
    }

    from open_ticket_ai.open_ticket_ai.core.pipeline.pipe_config import RenderedPipeConfig

    rendered_config = RenderedPipeConfig.model_validate(pipe_config)

    assert rendered_config.retries == 5
    assert rendered_config.retry_delay_seconds == 120


@pytest.mark.asyncio
async def test_pipe_retry_configuration_defaults():
    pipe_config = {
        "id": "test_pipe",
        "use": "tests.unit.open_ticket_ai.core.pipeline.test_prefect_integration:SimplePipe",
    }

    from open_ticket_ai.open_ticket_ai.core.pipeline.pipe_config import RenderedPipeConfig

    rendered_config = RenderedPipeConfig.model_validate(pipe_config)

    assert rendered_config.retries == 2
    assert rendered_config.retry_delay_seconds == 30
