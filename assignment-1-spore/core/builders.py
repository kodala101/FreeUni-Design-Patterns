from typing import Self

from core.decorators import ClawsDecorator, TeethDecorator
from core.enums import ClawSize, ToothSharpness
from core.models import BaseCreature, Creature, CreatureStats
from core.strategies import MovementStrategy


class CreatureBuilder:
    def __init__(
        self,
        name: str,
        position: int,
        strategy: MovementStrategy,
    ) -> None:
        self._name = name
        self._position = position
        self._strategy = strategy
        self._stats = CreatureStats(
            health=100,
            stamina=100,
            base_power=10,
            legs=2,
            wings=0,
        )
        self._claws: ClawSize | None = None
        self._teeth: ToothSharpness | None = None

    def with_stats(self, stats: CreatureStats) -> Self:
        self._stats = stats
        return self

    def with_claws(self, size: ClawSize | None) -> Self:
        self._claws = size
        return self

    def with_teeth(self, sharpness: ToothSharpness | None) -> Self:
        self._teeth = sharpness
        return self

    def build(self) -> Creature:
        creature: Creature = BaseCreature(
            name=self._name,
            position=self._position,
            stats=self._stats,
            movement_strategy=self._strategy,
        )
        if self._claws is not None:
            creature = ClawsDecorator(creature, self._claws)
        if self._teeth is not None:
            creature = TeethDecorator(creature, self._teeth)
        return creature
