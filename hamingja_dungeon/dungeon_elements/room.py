from copy import deepcopy
from typing import Tuple

import numpy as np

from hamingja_dungeon import tile_types
from hamingja_dungeon.dungeon_elements.mask import Mask
from hamingja_dungeon.utils.dimension_sampler import DimensionSampler
from hamingja_dungeon.dungeon_elements.area import Area
from hamingja_dungeon.utils.exceptions import EmptyFitArea
from hamingja_dungeon.utils.morphology.morphology import prune
from hamingja_dungeon.utils.direction import Direction
from hamingja_dungeon.tile_types import tile_dt
from hamingja_dungeon.utils.utils import circle_mask
from hamingja_dungeon.utils.vector import Vector

ROOM_MIN_SIZE = (3, 3)


class Room(Area):
    """Represent a room that can be inserted into dungeon area."""

    def __init__(
        self,
        size: Tuple[int, int],
        fill_value: np.ndarray = None,
        border_fill_value: np.ndarray = None,
    ):
        if fill_value is None:
            fill_value = tile_types.floor
        if border_fill_value is None:
            border_fill_value = tile_types.wall
        if fill_value.dtype != tile_dt or border_fill_value.dtype != tile_dt:
            raise ValueError("Fill value has to have the tile dtype.")
        super().__init__(
            (max(size[0], ROOM_MIN_SIZE[0]), max(size[1], ROOM_MIN_SIZE[1])),
            fill_value=fill_value,
        )
        self.draw_border(border_fill_value)
        self.entrypoints = self.connected_border()
        self.entrances: list[int] = []

    def place_entrance(self, origin: Vector, entrance: Area) -> int:
        id = self.add_child(origin, entrance)
        self.entrances.append(id)
        return id

    def remove_entrance(self, id: int) -> None:
        if id not in self.entrances:
            raise ValueError("Entrance with this id does not exist.")
        self.remove_child(id)
        self.entrances.remove(id)

    def get_entrances_area(self) -> Mask:
        result = Area.empty(self.size)
        for entrance_id in self.entrances:
            entrance = self.get_child(entrance_id)
            result.insert_shape(entrance.origin, entrance.object)
        return result

class LRoom(Room):
    def __init__(
        self,
        size: Tuple[int, int],
        fill_value: np.ndarray = None,
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
            border_fill_value=border_fill_value,
        )
        dim_range = DimensionSampler(
            (
                int(self.h // 2.5),
                int(self.h // 1.5),
                int(self.w // 2.5),
                int(self.w // 1.5),
            )
        )

        filling = Mask(dim_range.sample())
        fit_area = self.fit_in(filling, self.corners_in_direction(direction))
        if fit_area.is_empty():
            raise EmptyFitArea("Cannot fit the filling.")
        origin = fit_area.sample()
        self.remove_shape(origin, filling)
        self.draw_border(border_fill_value)
        self.entrypoints = self.connected_border()


class CircleRoom(Room):
    def __init__(
        self,
        dim: int,
        fill_value: np.ndarray = None,
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
            border_fill_value=border_fill_value,
        )
        self.mask = circle_mask(dim)
        self.draw_border(border_fill_value)

        room_anchor = deepcopy(self.mask)
        room_anchor[1:-1, 1:-1] = False
        room_anchor = prune(room_anchor)
        self.entrypoints = Mask.from_array(room_anchor)
