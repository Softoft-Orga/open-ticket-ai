import pytest

from open_ticket_ai.core import (
    clear_registry,
    jinja_template_method,
    jinja_variable,
)
from open_ticket_ai.core.template_rendering.jinja_renderer import JinjaRenderer


@pytest.fixture(autouse=True)
def reset_registry() -> None:
    clear_registry()
    yield
    clear_registry()


def test_jinja_renderer_loads_registered_methods() -> None:
    @jinja_template_method("my_upper")
    def my_upper(x: str) -> str:
        return x.upper()

    renderer = JinjaRenderer()
    result = renderer.render("{{ my_upper('hello') }}", {})

    assert result == "HELLO"


def test_jinja_renderer_loads_registered_variables() -> None:
    @jinja_variable("test_data")
    def get_test_data() -> dict[str, str]:
        return {"key": "value"}

    renderer = JinjaRenderer()
    result = renderer.render("{{ test_data.key }}", {})

    assert result == "value"


def test_jinja_renderer_loads_multiple_methods() -> None:
    @jinja_template_method("double")
    def double(x: int) -> int:
        return x * 2

    @jinja_template_method("triple")
    def triple(x: int) -> int:
        return x * 3

    renderer = JinjaRenderer()
    result = renderer.render("{{ double(5) }}, {{ triple(5) }}", {})

    assert result == "10, 15"


def test_jinja_renderer_loads_multiple_variables() -> None:
    @jinja_variable("var1")
    def get_var1() -> str:
        return "value1"

    @jinja_variable("var2")
    def get_var2() -> str:
        return "value2"

    renderer = JinjaRenderer()
    result = renderer.render("{{ var1 }}-{{ var2 }}", {})

    assert result == "value1-value2"


def test_registered_methods_work_with_existing_functionality() -> None:
    @jinja_template_method("custom_filter")
    def custom_filter(x: str) -> str:
        return f"custom_{x}"

    renderer = JinjaRenderer()

    result = renderer.render("{{ custom_filter('test') }}", {})
    assert result == "custom_test"


def test_registered_variables_work_with_scope() -> None:
    @jinja_variable("global_prefix")
    def get_global_prefix() -> str:
        return "PREFIX"

    renderer = JinjaRenderer()
    result = renderer.render("{{ global_prefix }}_{{ local_var }}", {"local_var": "local"})

    assert result == "PREFIX_local"


def test_multiple_renderer_instances_share_registry() -> None:
    @jinja_template_method("shared_func")
    def shared_func(x: str) -> str:
        return f"shared_{x}"

    renderer1 = JinjaRenderer()
    renderer2 = JinjaRenderer()

    result1 = renderer1.render("{{ shared_func('test1') }}", {})
    result2 = renderer2.render("{{ shared_func('test2') }}", {})

    assert result1 == "shared_test1"
    assert result2 == "shared_test2"


def test_registered_method_with_complex_logic() -> None:
    @jinja_template_method("format_list")
    def format_list(items: list[str]) -> str:
        return ", ".join(items)

    renderer = JinjaRenderer()
    result = renderer.render("{{ format_list(['a', 'b', 'c']) }}", {})

    assert result == "a, b, c"


def test_registered_variable_with_complex_structure() -> None:
    @jinja_variable("config")
    def get_config() -> dict[str, dict[str, str]]:
        return {"database": {"host": "localhost", "port": "5432"}}

    renderer = JinjaRenderer()
    result = renderer.render("{{ config.database.host }}:{{ config.database.port }}", {})

    assert result == "localhost:5432"


def test_empty_registry_does_not_break_renderer() -> None:
    clear_registry()
    renderer = JinjaRenderer()
    result = renderer.render("{{ 1 + 1 }}", {})

    assert result == 2


def test_registered_method_can_be_used_as_filter() -> None:
    @jinja_template_method("reverse")
    def reverse(x: str) -> str:
        return x[::-1]

    renderer = JinjaRenderer()
    result = renderer.render("{{ 'hello' | reverse }}", {})

    assert result == "olleh"


def test_variable_function_is_called_during_initialization() -> None:
    call_count = {"count": 0}

    @jinja_variable("counter_var")
    def get_counter() -> int:
        call_count["count"] += 1
        return call_count["count"]

    renderer1 = JinjaRenderer()
    result1 = renderer1.render("{{ counter_var }}", {})

    renderer2 = JinjaRenderer()
    result2 = renderer2.render("{{ counter_var }}", {})

    assert result1 == 1
    assert result2 == 2
