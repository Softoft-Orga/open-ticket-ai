from __future__ import annotations

import asyncio
import copy

from open_ticket_ai.core.pipeline.configurable_pipe import ConfigurablePipe
from open_ticket_ai.core.pipeline.configurable_pipe_config import (
    OnType,
    RawPipeConfig,
    RenderedPipeConfig,
)
from open_ticket_ai.core.pipeline.context import PipelineContext


class FakeRegistry:
    def __init__(self, mapping: dict[str, type[ConfigurablePipe]]):
        self._mapping = mapping

    def get_class(self, name: str) -> type[ConfigurablePipe]:
        return self._mapping[name]


class TrackingStepPipe(ConfigurablePipe[RawPipeConfig]):
    call_count = 0

    @staticmethod
    def get_raw_config_model_type() -> type[RawPipeConfig]:
        return RawPipeConfig

    async def _process(self) -> dict[str, str]:
        type(self).call_count += 1
        return {"step": self.config.name}


class TrackingMainPipe(ConfigurablePipe[RawPipeConfig]):
    def __init__(self, config: RawPipeConfig, registry: FakeRegistry, result: dict[str, object] | None = None):
        super().__init__(config=config, registry=registry)
        self._result = copy.deepcopy(result) if result is not None else {"status": "ok"}
        self.process_calls = 0

    @staticmethod
    def get_raw_config_model_type() -> type[RawPipeConfig]:
        return RawPipeConfig

    async def _process(self) -> dict[str, object]:
        self.process_calls += 1
        return copy.deepcopy(self._result)


def test_rendered_pipe_config_defaults() -> None:
    rendered = RenderedPipeConfig(use="ExamplePipe", when=True)

    assert rendered.name == "anonymous"
    assert rendered.on_failure is OnType.FAIL_CONTAINER
    assert rendered.on_success is OnType.CONTINUE
    assert rendered.steps == []


def test_raw_pipe_config_renders_to_rendered_model() -> None:
    raw = RawPipeConfig(
        name="{{ config['display_name'] }}",
        use="ExamplePipe",
        when="{{ config['should_run'] }}",
        on_failure="{{ 'finish_container' }}",
        on_success="{{ 'continue' }}",
        steps=[RawPipeConfig(name="child", use="ExamplePipe", when="True")],
    )

    context = PipelineContext(config={"display_name": "MainPipe", "should_run": True})

    rendered = raw.render(context)

    assert isinstance(rendered, RenderedPipeConfig)
    assert rendered.name == "MainPipe"
    assert rendered.when is True
    assert rendered.on_failure is OnType.FINISH_CONTAINER
    assert rendered.on_success is OnType.CONTINUE
    assert rendered.steps[0].use == "ExamplePipe"


def test_pipeline_context_has_distinct_defaults() -> None:
    first = PipelineContext()
    second = PipelineContext()

    first.pipes["a"] = {"value": 1}
    first.config["threshold"] = 10

    assert "a" not in second.pipes
    assert "threshold" not in second.config


def test_base_pipe_process_runs_steps_and_updates_context() -> None:
    TrackingStepPipe.call_count = 0
    registry = FakeRegistry({"TrackingStepPipe": TrackingStepPipe})

    step_config = RawPipeConfig(name="child", use="TrackingStepPipe", when="True")
    main_config = RawPipeConfig(name="parent", use="TrackingMainPipe", when="True", steps=[step_config])

    pipe = TrackingMainPipe(config=main_config, registry=registry, result={"outcome": "success"})

    input_context = PipelineContext()
    result_context = asyncio.run(pipe.process(input_context))

    assert TrackingStepPipe.call_count == 1
    assert pipe.process_calls == 1
    assert result_context is input_context
    assert result_context.pipes["child"] == {"step": "child"}
    assert result_context.pipes["parent"] == {"outcome": "success"}


def test_base_pipe_process_skips_when_condition_false() -> None:
    registry = FakeRegistry({})
    pipe = TrackingMainPipe(
        config=RawPipeConfig(name="skipped", use="TrackingMainPipe", when="False"),
        registry=registry,
    )

    original_context = PipelineContext(pipes={"existing": {"value": 42}})
    result_context = asyncio.run(pipe.process(original_context))

    assert pipe.process_calls == 0
    assert result_context is original_context
    assert result_context.pipes == {"existing": {"value": 42}}
