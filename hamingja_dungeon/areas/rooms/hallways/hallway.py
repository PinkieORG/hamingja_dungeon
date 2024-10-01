from __future__ import annotations

from typing import Tuple

import numpy as np
from scipy.ndimage import binary_dilation

from hamingja_dungeon.areas.area import Area
from hamingja_dungeon.areas.rooms.room import Room
from hamingja_dungeon.tile_types import carpet, wall


def tighten(array: np.array):
    non_zero_rows = np.where(np.any(array != 0, axis=1))[0]
    non_zero_columns = np.where(np.any(array != 0, axis=0))[0]

    return array[
        non_zero_rows.min() : non_zero_rows.max() + 1,
        non_zero_columns.min() : non_zero_columns.max() + 1,
    ]


class Hallway(Room):
    def __init__(
        self,
        path: np.array,
        fill_value: np.ndarray = None,
        border_fill_value: np.ndarray = None,
    ):
        new_size = (path.shape[0] + 2, path.shape[1] + 2)
        super().__init__(
            new_size,
            fill_value=fill_value,
            border_fill_value=border_fill_value,
        )
        enlarged = np.zeros(new_size).astype(bool)
        enlarged[1:-1, 1:-1] = path

        structure = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])

        mask = binary_dilation(enlarged, structure=structure)

        self.mask = mask
        hallway_border = Area.from_array(mask ^ enlarged)
        self.draw(wall, hallway_border)
