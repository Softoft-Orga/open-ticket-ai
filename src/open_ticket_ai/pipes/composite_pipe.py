from typing import Any

from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class CompositePipe(Pipe):
    """Run a list of pipes sequentially, passing results through PipeContext.

    Stops on the first failure and returns the union of all results.
    """

    def __init__(self, pipe_id: str, steps: list[Pipe]) -> None:
        super().__init__(pipe_id)
        self._steps = steps

    def to_descriptor(self) -> dict[str, Any]:
        return {
            **super().to_descriptor(),
            "children": [step.to_descriptor() for step in self._steps],
        }

    async def _process(self, context: PipeContext) -> PipeResult:
        results: list[PipeResult] = []
        for step in self._steps:
            result = await step.process(context)
            context = context.with_pipe_result(step.pipe_id, result)
            if result.has_failed():
                self._logger.warning(f"Step '{step.pipe_id}' failed — skipping remaining steps.")
                break
            results.append(result)
        return PipeResult.union(results)
