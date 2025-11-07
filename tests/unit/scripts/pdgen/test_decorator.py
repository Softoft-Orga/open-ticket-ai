from __future__ import annotations

from scripts.pdgen.decorator import include_in_uml


def test_include_in_uml_decorator_sets_attribute():
    @include_in_uml
    class TestClass:
        pass

    assert hasattr(TestClass, "__include_in_uml__")
    assert TestClass.__include_in_uml__ is True


def test_include_in_uml_preserves_class_functionality():
    @include_in_uml
    class TestClass:
        value: int = 42

        def method(self) -> str:
            return "test"

    instance = TestClass()
    assert instance.value == 42
    assert instance.method() == "test"


def test_include_in_uml_works_with_inheritance():
    @include_in_uml
    class Parent:
        pass

    class Child(Parent):
        pass

    assert hasattr(Parent, "__include_in_uml__")
    assert Parent.__include_in_uml__ is True
    assert hasattr(Child, "__include_in_uml__")
    assert not hasattr(Child, "__dict__") or "__include_in_uml__" not in Child.__dict__
