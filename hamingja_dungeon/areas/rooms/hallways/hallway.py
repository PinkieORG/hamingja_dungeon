from __future__ import annotations


import numpy as np
from scipy.ndimage import binary_dilation

from hamingja_dungeon.areas.area import Area
from hamingja_dungeon.areas.morphology.morphology import get_endpoints
from hamingja_dungeon.areas.morphology.structure_elements import PLUS
from hamingja_dungeon.areas.rooms.room import Room
from hamingja_dungeon.tile_types import wall


class Hallway(Room):
    """Represents a hallway: a path-like room surrounded by walls."""

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
        borderless = np.zeros(new_size).astype(bool)
        borderless[1:-1, 1:-1] = path
        with_border = binary_dilation(borderless)

        self.mask = with_border
        self.hallway_border = Area.from_array(with_border ^ borderless)
        self.draw(wall, self.hallway_border)

        endpoints = get_endpoints(borderless)
        self.room_anchor = (
            binary_dilation(endpoints, structure=PLUS) & self.hallway_border.mask
        )
