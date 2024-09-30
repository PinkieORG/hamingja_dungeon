from copy import deepcopy
from typing import Tuple

import numpy as np

from hamingja_dungeon import tile_types
from hamingja_dungeon.areas.area import Area
from hamingja_dungeon.areas.dimension_range import DimensionSampler
from hamingja_dungeon.areas.dungeon_object import DungeonObject
from hamingja_dungeon.areas.exceptions import EmptyFitArea
from hamingja_dungeon.direction.direction import Direction
from hamingja_dungeon.utils.utils import circle_mask

ROOM_MIN_SIZE = (3, 3)


class Room(DungeonObject):
    def __init__(
            self,
            size: Tuple[int, int],
            fill_value: np.ndarray = None,
            border_thickness: int = 1,
            border_fill_value: np.ndarray = None,
    ):
        if fill_value is None:
            fill_value = tile_types.floor
        if border_fill_value is None:
            border_fill_value = tile_types.wall
        super().__init__(
            (max(size[0], ROOM_MIN_SIZE[0]), max(size[1], ROOM_MIN_SIZE[1])),
            fill_value=fill_value,
            border_thickness=border_thickness,
            border_fill_value=border_fill_value,
        )
        self.room_anchor = self.connected_border()


class LRoom(Room):
    def __init__(
            self,
            size: Tuple[int, int],
            fill_value: np.ndarray = None,
            border_thickness: int = 1,
            border_fill_value: np.ndarray = None,
            direction: Direction = None,
    ):
        if direction is None:
            direction = Direction.get_random_direction()
        if border_fill_value is None:
            border_fill_value = tile_types.wall
        super().__init__(
            size,
            fill_value=fill_value,
            border_thickness=border_thickness,
            border_fill_value=border_fill_value,
        )
        dim_range = DimensionSampler(
            (
                int(self.h / 2.5),
                int(self.h // 1.5),
                int(self.w // 2.5),
                int(self.w // 1.5),
            )
        )

        filling = Area(dim_range.sample())
        fit_area = self.fit_in(filling, self.corners_in_direction(direction))
        if fit_area.is_empty():
            raise EmptyFitArea("Cannot fit the filling.")
        origin = fit_area.sample()
        self.remove_area(origin, filling)
        self.draw_border(border_fill_value)


class CircleRoom(Room):
    def __init__(
            self,
            dim: int,
            fill_value: np.ndarray = None,
            border_thickness: int = 1,
            border_fill_value: np.ndarray = None,
    ):
        if border_fill_value is None:
            border_fill_value = tile_types.wall
        # Circle room dimension has to be odd.
        if dim % 2 == 0:
            dim -= 1
        super().__init__(
            (dim, dim),
            fill_value=fill_value,
            border_thickness=border_thickness,
            border_fill_value=border_fill_value,
        )
        self.mask = circle_mask(dim)
        self.draw_border(border_fill_value)

        room_anchor = deepcopy(self.mask)
        room_anchor[1:-1, 1:-1] = False
        self.room_anchor = room_anchor
