from dataclasses import dataclass
from typing import Tuple

import numpy as np

from hamingja_dungeon.utils.direction import Direction

SQUARE = np.array(
    [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ]
)

PLUS = np.array(
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]
)

HORIZONTAL = np.array(
    [
        [1, 1],
    ]
)

VERTICAL = np.array(
    [
        [1],
        [1],
    ]
)


INSIDE_CORNERS = {
    Direction.NORTH: (
        np.array(
            [
                [0, 0],
                [1, 0],
            ]
        ),
        (0, -1),
    ),
    Direction.EAST: (
        np.array(
            [
                [1, 0],
                [0, 0],
            ]
        ),
        (-1, -1),
    ),
    Direction.SOUTH: (
        np.array(
            [
                [0, 1],
                [0, 0],
            ]
        ),
        (-1, 0),
    ),
    Direction.WEST: (
        np.array(
            [
                [0, 0],
                [0, 1],
            ]
        ),
        (0, 0),
    ),
}


OUTSIDE_CORNERS = {
    Direction.NORTH: (
        np.array(
            [
                [1, 0],
                [1, 1],
            ]
        ),
        (0, -1),
    ),
    Direction.EAST: (
        np.array(
            [
                [1, 1],
                [1, 0],
            ]
        ),
        (-1, -1),
    ),
    Direction.SOUTH: (
        np.array(
            [
                [1, 1],
                [0, 1],
            ]
        ),
        (-1, 0),
    ),
    Direction.WEST: (
        np.array(
            [
                [0, 1],
                [1, 1],
            ]
        ),
        (0, 0),
    ),
}


@dataclass
class HoMStructure:
    """Hit or Miss structure element for a scipy operation."""

    hit: np.array
    miss: np.array
    origin: Tuple[int, int]


ENDPOINTS = {
    Direction.NORTH: HoMStructure(
        hit=np.array(
            [
                [0, 0, 0],
                [0, 1, 0],
            ]
        ),
        miss=np.array(
            [
                [0, 1, 0],
                [1, 0, 1],
            ]
        ),
        origin=(0, 0),
    ),
    Direction.EAST: HoMStructure(
        hit=np.array(
            [
                [0, 0],
                [1, 0],
                [0, 0],
            ]
        ),
        miss=np.array(
            [
                [1, 0],
                [0, 1],
                [1, 0],
            ]
        ),
        origin=(0, -1),
    ),
    Direction.SOUTH: HoMStructure(
        hit=np.array(
            [
                [0, 1, 0],
                [0, 0, 0],
            ]
        ),
        miss=np.array(
            [
                [1, 0, 1],
                [0, 1, 0],
            ]
        ),
        origin=(-1, 0),
    ),
    Direction.WEST: HoMStructure(
        hit=np.array(
            [
                [0, 0],
                [0, 1],
                [0, 0],
            ]
        ),
        miss=np.array(
            [
                [0, 1],
                [1, 0],
                [0, 1],
            ]
        ),
        origin=(0, 0),
    ),
}


def get_corner_mask(direction: Direction, thickness: int = 1):
    pass
    # TODO dilate the corner masks and detect with them the corners of variable thickness.
