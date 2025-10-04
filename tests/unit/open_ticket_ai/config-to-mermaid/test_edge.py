from open_ticket_ai.tools.mermaid_conversion.edge import (
    EdgeDef,
    EdgeRenderer,
    _sanitize_mermaid_label,
)


class TestEdgeDef:
    def test_edge_def_creation_without_label(self):
        edge = EdgeDef("node1", "node2")
        assert edge.source == "node1"
        assert edge.target == "node2"
        assert edge.label is None

    def test_edge_def_creation_with_label(self):
        edge = EdgeDef("node1", "node2", "transition")
        assert edge.source == "node1"
        assert edge.target == "node2"
        assert edge.label == "transition"

    def test_edge_def_with_empty_label(self):
        edge = EdgeDef("start", "end", "")
        assert edge.source == "start"
        assert edge.target == "end"
        assert edge.label == ""

    def test_edge_def_equality(self):
        edge1 = EdgeDef("a", "b", "label")
        edge2 = EdgeDef("a", "b", "label")
        assert edge1 == edge2

    def test_edge_def_inequality(self):
        edge1 = EdgeDef("a", "b", "label1")
        edge2 = EdgeDef("a", "b", "label2")
        assert edge1 != edge2


class TestEdgeRenderer:
    def test_render_edge_without_label(self):
        edge = EdgeDef("step1", "step2")
        result = EdgeRenderer.render(edge)
        assert result == "  step1 --> step2"

    def test_render_edge_with_simple_label(self):
        edge = EdgeDef("start", "process", "begin")
        result = EdgeRenderer.render(edge)
        assert result == "  start -->|begin| process"

    def test_render_edge_with_special_characters(self):
        edge = EdgeDef("a", "b", "test [brackets]")
        result = EdgeRenderer.render(edge)
        assert "&#91;" in result
        assert "&#93;" in result
        assert "  a -->|" in result
        assert "| b" in result

    def test_render_edge_with_empty_string_label(self):
        edge = EdgeDef("node1", "node2", "")
        result = EdgeRenderer.render(edge)
        assert result == "  node1 --> node2"

    def test_render_edge_with_complex_identifiers(self):
        edge = EdgeDef("pipeline__step1__substep", "pipeline__step2", "success")
        result = EdgeRenderer.render(edge)
        assert result == "  pipeline__step1__substep -->|success| pipeline__step2"

    def test_render_edge_with_multiline_label(self):
        edge = EdgeDef("a", "b", "line1\nline2")
        result = EdgeRenderer.render(edge)
        assert "<br/>" in result
        assert "  a -->|line1<br/>line2| b" == result

    def test_render_edge_with_all_special_chars(self):
        edge = EdgeDef("source", "target", "[{test|value}]")
        result = EdgeRenderer.render(edge)
        assert "&#91;" in result
        assert "&#123;" in result
        assert "&#124;" in result
        assert "&#125;" in result
        assert "&#93;" in result


class TestSanitizeMermaidLabel:
    def test_sanitize_backslash(self):
        result = _sanitize_mermaid_label("test\\path")
        assert result == "test\\\\path"

    def test_sanitize_newline(self):
        result = _sanitize_mermaid_label("line1\nline2")
        assert result == "line1<br/>line2"

    def test_sanitize_square_brackets(self):
        result = _sanitize_mermaid_label("[test]")
        assert result == "&#91;test&#93;"

    def test_sanitize_curly_braces(self):
        result = _sanitize_mermaid_label("{test}")
        assert result == "&#123;test&#125;"

    def test_sanitize_pipe(self):
        result = _sanitize_mermaid_label("a|b")
        assert result == "a&#124;b"

    def test_sanitize_multiple_special_chars(self):
        result = _sanitize_mermaid_label("[{test|value}]")
        assert "&#91;" in result
        assert "&#123;" in result
        assert "&#124;" in result
        assert "&#125;" in result
        assert "&#93;" in result
        assert result == "&#91;&#123;test&#124;value&#125;&#93;"

    def test_sanitize_empty_string(self):
        result = _sanitize_mermaid_label("")
        assert result == ""

    def test_sanitize_normal_text(self):
        result = _sanitize_mermaid_label("normal text")
        assert result == "normal text"

    def test_sanitize_multiple_newlines(self):
        result = _sanitize_mermaid_label("line1\nline2\nline3")
        assert result == "line1<br/>line2<br/>line3"

    def test_sanitize_mixed_special_chars(self):
        result = _sanitize_mermaid_label("path\\to\\file\nwith [brackets]")
        assert result == "path\\\\to\\\\file<br/>with &#91;brackets&#93;"

    def test_sanitize_preserves_order(self):
        result = _sanitize_mermaid_label("before\nafter")
        assert result == "before<br/>after"

    def test_sanitize_only_special_chars(self):
        result = _sanitize_mermaid_label("[]{|}\\")
        assert result == "&#91;&#93;&#123;&#124;&#125;\\\\"


class TestEdgeIntegration:
    def test_create_and_render_simple_edge(self):
        edge = EdgeDef("fetch_tickets", "process_tickets")
        rendered = EdgeRenderer.render(edge)
        assert rendered == "  fetch_tickets --> process_tickets"

    def test_create_and_render_labeled_edge(self):
        edge = EdgeDef("classifier", "updater", "success")
        rendered = EdgeRenderer.render(edge)
        assert rendered == "  classifier -->|success| updater"

    def test_create_and_render_conditional_edge(self):
        edge = EdgeDef("decision", "action", "if {{ condition }}")
        rendered = EdgeRenderer.render(edge)
        assert "decision" in rendered
        assert "action" in rendered
        assert "if &#123;&#123; condition &#125;&#125;" in rendered

    def test_create_and_render_error_edge(self):
        edge = EdgeDef("process", "error_handler", "on error: [failed]")
        rendered = EdgeRenderer.render(edge)
        assert "process" in rendered
        assert "error_handler" in rendered
        assert "&#91;failed&#93;" in rendered

    def test_render_multiple_edges(self):
        edges = [
            EdgeDef("start", "step1"),
            EdgeDef("step1", "step2", "success"),
            EdgeDef("step2", "end"),
        ]
        rendered = [EdgeRenderer.render(e) for e in edges]
        assert len(rendered) == 3
        assert rendered[0] == "  start --> step1"
        assert rendered[1] == "  step1 -->|success| step2"
        assert rendered[2] == "  step2 --> end"

    def test_edge_with_depends_on_label(self):
        edge = EdgeDef("step1", "step2", "depends on: step1")
        rendered = EdgeRenderer.render(edge)
        assert "depends on: step1" in rendered

    def test_edge_with_jinja_expression(self):
        edge = EdgeDef("check", "update", "{{ result }}")
        rendered = EdgeRenderer.render(edge)
        assert "&#123;&#123; result &#125;&#125;" in rendered

    def test_edge_between_composite_nodes(self):
        edge = EdgeDef(
            "pipeline__composite1__exit",
            "pipeline__composite2__entry",
            "transition"
        )
        rendered = EdgeRenderer.render(edge)
        assert "pipeline__composite1__exit" in rendered
        assert "pipeline__composite2__entry" in rendered
        assert "transition" in rendered


class TestEdgeValidation:
    def test_edge_with_same_source_and_target(self):
        edge = EdgeDef("node1", "node1")
        rendered = EdgeRenderer.render(edge)
        assert rendered == "  node1 --> node1"

    def test_edge_with_whitespace_in_label(self):
        edge = EdgeDef("a", "b", "  spaces  ")
        rendered = EdgeRenderer.render(edge)
        assert rendered == "  a -->|  spaces  | b"

    def test_edge_with_numeric_identifiers(self):
        edge = EdgeDef("step_0", "step_1", "next")
        rendered = EdgeRenderer.render(edge)
        assert rendered == "  step_0 -->|next| step_1"

    def test_edge_with_long_label(self):
        long_label = "This is a very long label that describes a complex transition"
        edge = EdgeDef("source", "target", long_label)
        rendered = EdgeRenderer.render(edge)
        assert long_label in rendered
        assert "  source -->|" in rendered


class TestEdgeCornerCases:
    def test_edge_label_with_only_whitespace(self):
        edge = EdgeDef("a", "b", "   ")
        rendered = EdgeRenderer.render(edge)
        assert rendered == "  a -->|   | b"

    def test_edge_with_unicode_label(self):
        edge = EdgeDef("start", "end", "übergang")
        rendered = EdgeRenderer.render(edge)
        assert "übergang" in rendered

    def test_edge_with_emoji_label(self):
        edge = EdgeDef("step1", "step2", "✓ success")
        rendered = EdgeRenderer.render(edge)
        assert "✓ success" in rendered

    def test_edge_with_tab_character(self):
        edge = EdgeDef("a", "b", "before\tafter")
        rendered = EdgeRenderer.render(edge)
        assert "\t" in rendered

    def test_edge_with_html_like_label(self):
        edge = EdgeDef("node1", "node2", "<div>test</div>")
        rendered = EdgeRenderer.render(edge)
        assert "<div>test</div>" in rendered
