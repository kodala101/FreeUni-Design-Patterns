from __future__ import annotations

from abc import ABC, abstractmethod

from core.enums import MovementType
from core.models import Creature


class MovementHandler(ABC):
    def __init__(self, next_handler: MovementHandler | None = None) -> None:
        self._next = next_handler

    def handle(self, creature: Creature) -> bool:
        if self._can_execute(creature):
            self._apply(creature)
            return True
        if self._next is not None:
            return self._next.handle(creature)
        return False

    @property
    @abstractmethod
    def _movement_type(self) -> MovementType: ...

    @abstractmethod
    def _has_required_limbs(self, creature: Creature) -> bool: ...

    def _can_execute(self, creature: Creature) -> bool:
        move = self._movement_type
        return (
            self._has_required_limbs(creature)
            and creature.stamina >= move.min_stamina
            and creature.stamina >= move.stamina_cost
        )

    def _apply(self, creature: Creature) -> None:
        move = self._movement_type
        creature.stamina -= move.stamina_cost
        creature.position += move.speed


class FlyHandler(MovementHandler):
    @property
    def _movement_type(self) -> MovementType:
        return MovementType.FLYING

    def _has_required_limbs(self, creature: Creature) -> bool:
        return creature.wings >= 2


class RunHandler(MovementHandler):
    @property
    def _movement_type(self) -> MovementType:
        return MovementType.RUNNING

    def _has_required_limbs(self, creature: Creature) -> bool:
        return creature.legs >= 2


class WalkHandler(MovementHandler):
    @property
    def _movement_type(self) -> MovementType:
        return MovementType.WALKING

    def _has_required_limbs(self, creature: Creature) -> bool:
        return creature.legs >= 2


class HopHandler(MovementHandler):
    @property
    def _movement_type(self) -> MovementType:
        return MovementType.HOPPING

    def _has_required_limbs(self, creature: Creature) -> bool:
        return creature.legs >= 1


class CrawlHandler(MovementHandler):
    @property
    def _movement_type(self) -> MovementType:
        return MovementType.CRAWLING

    def _has_required_limbs(self, creature: Creature) -> bool:
        _ = creature
        return True
