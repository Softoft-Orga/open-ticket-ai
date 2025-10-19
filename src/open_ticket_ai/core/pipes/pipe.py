from __future__ import annotations

from abc import ABC
from typing import Any, final

from pydantic import BaseModel

from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


class Pipe[ParamsT: BaseModel](Injectable[ParamsT], ABC):
    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)
        self._config: PipeConfig = PipeConfig.model_validate(config.model_dump())

    @final
    async def process(self, context: PipeContext) -> PipeResult:
        if await self._should_run(context):
            self._logger.info(f"▶️  Executing pipe: {self._config.id}")
            self._logger.debug(f"Pipe type: {self.__class__.__name__}, Dependencies: {self._config.depends_on}")

            try:
                result = await self._process(context)

                if result.succeeded:
                    self._logger.info(f"✅ Pipe {self._config.id} completed successfully")
                    self._logger.debug(f"Result data keys: {list(result.data.keys()) if result.data else 'None'}")
                else:
                    self._logger.warning(f"⚠️  Pipe {self._config.id} failed: {result.message}")

                return result

            except Exception as e:
                self._logger.error(f"❌ Pipe {self._config.id} raised exception: {e}", exc_info=True)
                return PipeResult.failure(f"Exception in pipe {self._config.id}: {e!s}")
        else:
            self._logger.debug(f"⏭️  Skipping pipe: {self._config.id} (conditions not met)")
            return PipeResult.skipped()

    @final
    def _are_dependencies_fulfilled(self, context: PipeContext) -> bool:
        if not self._config.depends_on:
            return True

        fulfilled = all(context.has_succeeded(pipe_id) for pipe_id in self._config.depends_on)

        if not fulfilled:
            missing = [pipe_id for pipe_id in self._config.depends_on if not context.has_succeeded(pipe_id)]
            self._logger.debug(f"Dependencies not fulfilled for {self._config.id}. Missing: {missing}")

        return fulfilled

    async def _process(self, *_: Any, **__: Any) -> PipeResult:
        return PipeResult.skipped()

    async def _should_run(self, context: PipeContext) -> bool:
        return self._config.should_run and self._are_dependencies_fulfilled(context)
