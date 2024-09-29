from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", np.bool_),
        ("transparent", np.bool_),
        ("dark", graphic_dt),
    ]
)


def new_tile(
    *,
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, dark), dtype=tile_dt)


floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("."), (255, 255, 255), (5, 10, 20)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("#"), (255, 255, 255), (5, 10, 20)),
)

void = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 128, 0)),
)

default = new_tile(
    walkable=True,
    transparent=False,
    dark=(ord("X"), (255, 255, 255), (0, 128, 0)),
)
bg = new_tile(
    walkable=True,
    transparent=False,
    dark=(ord("_"), (255, 255, 255), (0, 128, 0)),
)
carpet = new_tile(
    walkable=True,
    transparent=False,
    dark=(ord("~"), (210, 105, 30), (5, 10, 20)),
)

column = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("O"), (192, 192, 192), (5, 10, 20)),
)

border = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("B"), (255, 0, 255), (255, 0, 255)),
)

green = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("B"), (124, 252, 0), (124, 252, 0)),
)

red = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("B"), (255, 0, 0), (255, 0, 0)),
)

yellow = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("B"), (255, 255, 0), (255, 255, 0)),
)

border_debug = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("B"), (0, 0, 0), (255, 51, 204)),
)

active_room = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("#"), (255, 255, 255), (255, 0, 0)),
)
