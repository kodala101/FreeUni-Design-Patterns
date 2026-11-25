import logging
from abc import ABC, abstractmethod

from core.models import Creature


class SimulationObserver(ABC):
    @abstractmethod
    def on_evolved(self, predator: Creature, prey: Creature) -> None: ...

    @abstractmethod
    def on_finished(self, outcome: str) -> None: ...


class LoggingSimulationObserver(SimulationObserver):
    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(__name__)

    def on_evolved(self, predator: Creature, prey: Creature) -> None:
        self._logger.info("Evolved: %s", predator.describe())
        self._logger.info("Evolved: %s", prey.describe())

    def on_finished(self, outcome: str) -> None:
        self._logger.info(outcome)


class OutcomeCounterObserver(SimulationObserver):
    def __init__(self) -> None:
        self.counts: dict[str, int] = {}

    def on_evolved(self, predator: Creature, prey: Creature) -> None:
        _ = (predator, prey)

    def on_finished(self, outcome: str) -> None:
        self.counts[outcome] = self.counts.get(outcome, 0) + 1
