from __future__ import annotations

from scripts.pdgen.generator import generate_plantuml
from scripts.pdgen.parser import ClassInfo


def test_generate_simple_diagram():
    classes = [
        ClassInfo(
            name="Vehicle",
            bases=[],
            module="test",
            has_decorator=True,
            file_path="/test.py",
        ),
    ]

    diagram = generate_plantuml(classes)

    assert "@startuml" in diagram
    assert "@enduml" in diagram
    assert "class Vehicle <<@include_in_uml>>" in diagram


def test_generate_diagram_with_inheritance():
    classes = [
        ClassInfo(
            name="Vehicle",
            bases=[],
            module="test",
            has_decorator=True,
            file_path="/test.py",
        ),
        ClassInfo(
            name="Car",
            bases=["Vehicle"],
            module="test",
            has_decorator=True,
            file_path="/test.py",
        ),
    ]

    diagram = generate_plantuml(classes)

    assert "class Vehicle <<@include_in_uml>>" in diagram
    assert "class Car <<@include_in_uml>>" in diagram
    assert "Vehicle <|-- Car" in diagram


def test_generate_diagram_child_decorated_parent_not():
    classes = [
        ClassInfo(
            name="Vehicle",
            bases=[],
            module="test",
            has_decorator=False,
            file_path="/test.py",
        ),
        ClassInfo(
            name="Car",
            bases=["Vehicle"],
            module="test",
            has_decorator=True,
            file_path="/test.py",
        ),
    ]

    diagram = generate_plantuml(classes)

    assert "class Vehicle" in diagram
    assert "class Car <<@include_in_uml>>" in diagram
    assert "Vehicle <|-- Car" in diagram


def test_generate_diagram_parent_decorated_child_not():
    classes = [
        ClassInfo(
            name="Vehicle",
            bases=[],
            module="test",
            has_decorator=True,
            file_path="/test.py",
        ),
        ClassInfo(
            name="Car",
            bases=["Vehicle"],
            module="test",
            has_decorator=False,
            file_path="/test.py",
        ),
    ]

    diagram = generate_plantuml(classes)

    assert "class Vehicle <<@include_in_uml>>" in diagram
    assert "class Car" in diagram
    assert "Vehicle <|-- Car" in diagram


def test_generate_diagram_excludes_unrelated_classes():
    classes = [
        ClassInfo(
            name="Vehicle",
            bases=[],
            module="test",
            has_decorator=True,
            file_path="/test.py",
        ),
        ClassInfo(
            name="UnrelatedClass",
            bases=[],
            module="test",
            has_decorator=False,
            file_path="/test.py",
        ),
    ]

    diagram = generate_plantuml(classes)

    assert "class Vehicle <<@include_in_uml>>" in diagram
    assert "UnrelatedClass" not in diagram


def test_generate_diagram_multiple_inheritance():
    classes = [
        ClassInfo(
            name="Vehicle",
            bases=[],
            module="test",
            has_decorator=True,
            file_path="/test.py",
        ),
        ClassInfo(
            name="Electric",
            bases=[],
            module="test",
            has_decorator=True,
            file_path="/test.py",
        ),
        ClassInfo(
            name="ElectricCar",
            bases=["Vehicle", "Electric"],
            module="test",
            has_decorator=False,
            file_path="/test.py",
        ),
    ]

    diagram = generate_plantuml(classes)

    assert "class Vehicle <<@include_in_uml>>" in diagram
    assert "class Electric <<@include_in_uml>>" in diagram
    assert "class ElectricCar" in diagram
    assert "Vehicle <|-- ElectricCar" in diagram
    assert "Electric <|-- ElectricCar" in diagram


def test_generate_diagram_deep_inheritance():
    classes = [
        ClassInfo(
            name="Vehicle",
            bases=[],
            module="test",
            has_decorator=True,
            file_path="/test.py",
        ),
        ClassInfo(
            name="Car",
            bases=["Vehicle"],
            module="test",
            has_decorator=False,
            file_path="/test.py",
        ),
        ClassInfo(
            name="SportsCar",
            bases=["Car"],
            module="test",
            has_decorator=False,
            file_path="/test.py",
        ),
    ]

    diagram = generate_plantuml(classes)

    assert "class Vehicle <<@include_in_uml>>" in diagram
    assert "class Car" in diagram
    assert "class SportsCar" in diagram
    assert "Vehicle <|-- Car" in diagram
    assert "Car <|-- SportsCar" in diagram


def test_generate_empty_diagram():
    classes: list[ClassInfo] = []
    diagram = generate_plantuml(classes)

    assert "@startuml" in diagram
    assert "@enduml" in diagram


def test_generate_diagram_no_decorated_classes():
    classes = [
        ClassInfo(
            name="PlainClass",
            bases=[],
            module="test",
            has_decorator=False,
            file_path="/test.py",
        ),
    ]

    diagram = generate_plantuml(classes)

    assert "@startuml" in diagram
    assert "@enduml" in diagram
    assert "PlainClass" not in diagram
