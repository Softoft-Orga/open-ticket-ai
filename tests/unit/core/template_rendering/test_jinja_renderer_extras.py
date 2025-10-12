import os
from unittest.mock import MagicMock

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.base.template_renderers.jinja_renderer_extras import (
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
    def test_at_path_with_simple_path(self):
        result = at_path("test_value", "a.b.c")
        assert result == '{"a": {"b": {"c": "test_value"}}}'

    def test_at_path_with_empty_path_returns_json_value(self):
        result = at_path("test_value", None)
        assert result == '"test_value"'

    def test_at_path_with_list_path(self):
        result = at_path("test_value", ["a", "b", "c"])
        assert result == '{"a": {"b": {"c": "test_value"}}}'

    def test_at_path_with_complex_value(self):
        value = {"users": [{"id": 1, "name": "Alice"}], "count": 1}
        result = at_path(value, "data.response")
        assert result == '{"data": {"response": {"users": [{"id": 1, "name": "Alice"}], "count": 1}}}'

    def test_at_path_with_base_model_value(self):
        model = SampleModel(name="John", age=30)
        result = at_path(model, "person")
        assert result == '{"person": {"name": "John", "age": 30}}'


class TestHasFailed:
    def test_has_failed_when_pipe_not_in_context(self):
        ctx = MagicMock()
        ctx.get.return_value = {}
        result = has_failed(ctx, "nonexistent_pipe")
        assert result is False

    def test_has_failed_with_failed_pipe_result(self):
        pipe_res = PipeResult(success=False, failed=True, message="Error occurred")
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": pipe_res}
        result = has_failed(ctx, "test_pipe")
        assert result is True


class TestPipeResult:
    def test_pipe_result_when_pipe_not_in_context(self):
        ctx = MagicMock()
        ctx.get.return_value = {}
        result = pipe_result(ctx, "nonexistent_pipe")
        assert result is None

    def test_pipe_result_with_default_key(self):
        pipe_res = PipeResult(
            success=True,
            failed=False,
            data={"value": "test_result", "extra": "data"},
        )
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": pipe_res}
        result = pipe_result(ctx, "test_pipe")
        assert result == "test_result"

    def test_pipe_result_with_custom_key(self):
        pipe_res = PipeResult(
            success=True,
            failed=False,
            data={"value": "default", "custom_key": "custom_value"},
        )
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": pipe_res}
        result = pipe_result(ctx, "test_pipe", "custom_key")
        assert result == "custom_value"

    def test_pipe_result_with_missing_key(self):
        pipe_res = PipeResult(
            success=True,
            failed=False,
            data={"other_key": "value"},
        )
        ctx = MagicMock()
        ctx.get.return_value = {"test_pipe": pipe_res}
        result = pipe_result(ctx, "test_pipe", "nonexistent")
        assert result is None


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

    def test_build_filtered_env_with_prefix(self):
        os.environ["OTAI_TEST"] = "otai_value"
        os.environ["OTHER_TEST"] = "other_value"

        config = JinjaRendererConfig(env_config=TemplateRendererEnvConfig(prefix="OTAI_"))
        result = build_filtered_env(config)

        assert "OTAI_TEST" in result
        assert "OTHER_TEST" not in result

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

        config = JinjaRendererConfig(env_config=TemplateRendererEnvConfig(prefix=None, denylist={"VAR2"}))
        result = build_filtered_env(config)

        assert "VAR1" in result
        assert "VAR2" not in result

    def test_build_filtered_env_with_combined_filters(self):
        os.environ["OTAI_ALLOW"] = "allowed"
        os.environ["OTAI_DENY"] = "denied"
        os.environ["OTHER_VAR"] = "other"

        config = JinjaRendererConfig(
            env_config=TemplateRendererEnvConfig(
                prefix="OTAI_", allowlist={"OTAI_ALLOW", "OTAI_DENY"}, denylist={"OTAI_DENY"}
            )
        )
        result = build_filtered_env(config)

        assert "OTAI_ALLOW" in result
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
