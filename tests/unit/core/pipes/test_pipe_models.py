import pytest

from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


@pytest.fixture
def success_result() -> PipeResult:
    return PipeResult.success(message="Operation successful", data={"key": "value"})


@pytest.fixture
def fail_result() -> PipeResult:
    return PipeResult.failure(message="Operation failed")


@pytest.fixture
def error_result() -> PipeResult:
    return PipeResult.failure(message="Error occurred")


@pytest.fixture
def skipped_result() -> PipeResult:
    return PipeResult.skipped(message="Operation skipped")


class TestPipeResultAndOperator:
    def test_and_combines_two_success_results(self) -> None:
        result1 = PipeResult.success(message="First success")
        result2 = PipeResult.success(message="Second success")

        combined = result1 & result2

        assert combined.succeeded is True
        assert "First success" in combined.message
        assert "Second success" in combined.message

    def test_and_combines_success_and_failure(self, success_result: PipeResult, fail_result: PipeResult) -> None:
        combined = success_result & fail_result

        assert combined.succeeded is False
        assert "Operation successful" in combined.message
        assert "Operation failed" in combined.message

    def test_and_merges_data_from_both_results(self) -> None:
        result1 = PipeResult.success(data={"key1": "value1"})
        result2 = PipeResult.success(data={"key2": "value2"})

        combined = result1 & result2

        assert combined.data == {"key1": "value1", "key2": "value2"}

    def test_and_second_data_overwrites_first(self) -> None:
        result1 = PipeResult.success(data={"key": "value1"})
        result2 = PipeResult.success(data={"key": "value2"})

        combined = result1 & result2

        assert combined.data["key"] == "value2"


class TestPipeResultUnion:
    def test_union_with_empty_list(self) -> None:
        result = PipeResult.union([])

        assert result.succeeded is True
        assert result.message == ""

    def test_union_with_single_result(self, success_result: PipeResult) -> None:
        result = PipeResult.union([success_result])

        assert result.succeeded is True
        assert "Operation successful" in result.message
        assert result.data == {"key": "value"}

    def test_union_behaves_like_chaining_and(self) -> None:
        result1 = PipeResult.success(message="First")
        result2 = PipeResult.success(message="Second")
        result3 = PipeResult.success(message="Third")

        union_result = PipeResult.union([result1, result2, result3])
        chained_result = result1 & result2 & result3

        assert union_result.succeeded == chained_result.succeeded
        assert union_result.message == chained_result.message
        assert union_result.data == chained_result.data

    def test_union_with_mixed_results(
        self, success_result: PipeResult, fail_result: PipeResult, error_result: PipeResult
    ) -> None:
        result = PipeResult.union([success_result, fail_result, error_result])

        assert result.succeeded is False
        assert "Operation successful" in result.message
        assert "Operation failed" in result.message
        assert "Error occurred" in result.message


class TestPipeResultStaticMethods:
    def test_success_returns_succeeded_result(self) -> None:
        result = PipeResult.success()

        assert result.succeeded is True
        assert result.was_skipped is False
        assert result.message == ""
        assert result.data == {}

    def test_success_with_message_and_data(self) -> None:
        result = PipeResult.success(message="Success message", data={"key": "value"})

        assert result.succeeded is True
        assert result.message == "Success message"
        assert result.data == {"key": "value"}

    def test_failure_returns_failed_result(self) -> None:
        result = PipeResult.failure(message="Failure message")

        assert result.succeeded is False
        assert result.was_skipped is False
        assert result.message == "Failure message"

    def test_skipped_returns_skipped_result(self) -> None:
        result = PipeResult.skipped(message="Skipped message")

        assert result.succeeded is False
        assert result.was_skipped is True
        assert result.message == "Skipped message"

    def test_skipped_without_message(self) -> None:
        result = PipeResult.skipped()

        assert result.succeeded is False
        assert result.was_skipped is True
        assert result.message == ""

    def test_empty_returns_default_result(self) -> None:
        result = PipeResult.empty()

        assert result.succeeded is True
        assert result.was_skipped is False
        assert result.message == ""
        assert result.data == {}


class TestPipeConfigShouldRun:
    def test_should_run_with_true_boolean(self) -> None:
        config = PipeConfig(id="test", use="test.module.Class", if_=True)

        assert config.should_run is True

    def test_should_run_with_false_boolean(self) -> None:
        config = PipeConfig(id="test", use="test.module.Class", if_=False)

        assert config.should_run is False

    def test_should_run_with_string_true(self) -> None:
        config = PipeConfig(id="test", use="test.module.Class", if_="True")

        assert config.should_run == "True"

    def test_should_run_with_string_expression(self) -> None:
        config = PipeConfig(id="test", use="test.module.Class", if_="some_condition")

        assert config.should_run == "some_condition"

    def test_should_run_default_value(self) -> None:
        config = PipeConfig(id="test", use="test.module.Class")

        assert config.should_run == "True"


@pytest.mark.parametrize(
    ("if_value", "expected"),
    [
        (True, True),
        (False, False),
        ("True", "True"),
        ("False", "False"),
        ("1 == 1", "1 == 1"),
    ],
)
def test_should_run_parametrized(if_value: str | bool, expected: str | bool) -> None:
    config = PipeConfig(id="test", use="test.module.Class", if_=if_value)

    assert config.should_run == expected
