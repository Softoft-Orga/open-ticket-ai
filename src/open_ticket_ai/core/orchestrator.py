import asyncio
import logging
import threading
from typing import Any, Iterable

from open_ticket_ai.core.config.config_models import OrchestratorRunnerConfig
from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.base_pipe import BasePipe
from open_ticket_ai.core.pipeline.base_pipe_config import RawPipeConfig
from open_ticket_ai.core.pipeline.context import PipelineContext


class Orchestrator:
    def __init__(
        self,
        runners: Iterable[OrchestratorRunnerConfig],
        registry: UnifiedRegistry,
    ) -> None:
        self._runner_configs = list(runners)
        self._registry = registry
        self._logger = logging.getLogger(__name__)
        self._stop_event = threading.Event()
        self._threads: list[threading.Thread] = []
        self._runner_exceptions: list[BaseException] = []
        self._exceptions_lock = threading.Lock()

        if not self._runner_configs:
            raise ValueError("At least one runner must be configured for the orchestrator")

    async def run(self, initial_context: dict[str, Any] | None = None) -> None:
        self._logger.info("Starting orchestrator with %d runner(s)", len(self._runner_configs))

        self._start_threads(initial_context or {})

        try:
            while not self._stop_event.is_set():
                await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            self._logger.info("Cancellation received, stopping orchestrator threads")
            self.stop()
            raise
        except Exception:
            self._logger.exception("Unexpected error in orchestrator run loop")
            self.stop()
            raise

        self.stop()

        if self._runner_exceptions:
            raise self._runner_exceptions[0]

    def stop(self) -> None:
        self._stop_event.set()
        for thread in self._threads:
            if thread.is_alive():
                thread.join()

    def _start_threads(self, initial_context: dict[str, Any]) -> None:
        for runner_config in self._runner_configs:
            thread = threading.Thread(
                target=self._runner_loop,
                args=(runner_config, initial_context.copy()),
                daemon=True,
            )
            thread.start()
            self._threads.append(thread)

    def _runner_loop(
        self,
        runner_config: OrchestratorRunnerConfig,
        initial_context: dict[str, Any],
    ) -> None:
        interval_seconds = max(runner_config.run_every_milli_seconds, 0) / 1000.0
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        context = PipelineContext()
        if initial_context:
            context.config.update(initial_context)

        try:
            while not self._stop_event.is_set():
                try:
                    context = loop.run_until_complete(
                        self._execute_pipe_config(runner_config.pipe, context)
                    )
                except Exception as exc:  # pragma: no cover - defensive logging
                    self._logger.error(
                        "Runner for interval %sms failed: %s",
                        runner_config.run_every_milli_seconds,
                        exc,
                        exc_info=True,
                    )
                    with self._exceptions_lock:
                        self._runner_exceptions.append(exc)
                    self._stop_event.set()
                    break

                if self._stop_event.wait(interval_seconds):
                    break
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            asyncio.set_event_loop(None)
            loop.close()

    async def _execute_pipe_config(
        self, pipe_config: RawPipeConfig, context: PipelineContext
    ) -> PipelineContext:
        if pipe_config.use:
            pipe_instance = self._build_pipe_instance(pipe_config)
            return await pipe_instance.process(context)

        if not pipe_config.steps:
            raise ValueError("Pipe configuration must define a 'use' or 'steps' entry")

        return await self._execute_steps(pipe_config.steps, context)

    async def _execute_steps(
        self, steps: Iterable[RawPipeConfig], context: PipelineContext
    ) -> PipelineContext:
        current_context = context
        for step in steps:
            current_context = await self._execute_pipe_config(step, current_context)
        return current_context

    def _build_pipe_instance(self, pipe_config: RawPipeConfig) -> BasePipe[Any]:
        pipe_class = self._registry.get_class(pipe_config.use)

        signature = inspect.signature(pipe_class.__init__)
        constructor_kwargs: dict[str, Any] = {}

        if "registry" in signature.parameters:
            constructor_kwargs["registry"] = self._registry

        if isinstance(pipe_config.services, dict):
            for param_name, service_id in pipe_config.services.items():
                if param_name in signature.parameters:
                    constructor_kwargs[param_name] = self._registry.get_service_instance(service_id)
                else:
                    self._logger.debug(
                        "Service binding '%s' ignored for pipe %s", param_name, pipe_class.__name__
                    )

        return pipe_class(config=pipe_config, **constructor_kwargs)
