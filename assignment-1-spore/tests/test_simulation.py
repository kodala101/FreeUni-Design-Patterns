import random

from core.builders import CreatureBuilder
from core.decorators import ClawsDecorator, TeethDecorator
from core.enums import ClawSize, ToothSharpness
from core.factories import CreatureFactory, RandomCreatureFactory
from core.models import BaseCreature, Creature, CreatureStats
from core.observers import LoggingSimulationObserver, OutcomeCounterObserver
from core.simulation import Simulation
from core.strategies import (
    ConservativeMovementStrategy,
    GreedyMovementStrategy,
    MovementStrategy,
)
from runner.main import main


class StubCreatureFactory(CreatureFactory):
    def __init__(self, creatures: list[Creature]) -> None:
        self._creatures = iter(creatures)

    def create(
        self,
        name: str,
        position: int,
        strategy: MovementStrategy,
    ) -> Creature:
        _ = (name, strategy)
        creature = next(self._creatures)
        creature.position = position
        return creature


def test_decorators_stack_in_wrapping_order() -> None:
    strategy = GreedyMovementStrategy()
    base = BaseCreature(
        name="Test",
        position=0,
        stats=CreatureStats(health=100, stamina=100, base_power=10, legs=2, wings=0),
        movement_strategy=strategy,
    )

    claws_then_teeth = TeethDecorator(
        ClawsDecorator(base, ClawSize.BIG),
        ToothSharpness.HIGH,
    )
    assert claws_then_teeth.get_attack_power() == (10 * 4) + 9

    teeth_then_claws = ClawsDecorator(
        TeethDecorator(base, ToothSharpness.HIGH),
        ClawSize.BIG,
    )
    assert teeth_then_claws.get_attack_power() == (10 + 9) * 4


def test_decorated_creature_delegates_all_properties_and_methods() -> None:
    strategy = GreedyMovementStrategy()
    decorated = (
        CreatureBuilder(name="Predator", position=0, strategy=strategy)
        .with_stats(
            CreatureStats(health=100, stamina=100, base_power=10, legs=2, wings=2),
        )
        .with_claws(ClawSize.SMALL)
        .with_teeth(ToothSharpness.LOW)
        .build()
    )

    assert decorated.name == "Predator"
    assert decorated.legs == 2
    assert decorated.wings == 2
    decorated.position = 10
    assert decorated.position == 10
    decorated.health = 80
    assert decorated.health == 80
    decorated.stamina = 90
    assert decorated.stamina == 90

    assert decorated.move() is True
    decorated.take_damage(10)
    assert decorated.health == 70
    assert decorated.is_alive() is True
    assert "Small Claws (x2)" in decorated.describe()
    assert "Low Sharpness Teeth (+3)" in decorated.describe()


def test_greedy_and_conservative_movement_strategies() -> None:
    greedy = GreedyMovementStrategy()
    flyer = (
        CreatureBuilder(name="Flyer", position=0, strategy=greedy)
        .with_stats(
            CreatureStats(health=100, stamina=85, base_power=10, legs=2, wings=2),
        )
        .build()
    )
    assert flyer.move() is True
    assert flyer.position == 8
    assert flyer.stamina == 81

    assert flyer.move() is True
    assert flyer.position == 16
    assert flyer.stamina == 77

    assert flyer.move() is True
    assert flyer.position == 22
    assert flyer.stamina == 73

    conservative = ConservativeMovementStrategy()
    walker = (
        CreatureBuilder(name="Walker", position=0, strategy=conservative)
        .with_stats(
            CreatureStats(health=100, stamina=100, base_power=10, legs=2, wings=2),
        )
        .build()
    )
    assert walker.move() is True
    assert walker.position == 4
    assert walker.stamina == 98


def test_prey_escapes_when_predator_runs_out_of_stamina() -> None:
    strategy = GreedyMovementStrategy()
    predator = (
        CreatureBuilder(name="Predator", position=0, strategy=strategy)
        .with_stats(
            CreatureStats(health=100, stamina=2, base_power=50, legs=0, wings=0),
        )
        .build()
    )
    prey = (
        CreatureBuilder(name="Pray", position=500, strategy=strategy)
        .with_stats(
            CreatureStats(health=100, stamina=100, base_power=5, legs=2, wings=2),
        )
        .build()
    )

    counter = OutcomeCounterObserver()
    sim = Simulation(
        factory=StubCreatureFactory([predator, prey]),
        predator_strategy=strategy,
        prey_strategy=strategy,
        observers=[LoggingSimulationObserver(), counter],
        rng=random.Random(42),
    )
    assert sim.run() == "Pray ran into infinity"
    assert counter.counts["Pray ran into infinity"] == 1


def test_predator_catches_and_defeats_prey() -> None:
    strategy = GreedyMovementStrategy()
    predator = (
        CreatureBuilder(name="Predator", position=0, strategy=strategy)
        .with_stats(
            CreatureStats(health=100, stamina=100, base_power=30, legs=2, wings=2),
        )
        .build()
    )
    prey = (
        CreatureBuilder(name="Pray", position=5, strategy=strategy)
        .with_stats(
            CreatureStats(health=50, stamina=10, base_power=5, legs=0, wings=0),
        )
        .build()
    )

    sim = Simulation(
        factory=StubCreatureFactory([predator, prey]),
        predator_strategy=strategy,
        prey_strategy=strategy,
        rng=random.Random(1),
    )
    assert sim.run() == "Some R-rated things have happened"


def test_mutual_kill_results_in_prey_escape_message() -> None:
    strategy = GreedyMovementStrategy()
    predator = (
        CreatureBuilder(name="Predator", position=0, strategy=strategy)
        .with_stats(
            CreatureStats(health=20, stamina=50, base_power=20, legs=2, wings=0),
        )
        .build()
    )
    prey = (
        CreatureBuilder(name="Pray", position=1, strategy=strategy)
        .with_stats(
            CreatureStats(health=20, stamina=0, base_power=20, legs=0, wings=0),
        )
        .build()
    )

    sim = Simulation(
        factory=StubCreatureFactory([predator, prey]),
        predator_strategy=strategy,
        prey_strategy=strategy,
        rng=random.Random(1),
    )
    assert sim.run() == "Pray ran into infinity"


def test_random_factory_generates_weapons_across_multiple_runs() -> None:
    factory = RandomCreatureFactory(rng=random.Random(7))
    strategy = GreedyMovementStrategy()
    descriptions = [
        factory.create(name="Predator", position=0, strategy=strategy).describe()
        for _ in range(15)
    ]
    assert any("Claws" in d for d in descriptions)
    assert any("Teeth" in d for d in descriptions)


def test_runner_main_executes() -> None:
    main()
