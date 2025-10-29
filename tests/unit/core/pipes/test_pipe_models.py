from open_ticket_ai.core.pipes.pipe_models import PipeResult


def test_and_combines_two_success_results() -> None:
    result1 = PipeResult.success(message="First")
    result2 = PipeResult.success(message="Second")

    combined = result1 & result2

    assert combined.succeeded is True
    assert combined.message == "First; Second"


def test_and_combines_success_and_failure() -> None:
    result1 = PipeResult.success(message="Success")
    result2 = PipeResult.failure(message="Failure")

    combined = result1 & result2

    assert combined.succeeded is False
    assert combined.message == "Success; Failure"


def test_union_behaves_like_chaining_and() -> None:
    p1 = PipeResult.success(message="First")
    p2 = PipeResult.success(message="Second")
    p3 = PipeResult.success(message="Third")

    union_result = PipeResult.union([p1, p2, p3])
    chained_result = p1 & p2 & p3

    assert union_result.succeeded == chained_result.succeeded
    assert union_result.message == chained_result.message
    assert union_result.data == chained_result.data


def test_success_returns_succeeded_result() -> None:
    result = PipeResult.success()

    assert result.succeeded is True
    assert result.message == ""


def test_failure_returns_failed_result() -> None:
    result = PipeResult.failure(message="Failure message")

    assert result.succeeded is False
    assert result.message == "Failure message"
