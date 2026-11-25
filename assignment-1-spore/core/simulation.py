import random

from core.combat import CombatResolver
from core.factories import CreatureFactory
from core.models import Creature
from core.observers import SimulationObserver
from core.strategies import MovementStrategy


class Simulation:
    def __init__(
        self,
        factory: CreatureFactory,
        predator_strategy: MovementStrategy,
        prey_strategy: MovementStrategy,
        observers: list[SimulationObserver] | None = None,
        rng: random.Random | None = None,
    ) -> None:
        self._factory = factory
        self._predator_strategy = predator_strategy
        self._prey_strategy = prey_strategy
        self._observers = observers or []
        self._rng = rng or random.Random()
        self._combat = CombatResolver()

    def run(self) -> str:
        predator, prey = self._evolve_phase()
        caught = self._chase_phase(predator, prey)
        outcome = (
            self._combat.resolve(predator, prey) if caught else "Pray ran into infinity"
        )
        for observer in self._observers:
            observer.on_finished(outcome)
        return outcome

    def _evolve_phase(self) -> tuple[Creature, Creature]:
        predator = self._factory.create(
            name="Predator",
            position=0,
            strategy=self._predator_strategy,
        )
        prey_pos = self._rng.randint(0, 1000)
        prey = self._factory.create(
            name="Pray",
            position=prey_pos,
            strategy=self._prey_strategy,
        )
        for observer in self._observers:
            observer.on_evolved(predator, prey)
        return predator, prey

    def _chase_phase(self, predator: Creature, prey: Creature) -> bool:
        while True:
            if not predator.move():
                return False
            prey.move()
            if predator.position >= prey.position:
                return True
