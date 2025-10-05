import logging
from typing import Any

from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult, RenderedPipeConfig
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory


class CompositePipeConfig(RenderedPipeConfig):
    steps: list[dict[str, Any]]


class CompositePipe(Pipe):

    def __init__(self, config_raw: dict[str, Any], factory: PipeFactory | None = None, *args, **kwargs) -> None:
        super().__init__(config_raw, factory, *args, **kwargs)
        self.config = CompositePipeConfig.model_validate(config_raw)

        self._logger = logging.getLogger(self.__class__.__name__)
        self._factory = factory
        self._app_config = kwargs.get("app_config")

    def _build_pipe_from_step_config(self, step_config: dict[str, Any], context: Context) -> Pipe:
        # Render the parent config before passing it to child pipes
        parent_config_rendered = self._factory.render_pipe_config(
            self.config.model_dump(),
            context.model_dump()
        )
        return self._factory.create_pipe(parent_config_rendered, step_config, context.model_dump())

    async def _process_steps(self, context: Context) -> list[PipeResult]:

        results: list[PipeResult] = []

        current_context = context

        from open_ticket_ai.core.pipeline.prefect_flows import is_in_prefect_context, execute_single_pipe_task

        use_prefect = is_in_prefect_context()

        for step_pipe_config_raw in self.config.steps:
            step_pipe_id = step_pipe_config_raw["id"]

            if use_prefect and self._app_config:
                retries = step_pipe_config_raw.get("retries", 2)
                retry_delay_seconds = step_pipe_config_raw.get("retry_delay_seconds", 30)
                
                context_data = current_context.model_dump()
                updated_context_data = await execute_single_pipe_task(
                    app_config=self._app_config,
                    pipe_config=step_pipe_config_raw,
                    context_data=context_data,
                    pipe_id=step_pipe_id,
                    retries=retries,
                    retry_delay_seconds=retry_delay_seconds,
                )
                current_context = Context(**updated_context_data)
            else:
                step_pipe = self._build_pipe_from_step_config(step_pipe_config_raw, current_context)
                current_context = await step_pipe.process(current_context)

            results.append(current_context.pipes[step_pipe_id])

        self._current_context = current_context

        return results

    async def process(self, context: Context) -> Context:

        if self.config.if_ and self.have_dependent_pipes_been_run(context):
            steps_result: list[PipeResult] = await self._process_steps(context)

            composite_result = PipeResult.union(steps_result)

            return self._save_pipe_result(self._current_context, composite_result)

        return context
