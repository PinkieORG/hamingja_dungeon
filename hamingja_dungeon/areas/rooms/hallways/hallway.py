from typing import Tuple

import numpy as np

from hamingja_dungeon.areas.rooms.room import Room


class Hallway(Room):
    def __init__(
            self,
            size: Tuple[int, int],
            fill_value: np.ndarray = None,
            border_thickness: int = 1,
            border_fill_value: np.ndarray = None,
    ):
        super().__init__(
            size,
            fill_value=fill_value,
            border_thickness=border_thickness,
            border_fill_value=border_fill_value,
        )