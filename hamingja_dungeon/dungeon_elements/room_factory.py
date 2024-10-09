from copy import deepcopy
from typing import Tuple

import numpy as np

from hamingja_dungeon import tile_types
from hamingja_dungeon.dungeon_elements.chamber import Chamber
from hamingja_dungeon.dungeon_elements.mask import Mask
from hamingja_dungeon.utils.dimension_sampler import DimensionSampler
from hamingja_dungeon.utils.direction import Direction
from hamingja_dungeon.utils.exceptions import EmptyFitArea
from hamingja_dungeon.utils.morphology.morphology import prune
from hamingja_dungeon.utils.utils import circle


class RoomFactory:

    def __init__(
        self,
        fill_value: np.ndarray = tile_types.floor,
        border_fill_value: np.ndarray = tile_types.wall,
    ):
        self.fill_value = fill_value
        self.border_fill_value = border_fill_value

    def rectangle_room(self, size: Tuple[int, int]):
        return Chamber(size, self.fill_value, self.border_fill_value)

    def l_room(self, size: Tuple[int, int], direction: Direction = None):
        if direction is None:
            direction = Direction.get_random_direction()
        room = Chamber(size, self.fill_value, self.border_fill_value)
        dim_range = DimensionSampler(
            (
                int(room.h // 2.5),
                int(room.h // 1.5),
                int(room.w // 2.5),
                int(room.w // 1.5),
            )
        )
        filling = Mask(dim_range.sample())
        fit_area = room.fit_in_touching_anchor(
            filling, room.corners_in_direction(direction)
        )
        if fit_area.is_empty():
            raise EmptyFitArea("Cannot fit the filling.")
        origin = fit_area.sample_mask_coordinate()
        room.remove_mask(origin, filling)
        room.entrypoints = room.border_without_corners()
        return room

    def circle_room(self, dim: int):
        if dim % 2 == 0:
            dim -= 1
        room = Chamber((dim, dim), self.fill_value, self.border_fill_value)
        room.mask = circle(dim)
        room.draw_border(self.border_fill_value)
        room_anchor = deepcopy(room.mask)
        room_anchor[1:-1, 1:-1] = False
        room_anchor = prune(room_anchor)
        room.entrypoints = Mask.from_array(room_anchor)
        return room
