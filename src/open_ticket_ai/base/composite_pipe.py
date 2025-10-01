from typing import Any

from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult


class CompositePipe(Pipe):
    def _build_pipe_from_step_config(self, step_config: dict[str, Any], context: Context) -> Pipe:
        return self._factory.create_pipe(self.config.model_dump(), step_config, context.model_dump())

    async def _process_steps(self, context: Context) -> list[PipeResult]:
        results: list[PipeResult] = []
        current_context = context
        for step_pipe_config_raw in self.config.steps:
            step_pipe_id = step_pipe_config_raw["id"]
            step_pipe = self._build_pipe_from_step_config(step_pipe_config_raw, current_context)
            current_context = await step_pipe.process(current_context)
            results.append(current_context.pipes[step_pipe_id])
        self._current_context = current_context
        return results

    async def process(self, context: Context) -> Context:
        # noinspection PyProtectedMember
        if self.config._if and self.have_dependent_pipes_been_run(context):
            steps_result: list[PipeResult] = await self._process_steps(context)

            new_context = context.model_copy()
            composite_result = PipeResult.union(steps_result)

            return self._save_pipe_result(new_context, composite_result)

        return context
