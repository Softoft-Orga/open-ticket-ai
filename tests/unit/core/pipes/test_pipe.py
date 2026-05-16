import pytest

from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class ConcretePipeForTesting(Pipe):
    def __init__(self, pipe_id: str = "test_pipe", value: str = "default") -> None:
        super().__init__(pipe_id)
        self.value = value
        self.process_called = False

    async def _process(self, context: PipeContext) -> PipeResult:
        self.process_called = True
        return PipeResult.success(message="processed", data={"result": self.value})


class TestPipeInitialization:
    def test_pipe_stores_pipe_id(self):
        pipe = ConcretePipeForTesting(pipe_id="my_pipe")
        assert pipe.pipe_id == "my_pipe"

    def test_pipe_defaults_to_class_name(self):
        pipe = ConcretePipeForTesting(pipe_id="")
        assert pipe.pipe_id == "ConcretePipeForTesting"

    def test_pipe_has_logger(self):
        pipe = ConcretePipeForTesting(pipe_id="test")
        assert pipe._logger is not None


class TestPipeProcess:
    async def test_process_calls_internal_process(self):
        pipe = ConcretePipeForTesting(pipe_id="test_pipe", value="test_value")
        context = PipeContext.empty()

        result = await pipe.process(context)

        assert pipe.process_called
        assert result.succeeded
        assert result.message == "processed"
        assert result.data == {"result": "test_value"}
