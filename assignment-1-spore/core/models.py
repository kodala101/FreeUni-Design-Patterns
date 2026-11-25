from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.strategies import MovementStrategy


@dataclass(frozen=True)
class CreatureStats:
    health: int
    stamina: int
    base_power: int
    legs: int
    wings: int


class Creature(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def position(self) -> int: ...

    @position.setter
    @abstractmethod
    def position(self, value: int) -> None: ...

    @property
    @abstractmethod
    def health(self) -> int: ...

    @health.setter
    @abstractmethod
    def health(self, value: int) -> None: ...

    @property
    @abstractmethod
    def stamina(self) -> int: ...

    @stamina.setter
    @abstractmethod
    def stamina(self, value: int) -> None: ...

    @property
    @abstractmethod
    def legs(self) -> int: ...

    @property
    @abstractmethod
    def wings(self) -> int: ...

    @abstractmethod
    def get_attack_power(self) -> int: ...

    @abstractmethod
    def move(self) -> bool: ...

    @abstractmethod
    def take_damage(self, amount: int) -> None: ...

    @abstractmethod
    def is_alive(self) -> bool: ...

    @abstractmethod
    def describe(self) -> str: ...


class BaseCreature(Creature):
    def __init__(
        self,
        name: str,
        position: int,
        stats: CreatureStats,
        movement_strategy: MovementStrategy,
    ) -> None:
        self._name = name
        self._position = position
        self._health = stats.health
        self._stamina = stats.stamina
        self._base_power = stats.base_power
        self._legs = stats.legs
        self._wings = stats.wings
        self._movement_strategy = movement_strategy

    @property
    def name(self) -> str:
        return self._name

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, value: int) -> None:
        self._position = value

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int) -> None:
        self._health = max(0, value)

    @property
    def stamina(self) -> int:
        return self._stamina

    @stamina.setter
    def stamina(self, value: int) -> None:
        self._stamina = max(0, value)

    @property
    def legs(self) -> int:
        return self._legs

    @property
    def wings(self) -> int:
        return self._wings

    def get_attack_power(self) -> int:
        return self._base_power

    def move(self) -> bool:
        return self._movement_strategy.execute_move(self)

    def take_damage(self, amount: int) -> None:
        self.health = self._health - amount

    def is_alive(self) -> bool:
        return self._health > 0

    def describe(self) -> str:
        return (
            f"{self._name} [Pos: {self._position}, HP: {self._health}, "
            f"Stamina: {self._stamina}, BasePower: {self._base_power}, "
            f"Legs: {self._legs}, Wings: {self._wings}]"
        )
