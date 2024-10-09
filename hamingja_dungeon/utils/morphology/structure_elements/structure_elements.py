import numpy as np

from hamingja_dungeon.utils.direction import Direction
from hamingja_dungeon.utils.morphology.structure_elements.utils import (CompoundStructure,
                                                                        Structure, )
from hamingja_dungeon.utils.vector import Vector

SQUARE = Structure(
    fg=np.array(
        [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
    ),
    origin=Vector(0, 0),
)

PLUS_SIGN = Structure(
    np.array(
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]
    ),
    origin=Vector(0, 0),
)

BORDERS_FOR_EROSION = {
    Direction.NORTH: Structure(
        fg=np.array(
            [
                [1],
                [1],
            ]
        ),
        origin=Vector(0, 0),
    ),
    Direction.EAST: Structure(
        fg=np.array(
            [
                [1, 1],
            ]
        ),
        origin=Vector(0, -1),
    ),
    Direction.SOUTH: Structure(
        fg=np.array(
            [
                [1],
                [1],
            ]
        ),
        origin=Vector(-1, 0),
    ),
    Direction.WEST: Structure(
        fg=np.array(
            [
                [1, 1],
            ]
        ),
        origin=Vector(0, 0),
    ),
}
HORIZONTAL_TUPLE = np.array(
    [
        [1, 1],
    ]
)

VERTICAL_TUPLE = np.array(
    [
        [1],
        [1],
    ]
)


INSIDE_CORNERS = {
    Direction.NORTH: Structure(
        fg=np.array(
            [
                [0, 0],
                [1, 0],
            ]
        ),
        origin=Vector(0, -1),
    ),
    Direction.EAST: Structure(
        fg=np.array(
            [
                [1, 0],
                [0, 0],
            ]
        ),
        origin=Vector(-1, -1),
    ),
    Direction.SOUTH: Structure(
        fg=np.array(
            [
                [0, 1],
                [0, 0],
            ]
        ),
        origin=Vector(-1, 0),
    ),
    Direction.WEST: Structure(
        fg=np.array(
            [
                [0, 0],
                [0, 1],
            ]
        ),
        origin=Vector(0, 0),
    ),
}


OUTSIDE_CORNERS = {
    Direction.NORTH: Structure(
        fg=np.array(
            [
                [1, 0],
                [1, 1],
            ]
        ),
        origin=Vector(0, -1),
    ),
    Direction.EAST: Structure(
        fg=np.array(
            [
                [1, 1],
                [1, 0],
            ]
        ),
        origin=Vector(-1, -1),
    ),
    Direction.SOUTH: Structure(
        fg=np.array(
            [
                [1, 1],
                [0, 1],
            ]
        ),
        origin=Vector(-1, 0),
    ),
    Direction.WEST: Structure(
        fg=np.array(
            [
                [0, 1],
                [1, 1],
            ]
        ),
        origin=Vector(0, 0),
    ),
}

ENDPOINTS = {
    Direction.NORTH: CompoundStructure(
        fg=np.array(
            [
                [0, 0, 0],
                [0, 1, 0],
            ]
        ),
        bg=np.array(
            [
                [0, 1, 0],
                [1, 0, 1],
            ]
        ),
        origin=Vector(0, 0),
    ),
    Direction.EAST: CompoundStructure(
        fg=np.array(
            [
                [0, 0],
                [1, 0],
                [0, 0],
            ]
        ),
        bg=np.array(
            [
                [1, 0],
                [0, 1],
                [1, 0],
            ]
        ),
        origin=Vector(0, -1),
    ),
    Direction.SOUTH: CompoundStructure(
        fg=np.array(
            [
                [0, 1, 0],
                [0, 0, 0],
            ]
        ),
        bg=np.array(
            [
                [1, 0, 1],
                [0, 1, 0],
            ]
        ),
        origin=Vector(-1, 0),
    ),
    Direction.WEST: CompoundStructure(
        fg=np.array(
            [
                [0, 0],
                [0, 1],
                [0, 0],
            ]
        ),
        bg=np.array(
            [
                [0, 1],
                [1, 0],
                [0, 1],
            ]
        ),
        origin=Vector(0, 0),
    ),
}


def get_corner_mask(direction: Direction, thickness: int = 1):
    pass
    # TODO dilate the corner masks and detect with them the corners of variable thickness.
