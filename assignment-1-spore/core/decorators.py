from core.enums import ClawSize, ToothSharpness
from core.models import Creature


class CreatureDecorator(Creature):
    def __init__(self, wrapped: Creature) -> None:
        self._wrapped = wrapped

    @property
    def name(self) -> str:
        return self._wrapped.name

    @property
    def position(self) -> int:
        return self._wrapped.position

    @position.setter
    def position(self, value: int) -> None:
        self._wrapped.position = value

    @property
    def health(self) -> int:
        return self._wrapped.health

    @health.setter
    def health(self, value: int) -> None:
        self._wrapped.health = value

    @property
    def stamina(self) -> int:
        return self._wrapped.stamina

    @stamina.setter
    def stamina(self, value: int) -> None:
        self._wrapped.stamina = value

    @property
    def legs(self) -> int:
        return self._wrapped.legs

    @property
    def wings(self) -> int:
        return self._wrapped.wings

    def get_attack_power(self) -> int:
        return self._wrapped.get_attack_power()

    def move(self) -> bool:
        return self._wrapped.move()

    def take_damage(self, amount: int) -> None:
        self._wrapped.take_damage(amount)

    def is_alive(self) -> bool:
        return self._wrapped.is_alive()

    def describe(self) -> str:
        return self._wrapped.describe()


class ClawsDecorator(CreatureDecorator):
    def __init__(self, wrapped: Creature, size: ClawSize) -> None:
        super().__init__(wrapped)
        self._size = size

    def get_attack_power(self) -> int:
        return self._wrapped.get_attack_power() * self._size.multiplier

    def describe(self) -> str:
        return (
            f"{self._wrapped.describe()} + "
            f"{self._size.label} Claws (x{self._size.multiplier})"
        )


class TeethDecorator(CreatureDecorator):
    def __init__(self, wrapped: Creature, sharpness: ToothSharpness) -> None:
        super().__init__(wrapped)
        self._sharpness = sharpness

    def get_attack_power(self) -> int:
        return self._wrapped.get_attack_power() + self._sharpness.bonus

    def describe(self) -> str:
        return (
            f"{self._wrapped.describe()} + "
            f"{self._sharpness.label} Teeth (+{self._sharpness.bonus})"
        )
