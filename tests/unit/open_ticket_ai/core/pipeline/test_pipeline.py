import importlib
from typing import Any

import pytest

from open_ticket_ai.core.config import jinja2_env
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.pipeline.pipe_config import PipeResult


class DummyChildPipe(Pipe):
    processed_contexts: list[Context] = []
    process_count: int = 0

    async def process(self, context: Context) -> Context:  # type: ignore[override]
        self.__class__.processed_contexts.append(context)
        return await super().process(context)

    async def _process(self) -> dict[str, Any]:
        self.__class__.process_count += 1
        return {"value": self.config.name}


class DummyParentPipe(Pipe):
    async def _process(self) -> dict[str, Any]:
        return {
            "child_names": list(self._current_context.pipes.keys()),
            "context_id": id(self._current_context),
        }


class SkipPipe(Pipe):
    executed: bool = False

    async def _process(self) -> dict[str, Any]:
        self.__class__.executed = True
        return {"value": "should not run"}


@pytest.fixture(autouse=True)
def reset_dummy_pipes() -> None:
    DummyChildPipe.processed_contexts = []
    DummyChildPipe.process_count = 0
    SkipPipe.executed = False


@pytest.fixture
def resolve_step_imports(monkeypatch: pytest.MonkeyPatch) -> None:
    def _resolve_class(import_path: str):
        module_path, separator, attr_name = import_path.partition(":")
        if not separator:
            module_path, _, attr_name = import_path.rpartition(".")
        module = importlib.import_module(module_path)
        return getattr(module, attr_name)

    def _build_pipe_from_step_config(self, step_config: dict[str, Any], context: Context):
        rendered_step_config = jinja2_env.render_recursive(step_config, context)
        resolved_config = dict(rendered_step_config)
        use_value = resolved_config.get("use")
        if isinstance(use_value, str):
            resolved_config["use"] = _resolve_class(use_value)
        pipe_class = resolved_config["use"]
        return pipe_class(resolved_config)

    monkeypatch.setattr(
        Pipe,
        "_build_pipe_from_step_config",
        _build_pipe_from_step_config,
        raising=False,
    )


@pytest.mark.asyncio
async def test_process_executes_child_pipes_and_updates_context(resolve_step_imports):
    context = Context(pipes={}, config={})
    parent_pipe = DummyParentPipe(
        {
            "name": "parent",
            "steps": [
                {
                    "name": "child",
                    "use": f"{__name__}:DummyChildPipe",
                }
            ],
        }
    )

    result_context = await parent_pipe.process(context)

    assert result_context is context
    assert DummyChildPipe.processed_contexts == [context]
    assert DummyChildPipe.process_count == 1

    child_state = result_context.pipes["child"]
    assert child_state.success is True
    assert child_state.failed is False
    assert child_state.data == {"value": "child"}

    parent_state = result_context.pipes["parent"]
    assert parent_state.success is True
    assert parent_state.failed is False
    assert parent_state.data["child_names"] == ["child"]
    assert parent_state.data["context_id"] == id(context)


@pytest.mark.asyncio
async def test_process_skips_pipe_when_condition_is_false():
    context = Context(
        pipes={
            "existing": PipeResult(success=True, failed=False, data={"value": 1})
        },
        config={},
    )
    skip_pipe = SkipPipe({"name": "skip", "when": False})

    result_context = await skip_pipe.process(context)

    assert result_context is context
    assert "skip" not in context.pipes
    assert not SkipPipe.executed


class FailingPipe(Pipe):
    async def _process(self) -> dict[str, Any]:
        raise RuntimeError("expected failure")


@pytest.mark.asyncio
async def test_process_records_failure_state():
    context = Context(pipes={}, config={})
    failing_pipe = FailingPipe({"name": "fail"})

    result_context = await failing_pipe.process(context)

    failure_state = result_context.pipes["fail"]
    assert failure_state.success is False
    assert failure_state.failed is True
    assert "expected failure" in failure_state.message
