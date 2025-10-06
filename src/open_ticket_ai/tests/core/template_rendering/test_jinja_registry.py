import pytest

from open_ticket_ai.core import (
    clear_registry,
    get_registered_methods,
    get_registered_variables,
    jinja_template_method,
    jinja_variable,
)


@pytest.fixture(autouse=True)
def reset_registry() -> None:
    clear_registry()
    yield
    clear_registry()


def test_jinja_template_method_decorator_registers_function() -> None:
    @jinja_template_method("my_filter")
    def my_filter(x: str) -> str:
        return x.upper()

    methods = get_registered_methods()
    assert "my_filter" in methods
    assert methods["my_filter"] is my_filter


def test_jinja_template_method_returns_original_function() -> None:
    @jinja_template_method("test_func")
    def test_func(x: int) -> int:
        return x * 2

    assert test_func(5) == 10


def test_jinja_variable_decorator_registers_function() -> None:
    @jinja_variable("my_data")
    def get_my_data() -> dict[str, str]:
        return {"foo": "bar"}

    variables = get_registered_variables()
    assert "my_data" in variables
    assert variables["my_data"] is get_my_data


def test_jinja_variable_returns_original_function() -> None:
    @jinja_variable("test_var")
    def test_var() -> str:
        return "test_value"

    assert test_var() == "test_value"


def test_multiple_methods_can_be_registered() -> None:
    @jinja_template_method("filter1")
    def filter1(x: str) -> str:
        return x.lower()

    @jinja_template_method("filter2")
    def filter2(x: str) -> str:
        return x.upper()

    methods = get_registered_methods()
    assert len(methods) == 2
    assert "filter1" in methods
    assert "filter2" in methods


def test_multiple_variables_can_be_registered() -> None:
    @jinja_variable("var1")
    def var1() -> str:
        return "value1"

    @jinja_variable("var2")
    def var2() -> str:
        return "value2"

    variables = get_registered_variables()
    assert len(variables) == 2
    assert "var1" in variables
    assert "var2" in variables


def test_clear_registry_removes_all_methods_and_variables() -> None:
    @jinja_template_method("method1")
    def method1(x: str) -> str:
        return x

    @jinja_variable("var1")
    def var1() -> str:
        return "value"

    assert len(get_registered_methods()) == 1
    assert len(get_registered_variables()) == 1

    clear_registry()

    assert len(get_registered_methods()) == 0
    assert len(get_registered_variables()) == 0


def test_get_registered_methods_returns_copy() -> None:
    @jinja_template_method("method1")
    def method1(x: str) -> str:
        return x

    methods = get_registered_methods()
    methods["extra"] = lambda: None

    assert "extra" not in get_registered_methods()


def test_get_registered_variables_returns_copy() -> None:
    @jinja_variable("var1")
    def var1() -> str:
        return "value"

    variables = get_registered_variables()
    variables["extra"] = lambda: None

    assert "extra" not in get_registered_variables()


def test_overwriting_method_with_same_name() -> None:
    @jinja_template_method("method1")
    def method1_v1(x: str) -> str:
        return x.lower()

    @jinja_template_method("method1")
    def method1_v2(x: str) -> str:
        return x.upper()

    methods = get_registered_methods()
    assert methods["method1"] is method1_v2


def test_overwriting_variable_with_same_name() -> None:
    @jinja_variable("var1")
    def var1_v1() -> str:
        return "value1"

    @jinja_variable("var1")
    def var1_v2() -> str:
        return "value2"

    variables = get_registered_variables()
    assert variables["var1"] is var1_v2
