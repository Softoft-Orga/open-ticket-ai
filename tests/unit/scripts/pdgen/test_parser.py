from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from scripts.pdgen.parser import ClassInfo, parse_python_file


@pytest.fixture
def tmp_python_file(tmp_path: Path) -> Path:
    return tmp_path / "test_module.py"


def test_parse_simple_class(tmp_python_file: Path):
    content = dedent("""
        from scripts.pdgen.decorator import include_in_uml

        @include_in_uml
        class SimpleClass:
            pass
    """)
    tmp_python_file.write_text(content)

    classes = parse_python_file(tmp_python_file)

    assert len(classes) == 1
    assert classes[0].name == "SimpleClass"
    assert classes[0].has_decorator is True
    assert classes[0].bases == []


def test_parse_class_with_inheritance(tmp_python_file: Path):
    content = dedent("""
        from scripts.pdgen.decorator import include_in_uml

        class BaseClass:
            pass

        @include_in_uml
        class DerivedClass(BaseClass):
            pass
    """)
    tmp_python_file.write_text(content)

    classes = parse_python_file(tmp_python_file)

    assert len(classes) == 2
    base_class = next(c for c in classes if c.name == "BaseClass")
    derived_class = next(c for c in classes if c.name == "DerivedClass")

    assert base_class.has_decorator is False
    assert derived_class.has_decorator is True
    assert derived_class.bases == ["BaseClass"]


def test_parse_multiple_inheritance(tmp_python_file: Path):
    content = dedent("""
        from scripts.pdgen.decorator import include_in_uml

        class Parent1:
            pass

        class Parent2:
            pass

        @include_in_uml
        class Child(Parent1, Parent2):
            pass
    """)
    tmp_python_file.write_text(content)

    classes = parse_python_file(tmp_python_file)

    child_class = next(c for c in classes if c.name == "Child")
    assert child_class.has_decorator is True
    assert set(child_class.bases) == {"Parent1", "Parent2"}


def test_parse_class_without_decorator(tmp_python_file: Path):
    content = dedent("""
        class PlainClass:
            pass
    """)
    tmp_python_file.write_text(content)

    classes = parse_python_file(tmp_python_file)

    assert len(classes) == 1
    assert classes[0].name == "PlainClass"
    assert classes[0].has_decorator is False


def test_parse_multiple_classes(tmp_python_file: Path):
    content = dedent("""
        from scripts.pdgen.decorator import include_in_uml

        @include_in_uml
        class FirstClass:
            pass

        class SecondClass:
            pass

        @include_in_uml
        class ThirdClass(SecondClass):
            pass
    """)
    tmp_python_file.write_text(content)

    classes = parse_python_file(tmp_python_file)

    assert len(classes) == 3
    assert sum(1 for c in classes if c.has_decorator) == 2


def test_parse_nested_class(tmp_python_file: Path):
    content = dedent("""
        from scripts.pdgen.decorator import include_in_uml

        @include_in_uml
        class OuterClass:
            class InnerClass:
                pass
    """)
    tmp_python_file.write_text(content)

    classes = parse_python_file(tmp_python_file)

    assert len(classes) == 2
    outer = next(c for c in classes if c.name == "OuterClass")
    inner = next(c for c in classes if c.name == "InnerClass")
    assert outer.has_decorator is True
    assert inner.has_decorator is False


def test_parse_invalid_python_file(tmp_python_file: Path):
    tmp_python_file.write_text("this is not valid python code {{{")
    classes = parse_python_file(tmp_python_file)
    assert classes == []


def test_parse_class_info_fields(tmp_python_file: Path):
    content = dedent("""
        from scripts.pdgen.decorator import include_in_uml

        @include_in_uml
        class TestClass:
            pass
    """)
    tmp_python_file.write_text(content)

    classes = parse_python_file(tmp_python_file)
    cls = classes[0]

    assert isinstance(cls, ClassInfo)
    assert cls.name == "TestClass"
    assert cls.module != ""
    assert cls.file_path == str(tmp_python_file)
    assert cls.has_decorator is True
    assert isinstance(cls.bases, list)
