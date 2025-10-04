from open_ticket_ai.tools.mermaid_conversion.node import (
    NodeDef,
    NodeRenderer,
    build_node_from_pipe,
    _is_composite,
    _choose_display_name,
    _format_node_label,
)
from open_ticket_ai.tools.mermaid_conversion.utils import (
    sanitize_token,
    _make_global_identifier,
    sanitize_for_mermaid_label,
)


class TestNodeDef:
    def test_node_def_creation(self):
        node = NodeDef("test_id", "Test Label", "process")
        assert node.identifier == "test_id"
        assert node.label == "Test Label"
        assert node.kind == "process"


class TestNodeRenderer:
    def test_render_process_node(self):
        node = NodeDef("step_1", "Process Step", "process")
        result = NodeRenderer.render(node)
        assert result == '    step_1["Process Step"]:::step'

    def test_render_start_node(self):
        node = NodeDef("start_node", "Start Pipeline", "start")
        result = NodeRenderer.render(node)
        assert result == '    start_node(["Start Pipeline"])'

    def test_render_hidden_node(self):
        node = NodeDef("hidden_1", " ", "hidden")
        result = NodeRenderer.render(node)
        assert result == '    hidden_1[" "]:::hidden'

    def test_render_node_with_special_chars(self):
        node = NodeDef("step_1", "Test [brackets] {braces}", "process")
        result = NodeRenderer.render(node)
        assert "&#91;" in result
        assert "&#93;" in result
        assert "&#123;" in result
        assert "&#125;" in result

    def test_render_empty_label(self):
        node = NodeDef("empty", "", "process")
        result = NodeRenderer.render(node)
        assert result == '    empty[" "]:::step'


class TestBuildNodeFromPipe:
    def test_build_simple_node(self):
        step_dict = {
            "id": "test_step",
            "use": "SomePipe"
        }
        node = build_node_from_pipe(step_dict, ["pipeline"], 0)
        assert node is not None
        assert node.identifier == "pipeline__test_step"
        assert "test_step" in node.label
        assert node.kind == "process"

    def test_build_node_without_id_uses_use(self):
        step_dict = {
            "use": "MyPipe:SubModule"
        }
        node = build_node_from_pipe(step_dict, ["pipeline"], 0)
        assert node is not None
        assert "SubModule" in node.label

    def test_build_node_without_id_or_use(self):
        step_dict = {}
        node = build_node_from_pipe(step_dict, ["pipeline"], 5)
        assert node is not None
        assert "step_5" in node.label

    def test_build_node_with_if_condition(self):
        step_dict = {
            "id": "conditional",
            "use": "CheckPipe",
            "if": "{{ some_condition }}"
        }
        node = build_node_from_pipe(step_dict, ["pipeline"], 0)
        assert node is not None
        assert node.kind == "process"
        assert "if {{ some_condition }}" in node.label

    def test_composite_step_returns_none(self):
        step_dict = {
            "id": "composite",
            "steps": [
                {"id": "inner"}
            ]
        }
        node = build_node_from_pipe(step_dict, ["pipeline"], 0)
        assert node is None

    def test_build_node_with_nested_path(self):
        step_dict = {"id": "inner_step"}
        node = build_node_from_pipe(step_dict, ["pipeline", "composite", "sub"], 0)
        assert node is not None
        assert node.identifier == "pipeline__composite__sub__inner_step"


class TestIsComposite:
    def test_is_composite_with_steps_list(self):
        step_dict = {"steps": [{"id": "child"}]}
        assert _is_composite(step_dict) is True

    def test_is_composite_with_empty_list(self):
        step_dict = {"steps": []}
        assert _is_composite(step_dict) is True

    def test_not_composite_without_steps(self):
        step_dict = {"id": "simple"}
        assert _is_composite(step_dict) is False

    def test_not_composite_with_non_list_steps(self):
        step_dict = {"steps": "not_a_list"}
        assert _is_composite(step_dict) is False


class TestChooseDisplayName:
    def test_choose_id_when_present(self):
        step_dict = {"id": "my_step", "use": "SomePipe"}
        assert _choose_display_name(step_dict, 0) == "my_step"

    def test_choose_use_when_no_id(self):
        step_dict = {"use": "module:SomePipe"}
        assert _choose_display_name(step_dict, 0) == "SomePipe"

    def test_choose_use_simple(self):
        step_dict = {"use": "SimplePipe"}
        assert _choose_display_name(step_dict, 0) == "SimplePipe"

    def test_choose_fallback_when_no_id_or_use(self):
        step_dict = {}
        assert _choose_display_name(step_dict, 3) == "step_3"

    def test_empty_id_uses_fallback(self):
        step_dict = {"id": "", "use": ""}
        assert _choose_display_name(step_dict, 7) == "step_7"


class TestFormatNodeLabel:
    def test_format_with_primary_only(self):
        label = _format_node_label("MyStep", {})
        assert label == "MyStep"

    def test_format_with_use_different_from_primary(self):
        step_dict = {"use": "full:path:Pipe"}
        label = _format_node_label("MyStep", step_dict)
        assert "MyStep" in label
        assert "full:path:Pipe" in label
        assert "<br/>" in label

    def test_format_with_use_same_as_primary(self):
        step_dict = {"use": "MyStep"}
        label = _format_node_label("MyStep", step_dict)
        assert label == "MyStep"
        assert label.count("MyStep") == 1

    def test_format_with_if_condition(self):
        step_dict = {"if": "{{ condition }}"}
        label = _format_node_label("Step", step_dict)
        assert "Step" in label
        assert "if {{ condition }}" in label
        assert "<br/>" in label

    def test_format_with_all_fields(self):
        step_dict = {
            "use": "module:Pipe",
            "if": "{{ check }}"
        }
        label = _format_node_label("MyStep", step_dict)
        assert "MyStep" in label
        assert "module:Pipe" in label
        assert "if {{ check }}" in label
        lines = label.split("<br/>")
        assert len(lines) == 3

    def test_format_empty_primary(self):
        label = _format_node_label("", {})
        assert label == ""


class TestSanitizeToken:
    def test_sanitize_alphanumeric(self):
        assert sanitize_token("test_step_123") == "test_step_123"

    def test_sanitize_special_chars(self):
        assert sanitize_token("test-step.name") == "test_step_name"

    def test_sanitize_multiple_underscores(self):
        assert sanitize_token("test___step") == "test_step"

    def test_sanitize_leading_trailing_underscores(self):
        assert sanitize_token("_test_") == "test"

    def test_sanitize_starts_with_digit(self):
        assert sanitize_token("123step") == "n_123step"

    def test_sanitize_empty_string(self):
        assert sanitize_token("") == "node"

    def test_sanitize_only_special_chars(self):
        assert sanitize_token("!!!") == "node"

    def test_sanitize_spaces(self):
        assert sanitize_token("my step name") == "my_step_name"

    def test_sanitize_unicode_chars(self):
        assert sanitize_token("tëst_stép") == "t_st_st_p"


class TestMakeGlobalIdentifier:
    def test_make_identifier_single_part(self):
        assert _make_global_identifier(["pipeline"]) == "pipeline"

    def test_make_identifier_multiple_parts(self):
        assert _make_global_identifier(["pipeline", "step1", "step2"]) == "pipeline__step1__step2"

    def test_make_identifier_with_special_chars(self):
        result = _make_global_identifier(["my-pipeline", "step.name"])
        assert result == "my_pipeline__step_name"

    def test_make_identifier_empty_list(self):
        assert _make_global_identifier([]) == ""

    def test_make_identifier_with_numbers(self):
        assert _make_global_identifier(["pipeline", "123step"]) == "pipeline__n_123step"


class TestSanitizeMermaidLabel:
    def test_sanitize_backslash(self):
        assert sanitize_for_mermaid_label("test\\path") == "test\\\\path"

    def test_sanitize_newline(self):
        assert sanitize_for_mermaid_label("line1\nline2") == "line1<br/>line2"

    def test_sanitize_square_brackets(self):
        result = sanitize_for_mermaid_label("[test]")
        assert result == "&#91;test&#93;"

    def test_sanitize_curly_braces(self):
        result = sanitize_for_mermaid_label("{test}")
        assert result == "&#123;test&#125;"

    def test_sanitize_pipe(self):
        result = sanitize_for_mermaid_label("a|b")
        assert result == "a&#124;b"

    def test_sanitize_multiple_special_chars(self):
        result = sanitize_for_mermaid_label("[{test|value}]")
        assert "&#91;" in result
        assert "&#123;" in result
        assert "&#124;" in result
        assert "&#125;" in result
        assert "&#93;" in result

    def test_sanitize_empty_string(self):
        assert sanitize_for_mermaid_label("") == ""

    def test_sanitize_normal_text(self):
        assert sanitize_for_mermaid_label("normal text") == "normal text"

    def test_sanitize_preserves_order(self):
        result = sanitize_for_mermaid_label("before\nafter")
        assert result == "before<br/>after"


class TestIntegration:
    def test_full_workflow_simple_step(self):
        step_dict = {
            "id": "fetch_tickets",
            "use": "FetchTicketsPipe",
        }
        node = build_node_from_pipe(step_dict, ["queue_classification"], 0)
        assert node is not None

        rendered = NodeRenderer.render(node)
        assert "queue_classification__fetch_tickets" in rendered
        assert "fetch_tickets" in rendered
        assert ":::step" in rendered

    def test_full_workflow_conditional_step(self):
        step_dict = {
            "id": "update_ticket",
            "use": "UpdatePipe",
            "if": "{{ has_failed('previous') }}"
        }
        node = build_node_from_pipe(step_dict, ["pipeline"], 0)
        assert node is not None

        rendered = NodeRenderer.render(node)
        assert "update_ticket" in rendered
        assert node.kind == "process"

    def test_full_workflow_with_special_characters(self):
        step_dict = {
            "id": "step-with.dots",
            "use": "module:sub:Pipe",
            "if": "{{ config['key'] }}"
        }
        node = build_node_from_pipe(step_dict, ["my-pipeline"], 0)
        assert node is not None

        assert "__" in node.identifier
        assert "&#91;" in node.label or "[" not in node.label or "config" in node.label

        rendered = NodeRenderer.render(node)
        assert "my_pipeline__step_with_dots" in rendered
