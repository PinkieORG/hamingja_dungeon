from __future__ import annotations

from enum import Enum
import random
from typing import Tuple

from direction.connectivity import FOUR_CONNECTIVITY
from direction.orientation import Orientation


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __add__(self, other: Direction) -> Direction:
        result = (self.value + other.value) % 4
        return Direction(result)

    def coordinates(self):
        return FOUR_CONNECTIVITY[self.value]

    def get_orientation(self) -> Orientation:
        return Orientation(self.value % 2)

    def is_vertical(self):
        return self.value % 2 == 0

    def get_opposite(self) -> Direction:
        result = (self.value + 2) % 4
        return Direction(result)

    def is_neighbour(self, other: Direction) -> bool:
        return ((self.value + 1) % 4 == other.value) or (
            (self.value - 1) % 4 == other.value
        )

    def get_clockwise_neighbour(self):
        return Direction((self.value + 1) % 4)

    def get_counterclockwise_neighbour(self):
        return Direction((self.value - 1) % 4)

    @staticmethod
    def get_random_direction() -> Direction:
        return Direction(random.randrange(0, 4))

    @staticmethod
    def get_all_directions() -> Tuple:
        return Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST

    @staticmethod
    def is_horizontal(direction: Direction) -> bool:
        return direction.value % 2 == 1
