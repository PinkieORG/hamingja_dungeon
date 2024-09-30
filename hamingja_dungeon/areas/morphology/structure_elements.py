from dataclasses import dataclass
from typing import Tuple

import numpy as np

from hamingja_dungeon.direction.direction import Direction

SQUARE = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])

HORIZONTAL = np.array([[1, 1]])

VERTICAL = np.array([[1], [1]])

CORNERS = {
    Direction.NORTH: (np.array([[0, 0], [1, 0]]), (0, -1)),
    Direction.EAST: (np.array([[1, 0], [0, 0]]), (-1, -1)),
    Direction.SOUTH: (np.array([[0, 1], [0, 0]]), (-1, 0)),
    Direction.WEST: (np.array([[0, 0], [0, 1]]), (0, 0)),
}


@dataclass
class HoMStructure:
    hit: np.array
    miss: np.array
    origin: Tuple[int, int]


ENDPOINTS_4 = {
    Direction.NORTH: HoMStructure(
        hit=np.array([[0, 0, 0], [0, 1, 0]]),
        miss=np.array([[0, 1, 0], [1, 0, 1]]),
        origin=(0, 0),
    ),
    Direction.EAST: HoMStructure(
        hit=np.array([[0, 0], [1, 0], [0, 0]]),
        miss=np.array([[1, 0], [0, 1], [1, 0]]),
        origin=(0, -1),
    ),
    Direction.SOUTH: HoMStructure(
        hit=np.array([[0, 1, 0], [0, 0, 0]]),
        miss=np.array([[1, 0, 1], [0, 1, 0]]),
        origin=(-1, 0),
    ),
    Direction.WEST: HoMStructure(
        hit=np.array([[0, 0], [0, 1], [0, 0]]),
        miss=np.array([[0, 1], [1, 0], [0, 1]]),
        origin=(0, 0),
    ),
}


def get_corner_mask(direction: Direction, thickness: int = 1):
    pass
    # TODO dilate the corner masks and detect with them the corners of variable thickness.
