from __future__ import annotations
import numpy as np
from scipy.ndimage import binary_dilation
from skimage.measure import label

from hamingja_dungeon.dungeon_elements.mask import Mask
from hamingja_dungeon.utils.morphology.morphology import get_endpoints
from hamingja_dungeon.utils.morphology.structure_elements import PLUS, SQUARE
from hamingja_dungeon.dungeon_elements.room import Room
from hamingja_dungeon.tile_types import wall
from hamingja_dungeon.utils.utils import tighten


# TODO create a common super class for hallway and room (region, section?) since hallway is not really a room, is it?
class Hallway(Room):
    """Represents a hallway: a path-like room surrounded by walls."""

    def __init__(
        self,
        path: np.array,
        fill_value: np.ndarray = None,
        border_fill_value: np.ndarray = None,
    ):
        path = tighten(path)
        new_size = (path.shape[0] + 2, path.shape[1] + 2)
        super().__init__(
            new_size,
            fill_value=fill_value,
            border_fill_value=border_fill_value,
        )

        borderless = np.zeros(new_size).astype(bool)
        borderless[1:-1, 1:-1] = path
        with_border = binary_dilation(borderless, structure=SQUARE)
        self.mask = with_border
        self.hallway_border = Mask.from_array(with_border ^ borderless)
        self.draw(wall, self.hallway_border)
        self.endpoints = get_endpoints(borderless)
        self.entrypoints = Mask.from_array(
            binary_dilation(self.endpoints, structure=PLUS) & self.border().mask
        )

    # TODO Make about localisation not only binary check.
    # TODO: make it work for very short hallways.
    def has_dead_end(self):
        labeled, count = label(self.endpoints, background=0, return_num=True)
        entrances = self.get_entrances_area()
        for component_label in range(1, count + 1):
            end = np.where(labeled == component_label, 1, 0)
            if not np.any(binary_dilation(end, structure=PLUS) & entrances.array):
                return True
        return False
