from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult


def test_has_succeeded_returns_true_for_successful_result():
    success_result = PipeResult.success(message="Success", data={"key": "value"})
    context = PipeContext(pipe_results={"pipe1": success_result.model_dump()}, params={})

    assert context.has_succeeded("pipe1") is True


def test_has_succeeded_returns_false_for_failed_result():
    failed_result = PipeResult.failure(message="Failed")
    context = PipeContext(pipe_results={"pipe1": failed_result.model_dump()}, params={})

    assert context.has_succeeded("pipe1") is False


def test_has_succeeded_returns_false_for_skipped_result():
    skipped_result = PipeResult.skipped(message="Skipped")
    context = PipeContext(pipe_results={"pipe1": skipped_result.model_dump()}, params={})

    assert context.has_succeeded("pipe1") is False


def test_has_succeeded_returns_false_for_missing_pipe():
    context = PipeContext(pipe_results={}, params={})

    assert context.has_succeeded("nonexistent") is False


def test_with_pipe_result_adds_new_result():
    context = PipeContext(pipe_results={}, params={})
    result = PipeResult.success(message="Success", data={"key": "value"})

    new_context = context.with_pipe_result("pipe1", result)

    assert "pipe1" in new_context.pipe_results
    stored_result = PipeResult.model_validate(new_context.pipe_results["pipe1"])
    assert stored_result == result


def test_with_pipe_result_preserves_existing_results():
    existing_result = PipeResult.success(message="Existing", data={"old": "data"})
    context = PipeContext(pipe_results={"pipe1": existing_result.model_dump()}, params={})
    new_result = PipeResult.success(message="New", data={"new": "data"})

    new_context = context.with_pipe_result("pipe2", new_result)

    assert "pipe1" in new_context.pipe_results
    assert "pipe2" in new_context.pipe_results


def test_with_pipe_result_returns_new_instance():
    context = PipeContext(pipe_results={}, params={})
    result = PipeResult.success(message="Success")

    new_context = context.with_pipe_result("pipe1", result)

    assert new_context is not context
    assert "pipe1" not in context.pipe_results
