import importlib
from typing import Any

import pytest

from open_ticket_ai.base.pipes.composite_pipe import CompositePipe
from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import CompositePipeResultData, PipeConfig, PipeResult
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig


class DummyChildPipe(Pipe):
    processed_contexts: list[PipeContext] = []
    process_count: int = 0

    async def process(self, context: PipeContext) -> PipeContext:
        self.__class__.processed_contexts.append(context)
        return await super().process(context)

    async def _process(self) -> PipeResult:
        self.__class__.process_count += 1
        return PipeResult(success=True, failed=False, data=CompositePipeResultData(value=self.pipe_config.id))


class DummyParentPipe(CompositePipe):
    async def _process(self) -> PipeResult:
        context = self._context
        if context is None:
            return PipeResult(success=False, failed=True, data=CompositePipeResultData(message="No context"))
        return PipeResult(
            success=True,
            failed=False,
            data=CompositePipeResultData(
                child_names=list(context.pipes.keys()),
                context_id=id(context),
            ),
        )


class SkipPipe(Pipe):
    executed: bool = False

    async def _process(self) -> PipeResult:
        self.__class__.executed = True
        return PipeResult(success=True, failed=False, data=CompositePipeResultData(value="should not run"))


@pytest.fixture(autouse=True)
def reset_dummy_pipes() -> None:
    DummyChildPipe.processed_contexts = []
    DummyChildPipe.process_count = 0
    SkipPipe.executed = False


@pytest.fixture
def resolve_step_imports(monkeypatch: pytest.MonkeyPatch, logger_factory: LoggerFactory) -> None:
    jinja_renderer = JinjaRenderer(JinjaRendererConfig(), logger_factory)

    def _resolve_class(import_path: str) -> type:
        module_path, separator, attr_name = import_path.partition(":")
        if not separator:
            module_path, _, attr_name = import_path.rpartition(".")
        module = importlib.import_module(module_path)
        return getattr(module, attr_name)  # type: ignore[no-any-return]

    def _build_pipe_from_step_config(self: Any, step_config: dict[str, Any], context: PipeContext) -> Any:
        rendered_step_config = jinja_renderer.render_recursive(step_config, context)
        resolved_config = dict(rendered_step_config)
        use_value = resolved_config.get("use")
        if use_value is None:
            raise ValueError("use value is required")
        pipe_class = _resolve_class(use_value) if isinstance(use_value, str) else use_value
        return pipe_class(resolved_config)

    monkeypatch.setattr(
        CompositePipe,
        "_build_pipe_from_step_config",
        _build_pipe_from_step_config,
        raising=False,
    )


@pytest.mark.asyncio
async def test_process_skips_pipe_when_condition_is_false(logger_factory: LoggerFactory) -> None:
    context = PipeContext(
        pipes={"existing": PipeResult(success=True, failed=False, data=CompositePipeResultData(value=1))}
    )
    skip_config: PipeConfig = PipeConfig(id="skip", use="SkipPipe", **{"if": False})
    skip_pipe = SkipPipe(skip_config, logger_factory)

    result_context = await skip_pipe.process(context)

    assert result_context is context
    assert "skip" not in context.pipes
    assert SkipPipe.executed is False
