from __future__ import annotations

from enum import Enum
import random
from typing import Tuple

from hamingja_dungeon.areas.vector import Vector

UNIT_VECTORS = [Vector(-1, 0), Vector(0, 1), Vector(1, 0), Vector(0, -1)]


class Direction(Enum):
    """Utility class representing a direction."""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def unit_vector(self) -> Vector:
        return UNIT_VECTORS[self.value]

    def is_vertical(self) -> bool:
        return self.value % 2 == 0

    def get_opposite(self) -> Direction:
        result = (self.value + 2) % 4
        return Direction(result)

    def is_orthogonal_to(self, other: Direction) -> bool:
        return ((self.value + 1) % 4 == other.value) or (
            (self.value - 1) % 4 == other.value
        )

    def right(self) -> Direction:
        return Direction((self.value + 1) % 4)

    def left(self) -> Direction:
        return Direction((self.value - 1) % 4)

    @staticmethod
    def get_random_direction() -> Direction:
        return Direction(random.randrange(0, 4))

    @staticmethod
    def get_all_directions() -> Tuple:
        return Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST
