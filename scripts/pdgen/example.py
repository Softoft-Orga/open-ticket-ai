from scripts.pdgen.decorator import include_in_uml


@include_in_uml
class Vehicle:
    def start(self) -> None:
        pass


class Car(Vehicle):
    def honk(self) -> None:
        pass


@include_in_uml
class Bike(Vehicle):
    def ring_bell(self) -> None:
        pass


class SportsCar(Car):
    def activate_turbo(self) -> None:
        pass


@include_in_uml
class Electric:
    def charge(self) -> None:
        pass


class ElectricCar(Car, Electric):
    pass


class UnrelatedClass:
    pass
