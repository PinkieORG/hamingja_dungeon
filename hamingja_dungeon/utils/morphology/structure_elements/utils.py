from dataclasses import dataclass
from typing import Tuple

import numpy as np

from hamingja_dungeon.utils.vector import Vector


@dataclass
class Structure:
    """A structure element for a scipy operation."""

    fg: np.array
    origin: Vector


@dataclass
class CompoundStructure(Structure):
    """Hit or Miss structure element for a scipy operation."""

    bg: np.array


def center_to_top_left(size: Tuple[int, int]) -> Vector:
    return Vector(-(size[0] // 2), -(size[1] // 2))


def center_to_bottom_right(size: Tuple[int, int]) -> Vector:
    return Vector((size[0] - 1) // 2, (size[1] - 1) // 2)
