from __future__ import annotations

from typing import Tuple


class Vector:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other: Vector):
        return Vector(self.y + other.y, self.x + other.x)

    def __sub__(self, other: Vector):
        return Vector(self.y - other.y, self.x - other.x)

    def is_positive(self):
        return self.x >= 0 and self.y >= 0

    @staticmethod
    def from_tuple(tup: Tuple[int, int]):
        return Vector(*tup)
