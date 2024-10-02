from __future__ import annotations
from typing import Tuple


class Vector:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def __eq__(self, other: Vector) -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.y + other.y, self.x + other.x)

    def __iadd__(self, other: Vector) -> Vector:
        self.y += other.y
        self.x += other.x
        return self

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.y - other.y, self.x - other.x)

    def __isub__(self, other: Vector) -> Vector:
        self.y -= other.y
        self.x -= other.x
        return self

    def __mul__(self, other: int) -> Vector:
        return Vector(other * self.y, other * self.x)

    def __rmul__(self, other: int) -> Vector:
        return self * other

    def __imul__(self, other: int) -> Vector:
        self.y *= other
        self.x *= other
        return self

    def __str__(self):
        return f"({self.y}, {self.x})"

    def is_positive(self) -> bool:
        return self.x >= 0 and self.y >= 0

    def neighbours(self) -> list[Vector]:
        result = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                result.append(Vector(self.y + y, self.x + x))
        result.remove(self)
        return result

    @staticmethod
    def from_tuple(tup: Tuple[int, int]) -> Vector:
        return Vector(*tup)
