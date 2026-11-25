from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core.movement import (
    CrawlHandler,
    FlyHandler,
    HopHandler,
    MovementHandler,
    RunHandler,
    WalkHandler,
)

if TYPE_CHECKING:
    from core.models import Creature


class MovementStrategy(ABC):
    @abstractmethod
    def execute_move(self, creature: Creature) -> bool: ...


class GreedyMovementStrategy(MovementStrategy):
    def __init__(self) -> None:
        self._chain: MovementHandler = FlyHandler(
            RunHandler(
                WalkHandler(
                    HopHandler(
                        CrawlHandler(),
                    ),
                ),
            ),
        )

    def execute_move(self, creature: Creature) -> bool:
        return self._chain.handle(creature)


class ConservativeMovementStrategy(MovementStrategy):
    def __init__(self) -> None:
        self._chain: MovementHandler = WalkHandler(
            HopHandler(
                CrawlHandler(),
            ),
        )

    def execute_move(self, creature: Creature) -> bool:
        return self._chain.handle(creature)
