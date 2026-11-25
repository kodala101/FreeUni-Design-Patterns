import random
from abc import ABC, abstractmethod

from core.builders import CreatureBuilder
from core.enums import ClawSize, ToothSharpness
from core.models import Creature, CreatureStats
from core.strategies import MovementStrategy


class CreatureFactory(ABC):
    @abstractmethod
    def create(
        self,
        name: str,
        position: int,
        strategy: MovementStrategy,
    ) -> Creature: ...


class RandomCreatureFactory(CreatureFactory):
    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()

    def create(
        self,
        name: str,
        position: int,
        strategy: MovementStrategy,
    ) -> Creature:
        stats = CreatureStats(
            health=self._rng.randint(60, 150),
            stamina=self._rng.randint(60, 150),
            base_power=self._rng.randint(5, 15),
            legs=self._rng.randint(0, 4),
            wings=self._rng.randint(0, 4),
        )
        claw_choice = self._rng.choice([None, *list(ClawSize)])
        teeth_choice = self._rng.choice([None, *list(ToothSharpness)])

        return (
            CreatureBuilder(name=name, position=position, strategy=strategy)
            .with_stats(stats)
            .with_claws(claw_choice)
            .with_teeth(teeth_choice)
            .build()
        )
