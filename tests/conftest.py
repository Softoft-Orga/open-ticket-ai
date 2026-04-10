import pytest

from open_ticket_ai.core.pipes.pipe_context_model import PipeContext


@pytest.fixture
def empty_pipeline_context() -> PipeContext:
    return PipeContext.empty()
