import os
from unittest.mock import MagicMock

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.template_rendering.jinja_renderer_extras import (
    at_path,
    build_filtered_env,
    has_failed,
    pipe_result,
)
from open_ticket_ai.core.template_rendering.renderer_config import (
    JinjaRendererConfig,
    TemplateRendererEnvConfig,
)


class SampleModel(BaseModel):
    name: str
    age: int


class TestAtPath:
    def test_at_path_with_none_path(self):
        result = at_path("test_value", None)
        assert result == '"test_value"'

    def test_at_path_with_empty_string_path(self):
        result = at_path("test_value", "")
        assert result == '"test_value"'

    def test_at_path_with_whitespace_path(self):
        result = at_path("test_value", "   ")
        assert result == '"test_value"'

    def test_at_path_with_simple_string_path(self):
        result = at_path("test_value", "a.b.c")
        assert result == '{"a": {"b": {"c": "test_value"}}}'

    def test_at_path_with_single_key_path(self):
        result = at_path("test_value", "key")
        assert result == '{"key": "test_value"}'

    def test_at_path_with_list_path(self):
        result = at_path("test_value", ["a", "b", "c"])
        assert result == '{"a": {"b": {"c": "test_value"}}}'

    def test_at_path_with_tuple_path(self):
        result = at_path("test_value", ("x", "y", "z"))
        assert result == '{"x": {"y": {"z": "test_value"}}}'

    def test_at_path_with_list_path_filters_empty_strings(self):
        result = at_path("test_value", ["a", "", "b"])
        assert result == '{"a": {"b": "test_value"}}'

    def test_at_path_with_literal_eval_list_string(self):
        result = at_path("test_value", "['a', 'b', 'c']")
        assert result == '{"a": {"b": {"c": "test_value"}}}'

    def test_at_path_with_literal_eval_tuple_string(self):
        result = at_path("test_value", "('x', 'y')")
        assert result == '{"x": {"y": "test_value"}}'

    def test_at_path_with_invalid_literal_eval_falls_back_to_split(self):
        result = at_path("test_value", "['invalid")
        assert result == '{"[\'invalid": "test_value"}'

    def test_at_path_with_numeric_path(self):
        result = at_path("test_value", 123)
        assert result == '{"123": "test_value"}'

    def test_at_path_with_dict_value(self):
        result = at_path({"key": "value"}, "a.b")
        assert result == '{"a": {"b": {"key": "value"}}}'

    def test_at_path_with_base_model_value(self):
        model = SampleModel(name="John", age=30)
        result = at_path(model, "person")
        assert result == '{"person": {"name": "John", "age": 30}}'

    def test_at_path_with_complex_nested_structure(self):
        value = {"users": [{"id": 1, "name": "Alice"}], "count": 1}
        result = at_path(value, "data.response")
        assert result == '{"data": {"response": {"users": [{"id": 1, "name": "Alice"}], "count": 1}}}'

    def test_at_path_with_path_containing_dots_in_middle(self):
        result = at_path("value", "a..b")
        assert result == '{"a": {"b": "value"}}'

    def test_at_path_with_path_starting_with_dot(self):
        result = at_path("value", ".a.b")
        assert result == '{"a": {"b": "value"}}'

    def test_at_path_with_path_ending_with_dot(self):
        result = at_path("value", "a.b.")
        assert result == '{"a": {"b": "value"}}'


class TestHasFailed:
    def test_has_failed_when_pipe_id_not_in_context(self):
        ctx = MagicMock()
        ctx.get.return_value = {}
        result = has_failed(ctx, "nonexistent_pipe")
        assert result is False

    def test_has_failed_when_pipes_key_missing_in_context(self):
        ctx = MagicMock()
        ctx.get.return_value = {}
        result = has_failed(ctx, "test_pipe")
        assert result is False

    def test_has_failed_with_pipe_result_failed_true(self):
        pipe_res = PipeResult(success=False, failed=True, message="Error occurred")
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": pipe_res}
        result = has_failed(ctx, "test_pipe")
        assert result is True

    def test_has_failed_with_pipe_result_object_attribute_set_to_true(self):
        pipe_res = PipeResult(success=True, failed=False)
        pipe_res.failed = True
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": pipe_res}
        result = has_failed(ctx, "test_pipe")
        assert result is True

    def test_has_failed_with_mock_pipe_with_failed_attribute(self):
        # Test with a mock object that has both .failed attribute and .get() method
        mock_pipe = MagicMock()
        mock_pipe.failed = True
        mock_pipe.get.return_value = False
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": mock_pipe}
        result = has_failed(ctx, "test_pipe")
        # Should return True because pipe.failed is True (short-circuit evaluation)
        assert result is True

    def test_has_failed_with_mock_pipe_failed_false_and_get_returns_true(self):
        # Test with a mock object that has .failed=False and .get("failed") returns True
        mock_pipe = MagicMock()
        mock_pipe.failed = False
        mock_pipe.get.return_value = True
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": mock_pipe}
        result = has_failed(ctx, "test_pipe")
        # Should return True because pipe.get("failed") is True
        assert result is True

    def test_has_failed_with_mock_pipe_both_false(self):
        # Test with a mock object that has .failed=False and .get("failed") returns False
        mock_pipe = MagicMock()
        mock_pipe.failed = False
        mock_pipe.get.return_value = False
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": mock_pipe}
        result = has_failed(ctx, "test_pipe")
        # Should return False
        assert result is False


class TestPipeResult:
    def test_pipe_result_when_pipe_id_not_in_context(self):
        ctx = MagicMock()
        ctx.get.return_value = {}
        result = pipe_result(ctx, "nonexistent_pipe")
        assert result is None

    def test_pipe_result_when_pipes_key_missing_in_context(self):
        ctx = MagicMock()
        ctx.get.return_value = {}
        result = pipe_result(ctx, "test_pipe")
        assert result is None

    def test_pipe_result_with_pipe_result_object_default_key(self):
        pipe_res = PipeResult(
            success=True,
            failed=False,
            data={"value": "test_result", "extra": "data"},
        )
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": pipe_res}
        result = pipe_result(ctx, "test_pipe")
        assert result == "test_result"

    def test_pipe_result_with_pipe_result_object_custom_key(self):
        pipe_res = PipeResult(
            success=True,
            failed=False,
            data={"value": "default", "custom_key": "custom_value"},
        )
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": pipe_res}
        result = pipe_result(ctx, "test_pipe", "custom_key")
        assert result == "custom_value"

    def test_pipe_result_with_dict_pipe_default_key(self):
        ctx = MagicMock()
        ctx.get.return_value = {
            "test_pipe": {
                "success": True,
                "failed": False,
                "data": {"value": "dict_result"},
            }
        }
        result = pipe_result(ctx, "test_pipe")
        assert result == "dict_result"

    def test_pipe_result_with_dict_pipe_custom_key(self):
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": {"data": {"value": "default", "status": "completed"}}}
        result = pipe_result(ctx, "test_pipe", "status")
        assert result == "completed"

    def test_pipe_result_with_missing_data_key(self):
        pipe_res = PipeResult(
            success=True,
            failed=False,
            data={"other_key": "value"},
        )
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": pipe_res}
        result = pipe_result(ctx, "test_pipe", "nonexistent")
        assert result is None

    def test_pipe_result_with_complex_data_structure(self):
        pipe_res = PipeResult(
            success=True,
            failed=False,
            data={
                "value": {"nested": {"data": "test"}},
                "list": [1, 2, 3],
            },
        )
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": pipe_res}
        result = pipe_result(ctx, "test_pipe")
        assert result == {"nested": {"data": "test"}}


class TestBuildFilteredEnv:
    def setup_method(self):
        self.original_env = dict(os.environ)

    def teardown_method(self):
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_build_filtered_env_with_no_prefix(self):
        os.environ["TEST_VAR"] = "test_value"
        os.environ["OTHER_VAR"] = "other_value"

        config = JinjaRendererConfig(env_config=TemplateRendererEnvConfig(prefix=None))
        result = build_filtered_env(config)

        assert "TEST_VAR" in result
        assert "OTHER_VAR" in result
        assert result["TEST_VAR"] == "test_value"
        assert result["OTHER_VAR"] == "other_value"

    def test_build_filtered_env_with_empty_string_prefix(self):
        os.environ["TEST_VAR"] = "test_value"
        os.environ["OTHER_VAR"] = "other_value"

        config = JinjaRendererConfig(env_config=TemplateRendererEnvConfig(prefix=""))
        result = build_filtered_env(config)

        assert "TEST_VAR" in result
        assert "OTHER_VAR" in result

    def test_build_filtered_env_with_prefix(self):
        os.environ["OTAI_TEST"] = "otai_value"
        os.environ["OTHER_TEST"] = "other_value"

        config = JinjaRendererConfig(env_config=TemplateRendererEnvConfig(prefix="OTAI_"))
        result = build_filtered_env(config)

        assert "OTAI_TEST" in result
        assert "OTHER_TEST" not in result
        assert result["OTAI_TEST"] == "otai_value"

    def test_build_filtered_env_with_allowlist(self):
        os.environ["VAR1"] = "value1"
        os.environ["VAR2"] = "value2"
        os.environ["VAR3"] = "value3"

        config = JinjaRendererConfig(env_config=TemplateRendererEnvConfig(prefix=None, allowlist={"VAR1", "VAR3"}))
        result = build_filtered_env(config)

        assert "VAR1" in result
        assert "VAR2" not in result
        assert "VAR3" in result

    def test_build_filtered_env_with_denylist(self):
        os.environ["VAR1"] = "value1"
        os.environ["VAR2"] = "value2"
        os.environ["VAR3"] = "value3"

        config = JinjaRendererConfig(env_config=TemplateRendererEnvConfig(prefix=None, denylist={"VAR2"}))
        result = build_filtered_env(config)

        assert "VAR1" in result
        assert "VAR2" not in result
        assert "VAR3" in result

    def test_build_filtered_env_with_prefix_and_allowlist(self):
        os.environ["OTAI_ALLOWED"] = "allowed_value"
        os.environ["OTAI_BLOCKED"] = "blocked_value"
        os.environ["OTHER_VAR"] = "other_value"

        config = JinjaRendererConfig(env_config=TemplateRendererEnvConfig(prefix="OTAI_", allowlist={"OTAI_ALLOWED"}))
        result = build_filtered_env(config)

        assert "OTAI_ALLOWED" in result
        assert "OTAI_BLOCKED" not in result
        assert "OTHER_VAR" not in result

    def test_build_filtered_env_with_prefix_and_denylist(self):
        os.environ["OTAI_GOOD"] = "good_value"
        os.environ["OTAI_BAD"] = "bad_value"
        os.environ["OTHER_VAR"] = "other_value"

        config = JinjaRendererConfig(env_config=TemplateRendererEnvConfig(prefix="OTAI_", denylist={"OTAI_BAD"}))
        result = build_filtered_env(config)

        assert "OTAI_GOOD" in result
        assert "OTAI_BAD" not in result
        assert "OTHER_VAR" not in result

    def test_build_filtered_env_with_all_filters(self):
        os.environ["OTAI_ALLOW1"] = "value1"
        os.environ["OTAI_ALLOW2"] = "value2"
        os.environ["OTAI_DENY"] = "deny_value"
        os.environ["OTHER_VAR"] = "other_value"

        config = JinjaRendererConfig(
            env_config=TemplateRendererEnvConfig(
                prefix="OTAI_", allowlist={"OTAI_ALLOW1", "OTAI_ALLOW2", "OTAI_DENY"}, denylist={"OTAI_DENY"}
            )
        )
        result = build_filtered_env(config)

        assert "OTAI_ALLOW1" in result
        assert "OTAI_ALLOW2" in result
        assert "OTAI_DENY" not in result
        assert "OTHER_VAR" not in result

    def test_build_filtered_env_empty_result(self):
        os.environ["VAR1"] = "value1"

        config = JinjaRendererConfig(env_config=TemplateRendererEnvConfig(prefix="NONEXISTENT_"))
        result = build_filtered_env(config)

        assert len(result) == 0

    def test_build_filtered_env_preserves_values(self):
        os.environ["OTAI_SPECIAL"] = "special!@#$%^&*()"

        config = JinjaRendererConfig(env_config=TemplateRendererEnvConfig(prefix="OTAI_"))
        result = build_filtered_env(config)

        assert result["OTAI_SPECIAL"] == "special!@#$%^&*()"
