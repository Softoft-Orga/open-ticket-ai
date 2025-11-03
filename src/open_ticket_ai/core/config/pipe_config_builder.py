from __future__ import annotations

import uuid
from collections.abc import Iterable, Sequence
from datetime import timedelta
from typing import Any

from otai_base.base_plugin import BasePlugin
from otai_base.pipes.composite_pipe import CompositePipe
from otai_base.pipes.interval_trigger_pipe import IntervalTrigger
from otai_base.pipes.pipe_runners.simple_sequential_runner import SimpleSequentialRunner
from open_ticket_ai.core.pipes.pipe_models import PipeConfig


class PipeConfigFactory:
    """Factory for constructing pipe-related ``PipeConfig`` instances."""

    def create_pipe(
        self,
        pipe_id: str,
        use: str,
        *,
        params: dict[str, Any] | None = None,
        injects: dict[str, str] | None = None,
    ) -> PipeConfig:
        return PipeConfig(
            id=pipe_id,
            use=use,
            params=params or {},
            injects=injects or {},
        )

    def create_composite_builder(
        self,
        pipe_id: str,
        use: str | None = None,
        *,
        params: dict[str, Any] | None = None,
        injects: dict[str, str] | None = None,
        steps: Sequence[PipeConfig] | None = None,
    ) -> PipeConfigBuilder:
        builder = PipeConfigBuilder(
            factory=self,
            pipe_id=pipe_id,
            use=use or BasePlugin().get_registry_name(CompositePipe),
            params=params,
            injects=injects,
        )
        if steps:
            builder.add_steps(steps)
        return builder

    def create_composite_pipe(
        self,
        pipe_id: str,
        steps: Sequence[PipeConfig],
        *,
        params: dict[str, Any] | None = None,
        injects: dict[str, str] | None = None,
    ) -> PipeConfig:
        return self.create_composite_builder(
            pipe_id,
            params=params,
            injects=injects,
            steps=steps,
        ).build()

    def create_interval_trigger(
        self,
        *,
        trigger_id: str = "interval_trigger",
        interval: timedelta,
        params: dict[str, Any] | None = None,
    ) -> PipeConfig:
        trigger_params = dict(params or {})
        trigger_params.setdefault("interval", interval)
        return self.create_pipe(trigger_id, BasePlugin().get_registry_name(IntervalTrigger), params=trigger_params)

    def create_simple_sequential_runner(
        self,
        *,
        runner_id: str,
        on: PipeConfig,
        run: PipeConfig,
        params: dict[str, Any] | None = None,
        injects: dict[str, str] | None = None,
    ) -> PipeConfig:
        runner_params = dict(params or {})
        runner_params["on"] = on.model_dump(mode="json", exclude_none=True)
        runner_params["run"] = run.model_dump(mode="json", exclude_none=True)
        return self.create_pipe(
            runner_id,
            BasePlugin().get_registry_name(SimpleSequentialRunner),
            params=runner_params,
            injects=injects,
        )


class PipeConfigBuilder:
    """Builder that accumulates steps for composite pipes."""

    def __init__(
        self,
        *,
        factory: PipeConfigFactory | None = None,
        pipe_id: str | None = None,
        use: str | None = None,
        params: dict[str, Any] | None = None,
        injects: dict[str, str] | None = None,
    ) -> None:
        self._factory = factory or PipeConfigFactory()

        self._pipe_id = pipe_id or uuid.uuid4().hex
        self._use = use
        self._params = dict(params or {})
        self._injects = dict(injects or {})
        self._steps: list[PipeConfig] = []

    def add_step(self, step: PipeConfig) -> PipeConfigBuilder:
        self._steps.append(step)
        return self

    def add_steps(self, steps: Iterable[PipeConfig]) -> PipeConfigBuilder:
        self._steps.extend(steps)
        return self

    def set_id(self, pipe_id: str) -> PipeConfigBuilder:
        self._pipe_id = pipe_id
        return self

    def set_use(self, use: str) -> PipeConfigBuilder:
        self._use = use
        return self

    def set_params(self, params: dict[str, Any]) -> PipeConfigBuilder:
        self._params = dict(params)
        return self

    def set_injects(self, injects: dict[str, str]) -> PipeConfigBuilder:
        self._injects = dict(injects)
        return self

    def copy(self) -> PipeConfigBuilder:
        builder = PipeConfigBuilder(
            factory=self._factory,
            pipe_id=self._pipe_id,
            use=self._use,
            params=self._params.copy(),
            injects=self._injects.copy(),
        )
        builder._steps = self._steps.copy()
        return builder

    def build(self) -> PipeConfig:
        params = dict(self._params)
        if self._steps:
            params["steps"] = [step.model_dump(mode="json", exclude_none=True) for step in self._steps]
        return self._factory.create_pipe(
            self._pipe_id,
            self._use,
            params=params,
            injects=self._injects,
        )
