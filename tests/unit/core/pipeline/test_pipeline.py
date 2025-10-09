import importlib
from typing import Any

import pytest

from open_ticket_ai.base.composite_pipe import CompositePipe
from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.template_rendering.jinja_renderer import JinjaRenderer


class DummyChildPipe(Pipe):
    processed_contexts: list[Context] = []
    process_count: int = 0

    async def process(self, context: Context) -> Context:  # type: ignore[override]
        self.__class__.processed_contexts.append(context)
        return await super().process(context)

    async def _process(self) -> PipeResult:
        self.__class__.process_count += 1
        return PipeResult(success=True, failed=False, data={"value": self.config.id})


class DummyParentPipe(CompositePipe):
    async def _process(self) -> PipeResult:
        return PipeResult(
            success=True,
            failed=False,
            data={
                "child_names": list(self._current_context.pipes.keys()),
                "context_id": id(self._current_context),
            },
        )


class SkipPipe(Pipe):
    executed: bool = False

    async def _process(self) -> PipeResult:
        self.__class__.executed = True
        return PipeResult(success=True, failed=False, data={"value": "should not run"})


@pytest.fixture(autouse=True)
def reset_dummy_pipes() -> None:
    DummyChildPipe.processed_contexts = []
    DummyChildPipe.process_count = 0
    SkipPipe.executed = False


@pytest.fixture
def resolve_step_imports(monkeypatch: pytest.MonkeyPatch) -> None:
    from open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig

    jinja_renderer = JinjaRenderer(JinjaRendererConfig())

    def _resolve_class(import_path: str):
        module_path, separator, attr_name = import_path.partition(":")
        if not separator:
            module_path, _, attr_name = import_path.rpartition(".")
        module = importlib.import_module(module_path)
        return getattr(module, attr_name)

    def _build_pipe_from_step_config(self, step_config: dict[str, Any], context: Context):
        rendered_step_config = jinja_renderer.render_recursive(step_config, context)
        resolved_config = dict(rendered_step_config)
        use_value = resolved_config.get("use")
        pipe_class = _resolve_class(use_value) if isinstance(use_value, str) else use_value
        return pipe_class(resolved_config)

    monkeypatch.setattr(
        CompositePipe,
        "_build_pipe_from_step_config",
        _build_pipe_from_step_config,
        raising=False,
    )


@pytest.mark.asyncio
async def test_process_skips_pipe_when_condition_is_false():
    context = Context(pipes={"existing": PipeResult(success=True, failed=False, data={"value": 1})})
    skip_pipe = SkipPipe({"id": "skip", "use": "SkipPipe", "if": False})

    result_context = await skip_pipe.process(context)

    assert result_context is context
    assert "skip" not in context.pipes
    assert SkipPipe.executed is False
