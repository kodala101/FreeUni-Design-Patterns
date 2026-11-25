import logging

from core.factories import RandomCreatureFactory
from core.observers import LoggingSimulationObserver, OutcomeCounterObserver
from core.simulation import Simulation
from core.strategies import GreedyMovementStrategy


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    factory = RandomCreatureFactory()
    strategy = GreedyMovementStrategy()
    log_observer = LoggingSimulationObserver()
    counter_observer = OutcomeCounterObserver()

    for i in range(1, 101):
        logging.info("--- Simulation %d ---", i)
        sim = Simulation(
            factory=factory,
            predator_strategy=strategy,
            prey_strategy=strategy,
            observers=[log_observer, counter_observer],
        )
        sim.run()

    logging.info("Summary after 100 runs: %s", counter_observer.counts)


if __name__ == "__main__":
    main()
