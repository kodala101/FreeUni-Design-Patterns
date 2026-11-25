from enum import Enum


class MovementType(Enum):
    FLYING = ("Flying", 80, 4, 8)
    RUNNING = ("Running", 60, 4, 6)
    WALKING = ("Walking", 40, 2, 4)
    HOPPING = ("Hopping", 20, 2, 3)
    CRAWLING = ("Crawling", 0, 1, 1)

    def __init__(
        self,
        label: str,
        min_stamina: int,
        stamina_cost: int,
        speed: int,
    ) -> None:
        self.label = label
        self.min_stamina = min_stamina
        self.stamina_cost = stamina_cost
        self.speed = speed


class ClawSize(Enum):
    SMALL = ("Small", 2)
    MEDIUM = ("Medium", 3)
    BIG = ("Big", 4)

    def __init__(self, label: str, multiplier: int) -> None:
        self.label = label
        self.multiplier = multiplier


class ToothSharpness(Enum):
    LOW = ("Low Sharpness", 3)
    MEDIUM = ("Medium Sharpness", 6)
    HIGH = ("High Sharpness", 9)

    def __init__(self, label: str, bonus: int) -> None:
        self.label = label
        self.bonus = bonus
