from typing import Tuple

import numpy as np

from hamingja_dungeon import tile_types
from hamingja_dungeon.dungeon_elements.area import Area
from hamingja_dungeon.dungeon_elements.mask import Mask
from hamingja_dungeon.utils.checks.area_checks import (
    check_child_of_id_exists,
    check_value_is_tile_type,
)
from hamingja_dungeon.utils.vector import Vector

CAMBER_MIN_SIZE = (3, 3)


class Chamber(Area):
    def __init__(
            self,
            size: Tuple[int, int],
            fill_value: np.ndarray = tile_types.floor,
            border_fill_value: np.ndarray = tile_types.wall,
    ):
        super().__init__(
            (max(size[0], CAMBER_MIN_SIZE[0]), max(size[1], CAMBER_MIN_SIZE[1])),
            fill_value=fill_value,
        )
        check_value_is_tile_type(border_fill_value)
        self.draw_border(border_fill_value)
        self.entrypoints = self.border_without_corners()
        self.entrances: list[int] = []

    def place_entrance(self, origin: Vector, entrance: Area) -> int:
        entrance_id = self.add_child(origin, entrance)
        self.entrances.append(entrance_id)
        return entrance_id

    def remove_entrance(self, entrance_id: int) -> None:
        check_child_of_id_exists(entrance_id, self.children)
        self.remove_child(entrance_id)
        self.entrances.remove(entrance_id)

    def get_entrances_mask(self) -> Mask:
        return self.embedded_children_mask(self.entrances)
