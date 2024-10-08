from dataclasses import dataclass

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
